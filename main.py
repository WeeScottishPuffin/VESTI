#!/usr/bin/env python 
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
unparkedCars = []
garages = []
lisences = {}
selectedCar = None
selectedGarage = None

def sf(car): 
    return car.getLisencePlate()

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
        unparkedCars.append(newCar)
        #Create lisence for car
        lisences[newCar] = interface.Lisence(newCar,car["lisenceNum"])
        #Check if the car is selected
        if data["selectedCar"] == car["plate"]:
            selectedCar = newCar

    for garage in data["garages"]: #Create garage objects
        parked = []
        for car in garage["parked"]: #Create car objects for parked cars aswell
            newCar = interface.Car( 
                car["plate"],
                car["brand"],
                car["model"],
                car["colour"]
            )
            cars.append(newCar)
            parked.append(newCar)
            lisences[newCar] = interface.Lisence(newCar,car["lisenceNum"])
            if data["selectedCar"] == car["plate"]:
                selectedCar = newCar
        newGarage = interface.Garage(
            parked,
            garage["cap"]
        )
        garages.append(newGarage)
        #Check if the current garage is selected
        if data["selectedGarage"] == garage["id"]:
            selectedGarage = newGarage

def putJsonData():
    global cars,garages,selectedCar,selectedGarage #Global scope
    jsonObj = { #Pack it neatly into json
        "cars":[c.toJson() for c in unparkedCars],
        "garages":[g.toJson() for g in garages],
        "selectedCar":selectedCar.getLisencePlate() if selectedCar else None,
        "selectedGarage":selectedGarage.getId() if selectedGarage else None
    }

    with open("state.json","w") as state:
        json.dump(jsonObj,state)

getJsonData()
parser = argparse.ArgumentParser(description="CLI to inteface with VESTI.")
subparsers = parser.add_subparsers(required=True,dest="command")

c_cinfo = subparsers.add_parser("cinfo")
c_ginfo = subparsers.add_parser("ginfo")
c_hand = subparsers.add_parser("hand")
c_list = subparsers.add_parser("list")
c_list_flags = c_list.add_mutually_exclusive_group(required=True)
c_list_flags.add_argument("-c", action="store_true")
c_list_flags.add_argument("-g", action="store_true")
c_select = subparsers.add_parser("select")
c_select_flags = c_select.add_mutually_exclusive_group(required=True)
c_select_flags.add_argument("-c", action="store_true")
c_select_flags.add_argument("-g", action="store_true")
c_select.add_argument("identifier")
c_park = subparsers.add_parser("park")
c_unpark = subparsers.add_parser("unpark")


#Parse arguments
args = parser.parse_args()

