import interactions as interface
import time, os, random, json
from sys import platform

HELP = {																					#Help messages
    "exit":
    "exit\n exits the program",
    "help":
    "help [cmd]\n displays a help message for a given command, or a list of commands if none is given",
    "select":
    "select {-c|-g} {lisenceplate|garageID}\n selects either a car by lisenceplate (-c) or a garage by ID (-g)",
}
CARS = []																					#List of cars loaded from state.json
GARAGES = []																			#List of garages, idem	
VERSION = "beta"																	#Version of the program (1.0 will be first working version)
hour = time.localtime()[3]												#Current hour, used to determine the correct greeting
running = True																		#Flag to determine if the program is running
gdict = {}																				#Dictionary to store garage objects with their ID as keys
selectedCar,selectedGarage = None,None						#Currently selected car and garage, None by default

#Open state.json and load the data into the lists
with open("state.json", "r") as f:
    state = json.load(f)

#Save data from state.json to the lists
for car in state["cars"]:
	CARS.append(interface.Car(car["plate"], car["brand"], car["model"], car["colour"]))
for garage in state["garages"]: 
	n = interface.Garage([], garage["cap"])
	GARAGES.append(n)
	gdict[n.getId()] = n
	
##Not specified how lisence instances should be instanced. COde below will iterate over the car list and create a lisence instance assigned to each car. For testing this can be modified. The lisences are not saved to a list as they should be evaluted as needed when parking cars. The distributed lisences are valid for a randomly chosen garage. Might move it to state.json later.

#Give each car a lisence
for car in CARS:
	interface.Lisence(car, random.randint(0, len(GARAGES) - 1))

#Greet the user and display a welcome message (Could add an MOTD like the old ARPA/INTER NET)
if 12 > hour > 6: print("Доброе утро")
elif 18 > hour > 12: print("Добрый день")
else: print("Добрый вечер")
print("VESTI Parking Manager CLI version %s" % VERSION)
print("By WeeScottishPuffin")
time.sleep(3)

#The sort function to sort cars by alphabetical order to make displaying them all easier
def sf(car): return car.getLisencePlate()

#A universal clear function
def clear():
	match platform:
		case "linux" | "linux2" | "darwin":
			# shell or zsh (I don't judge)
			os.system("clear")
		case "win32" | "cygwin":
			# msdos
			os.system("cls")

#THE MAINLOOP
while running:
	ioIN = input("> ").lower().split(" ")																								#Get raw-ish input
	cmd = ioIN[0]																																				#The actual command itself
	args: list = ioIN[1:]																																#The arguments of the command

	#Match-Case structure to 'parse commands'
	#Will add more comments when I'm done
	match cmd:
		case "quit" | "exit":
			running = False
			print("До свидания!")
			time.sleep(1)

		case "help":
			if args: print(HELP[args[0]])
			else:
				for msg in HELP.values():
					print(msg, "\n")

		case "select":
			if args and len(args) > 1:
				if args[0] == "-c":
					#selecting a car by lisence
					if args[1]: 
						for car in CARS:
							if car.getLisencePlate() == args[1]: 
								selected = car
								print("Succesfully selected car with lisence: %s"%args[1])
								print(selected.__dict__) #temporary
								break
							print("Unable to find car with lisence: %s"%args[1])
								
				elif args[0] == "-g":
					pass
				else:
					print("Invalid argument at position 1: %s given, expected -c or -g" %args[0])
			else:
				print("Invalid number of arguments: %s given, 2 expected." % len(args))
