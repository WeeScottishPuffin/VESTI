import interactions as interface
import time, os, random, json
from sys import platform
import argparse

HELP = {																					#Help messages
		"cinfo":"cinfo\n shows information about the currently selected car",
		"ginfo":"ginfo\n shows information about the currently selected garage",
		"hand":"hand\n shows the currently selected car and garage",
    "help":"help [cmd]\n displays a help message for a given command, or a list of commands if none is given",
		"list":"list {-c|-g}\n lists all cars (-c) or all garages (-g)",
		"park":"park\n parks the currently selected car in the currently selected garage",
    "select":"select {-c|-g} {lisenceplate|garageID}\n selects either a car by lisenceplate (-c) or a garage by ID (-g)",
		"unpark":"unpark\n unparks the currently selected car from the currently selected garage"
}

cars = []
garages = []
lisences = {}
selectedCar = None
selectedGarage = None

#Program is not persistent, so data needs to be stored in state.json
def getJsonData():
    global cars,garages,selectedCar,selectedGarage #Global scope
    with open("./state.json") as state:
        data = json.load(state)
    
    for car in data["cars"]: #Create car objects
        newCar = interface.Car(
            car["plate"],
            car["brand"],
            car["model"],
            car["colour"]
        )
        cars.append(newCar)
        #Create lisence for car
        lisences[newCar] = interface.Lisence(newCar,car["lisenceNum"])
        #Check if the car is selected
        if data["selectedCar"] == car["plate"]:
            selectedCar = newCar

    for garage in data["garages"]: #Create garage objects
        newGarage = interface.Garage(
            garage["parked"],
            garage["cap"]
        )
        garages.append(newGarage)

        for car in garage["parked"]: #Create car objects for parked cars aswell
            newCar = interface.Car( 
                car["plate"],
                car["brand"],
                car["model"],
                car["colour"]
            )
            cars.append(newCar)
            lisences[newCar] = interface.Lisence(newCar,newCar["lisenceNum"])
        #Check if the current garage is selected
        if data["selectedGarage"] == garage["id"]:
            selectedGarage = newGarage

def putJsonData():
    global cars,garages,selectedCar,selectedGarage #Global scope
    jsonObj = { #Pack it neatly into json
        "cars":[c.toJson() for c in cars],
        "garages":[g.toJson() for g in garages],
        "selectedCar":selectedCar.getLisencePlate() if selectedCar else None,
        "selectedGarage":selectedGarage.getId() if selectedGarage else None
    }

    with open("state,json","w") as state:
        json.dump(jsonObj,state)

getJsonData()

print(cars[1].toJson())
cars[1].colour = "Silver"
print(cars[1].toJson())

putJsonData()

# parser = argparse.ArgumentParser(description="CLI to inteface with VESTI.")
# subparsers = parser.add_subparsers(required=True)

#Command: CINFO
