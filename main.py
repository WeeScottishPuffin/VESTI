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
	CARS.append(interface.Car(car["plate"].upper().replace(" ",""), car["brand"], car["model"], car["colour"]))
for garage in state["garages"]: 
	n = interface.Garage([], garage["cap"])
	GARAGES.append(n)
	gdict[n.getId()] = n
	
##Not specified how lisence instances should be instanced. COde below will iterate over the car list and create a lisence instance assigned to each car. For testing this can be modified. The lisences are not saved to a list as they should be evaluted as needed when parking cars. The distributed lisences are valid for a randomly chosen garage. Might move it to state.json later.

#Give each car a lisence
for car in CARS:
	interface.Lisence(car, 2)

#Greet the user and display a welcome message (Could add an MOTD like the old ARPA/INTER NET)
if 12 > hour > 6: print("Доброе утро")
elif 18 > hour > 12: print("Добрый день")
else: print("Добрый вечер")
print("VESTI Parking Manager CLI version %s" % VERSION)
print("By WeeScottishPuffin")

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
						s = True
						args[1]=args[1].upper()
						for car in CARS:
							if car.getLisencePlate() == args[1]: 
								selectedCar = car
								print("Succesfully selected car with lisence: %s"%args[1])
								s = False
								print(selectedCar.__dict__) #temporary
								break #To escape the for loop
						if s:print("Unable to find car with lisence: %s"%args[1])
					else:
						print("Invalid number of arguments: %s given, 1 expected." % len(args))
								
				elif args[0] == "-g":
					#Selecting a garage by ID
					if args[1]:
						try:
							id = int(args[1])
						except ValueError:
							print("Invalid numerical ID: %s"%args[1])
						else:
							if id in gdict.keys():
								selectedGarage = gdict[id]
								print("Succesfully selected garage with ID: %s"%args[1])
								print(selectedGarage.__dict__) #temporary
							else:
								print("Unable to find garage with ID: %s"%args[1])
					else:
						print("Invalid number of arguments: %s given, 1 expected." % len(args))
				else:
					print("Invalid argument at position 1: %s given, expected -c or -g" %args[0])
			else:
				print("Invalid number of arguments: %s given, 2 expected." % len(args))


		case "hand":
			sc,sg = None,None
			if selectedCar: sc = selectedCar.getLisencePlate()
			if selectedGarage: sg = selectedGarage.getId()
			print("Selected Car: %s" % sc)
			print("Selected Garage: %s" % sg)

		case "clear": clear()

		case "list":
			if len(args) > 0:
				if args[0] == "-c":
					print("PLATE","MODEL","BRAND","COLOUR",sep=10*" ")
					for car in CARS:
						pla,mod,bra,col=car.getLisencePlate()[:14],car.getModel()[:14],car.getBrand()[:14],car.getColour()[:15]
						print(pla,(15-len(pla))*" ",mod,(15-len(mod))*" ",bra,(15-len(bra))*" ",col,sep="")
					lx=54-len(str(len(CARS)))	
					if lx%2 == 0: print("-"*int(lx/2),"%s TOTAL"%len(CARS),"-"*int(lx/2),sep="")
					else: print("-"*int(lx/2),"%s TOTAL-"%len(CARS),"-"*int(lx/2),sep="")
				elif args[0] == "-g":
					for garage in GARAGES:
						print("%s: (%s/%s)"%(garage.getId(),garage.getCapacity(),garage.maxCapacity))
				else:
					print("Invalid argument at position 1: %s given, expected -c or -g" %args[0])
			else:
				print("Invalid number of arguments: %s given, 1 expected." % len(args))

		case "ginfo":
			if selectedGarage:
				print("Garage Info for ID: %s"%selectedGarage.getId())
				print("Maximum Capacity  : %s"%selectedGarage.maxCapacity)
				print("Used Capacity     : %s (%s%%)"%(selectedGarage.getCapacity(),int(selectedGarage.getCapacity()/selectedGarage.maxCapacity*100)))
				print("Parked Cars       :")
				print("PLATE","MODEL","BRAND","COLOUR",sep=10*" ")
				for car in sorted(selectedGarage.parkedCars,key=sf):
					pla,mod,bra,col=car.getLisencePlate()[:14],car.getModel()[:14],car.getBrand()[:14],car.getColour()[:15]
					print(pla,(15-len(pla))*" ",mod,(15-len(mod))*" ",bra,(15-len(bra))*" ",col,sep="")
				lx=54-len(str(len(selectedGarage.parkedCars)))	
				if lx%2 == 0: print("-"*int(lx/2),"%s TOTAL"%len(CARS),"-"*int(lx/2),sep="")
				else: print("-"*int(lx/2),"%s TOTAL-"%len(CARS),"-"*int(lx/2),sep="")
			else:
				print("No garage selected")

		case "cinfo":
			if selectedCar:
				print("PLATE:    %s"%selectedCar.getLisencePlate())
				print("MODEL:    %s"%selectedCar.getModel())
				print("BRAND:    %s"%selectedCar.getBrand())
				print("COLOUR:   %s"%selectedCar.getColour())
			else:
				print("No car selected")