match args.command:
    case "cinfo":
        if selectedCar:
            print("PLATE:    %s"%selectedCar.getLisencePlate())
            print("MODEL:    %s"%selectedCar.getModel())
            print("BRAND:    %s"%selectedCar.getBrand())
            print("COLOUR:   %s"%selectedCar.getColour())
        else:
            print("No car selected!")
    case "ginfo":
        if selectedGarage: #Check if the user has selected a garage
            print("Garage Info for ID: %s"%selectedGarage.getId())
            print("Maximum Capacity  : %s"%selectedGarage.maxCapacity)
            print("Used Capacity     : %s (%s%%)"%(selectedGarage.getCapacity(),int(selectedGarage.getCapacity()/selectedGarage.maxCapacity*100)))
            print("Parked Cars       :")
            print("PLATE","MODEL","BRAND","COLOUR",sep=10*" ")
            for car in sorted(selectedGarage.parkedCars,key=sf): #Same table as above (list case)
                pla,mod,bra,col=car.getLisencePlate()[:14],car.getModel()[:14],car.getBrand()[:14],car.getColour()[:15]
                print(pla,(15-len(pla))*" ",mod,(15-len(mod))*" ",bra,(15-len(bra))*" ",col,sep="")
            lx=54-len(str(len(selectedGarage.parkedCars)))	
            if lx%2 == 0: print("-"*int(lx/2),"%s TOTAL"%len(selectedGarage.parkedCars),"-"*int(lx/2),sep="")
            else: print("-"*int(lx/2),"%s TOTAL-"%len(selectedGarage.parkedCars),"-"*int(lx/2),sep="")
        else:
            print("No garage selected")
    case "hand":
        sc,sg = None,None #Display data variables of the selected objects
        if selectedCar: sc = selectedCar.getLisencePlate()
        if selectedGarage: sg = selectedGarage.getId()
        print("Selected Car: %s" % sc)
        print("Selected Garage: %s" % sg)
    case "list":
        if args.c:
            #Cars
            print("PLATE","MODEL","BRAND","COLOUR",sep=10*" ") #'Table' header
            for car in cars:
                pla,mod,bra,col=car.getLisencePlate()[:14],car.getModel()[:14],car.getBrand()[:14],car.getColour()[:15] #Truncate to account for limited space
                print(pla,(15-len(pla))*" ",mod,(15-len(mod))*" ",bra,(15-len(bra))*" ",col,sep="") #Loving the oneliners; some simple math to calculate the right whitespacing
            lx=54-len(str(len(cars))) #Amount of - characters for the footer row	
            if lx%2 == 0: print("-"*int(lx/2),"%s TOTAL"%len(cars),"-"*int(lx/2),sep="") #Either equally divide it in two
            else: print("-"*int(lx/2),"%s TOTAL-"%len(cars),"-"*int(lx/2),sep="") #Or shift the remainder to the righthand-side
        elif args.g:
            for garage in garages:
                print("%s: (%s/%s)"%(garage.getId(),garage.getCapacity(),garage.maxCapacity)) #garage id: (used/max)
        else:
            pass
    case "select":
        if args.c:
            s = True #Keep track if a match was found. True == no match found
            iden = args.identifier.upper()	#Plates get converted to upper case, so should the query
            for car in cars:
                if car.getLisencePlate() == iden: 
                    selectedCar = car
                    print("Succesfully selected car with lisence: %s"%iden)
                    s = False #Indicate we found a match
                    break #To escape the for loop, match-case statements have no fallthrough
            if s:print("Unable to find car with lisence: %s"%iden) #If the flag is still true, we haven't found a match
					
        elif args.g:
            s = True #!Match found
            try:
                iden = int(args.identifier)
            except ValueError:
                print("Invalid garage ID: %s"%args.identifier)
            else:
                for garage in garages:
                    if garage.getId() == iden:
                        selectedGarage = garage
                        print("Succesfully selected garage with id: %s"%iden)
                        s=False
                        break
                if s:print("Unable to find garage with ID:%s"%iden)
    case "park":
        if selectedCar:
            if selectedGarage:
                if selectedCar in unparkedCars:
                    #Try parking car
                    i = input("Park car with plates: %s in garage with ID: %s? (y/N) "%(selectedCar.getLisencePlate(),selectedGarage.getId()))
                    if i.lower() == "y":
                        pc = selectedGarage.parkCar(selectedCar)
                        if pc:
                            unparkedCars.remove(selectedCar)
                            print("Succesfully parked car with plates: %s in garage with ID: %s"%(selectedCar.getLisencePlate(),selectedGarage.getId()))
                        else:
                            print("Unable to park car.")
                else:
                    print("Car is already parked!")
            else:
                print("No garage selected!")
        else:
            print("No car selected!")
    case "unpark":
        if selectedCar:
            if selectedGarage:
                if selectedCar in selectedGarage.parkedCars:
                    selectedGarage.unparkCar(selectedCar)
                    print("Succesfully unparked car form garage!")
                else:
                    print("Selected car is not parked in selected garage!")
            else:
                print("No garage selected!")
        else:
            print("No car selected!")
    case _:
        print("No command")

putJsonData()