import interactions as interface
import time, os, random, json
from sys import platform

HELP = {																					#Help messages
		"cinfo":"cinfo\n shows information about the currently selected car",
		"clear":"clear\n clears the cli interface",
    "exit":"exit\n exits the program",
		"ginfo":"ginfo\n shows information about the currently selected garage",
		"hand":"hand\n shows the currently selected car and garage",
    "help":"help [cmd]\n displays a help message for a given command, or a list of commands if none is given",
		"list":"list {-c|-g}\n lists all cars (-c) or all garages (-g)",
		"park":"park\n parks the currently selected car in the currently selected garage",
    "select":"select {-c|-g} {lisenceplate|garageID}\n selects either a car by lisenceplate (-c) or a garage by ID (-g)",
		"unpark":"unpark\n unparks the currently selected car from the currently selected garage"
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
	c = interface.Car(car["plate"].upper().replace(" ",""), car["brand"], car["model"], car["colour"])
	CARS.append(c)
	interface.Lisence(c, car["lisenceNum"])
for garage in state["garages"]: 
	n = interface.Garage([], garage["cap"])
	GARAGES.append(n)
	gdict[n.getId()] = n	

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
	match cmd:
        #Quit
		case "quit" | "exit":
			running = False #Change running flag to false
			print("До свидания!") #Goodbye )
			time.sleep(1)
        #Help message
		case "help":
			if args: #the user specified a command
				if args[0] in HELP.keys(): #Check if the user entered a valid command
					print(HELP[args[0]]) #Print the corresponding help message
			else: #If not, print a list of commands
				for msg in HELP.values():
					print(msg, "\n")
		#Select a car or a garage
		case "select":
			if args and len(args) > 1: #Check if the user specified 2 or more arguments. Any args after the 2nd get ignored
				if args[0] == "-c":
					#selecting a car by lisence
					if args[1]: #Redundant check for the 2nd argument
						s = True #Keep track if a match was found. True == no match found
						args[1]=args[1].upper()	#Plates get converted to upper case, so should the query
						for car in CARS:
							if car.getLisencePlate() == args[1]: 
								selectedCar = car
								print("Succesfully selected car with lisence: %s"%args[1])
								s = False #Indicate we found a match
								break #To escape the for loop, match-case statements have no fallthrough
						if s:print("Unable to find car with lisence: %s"%args[1]) #If the flag is still true, we haven't found a match
					else: #error message
						print("Invalid number of arguments: %s given, 1 expected." % len(args))
								
				elif args[0] == "-g":
					#Selecting a garage by ID
					if args[1]: #Redundant check for the 2nd argument
						try: #Need to catch ValueErrors when converting between datatypes
							id = int(args[1])
						except ValueError: #Error
							print("Invalid numerical ID: %s"%args[1])
						else: #Only executes if no error was triggered
							if id in gdict.keys(): #Check if the id is present to avoid errors
								selectedGarage = gdict[id]
								print("Succesfully selected garage with ID: %s"%args[1])
							else: print("Unable to find garage with ID: %s"%args[1])#Error message
					else: print("Invalid number of arguments: %s given, 1 expected." % len(args))#Error message
				else: print("Invalid argument at position 1: %s given, expected -c or -g" %args[0])#Error message
			else: print("Invalid number of arguments: %s given, 2 expected." % len(args)) #Error message
		#Check selected items
		case "hand":
			sc,sg = None,None #Display data variables of the selected objects
			if selectedCar: sc = selectedCar.getLisencePlate()
			if selectedGarage: sg = selectedGarage.getId()
			print("Selected Car: %s" % sc)
			print("Selected Garage: %s" % sg)
		#Clear the screen
		case "clear": clear()
		#List either all cars or all garages
		case "list":
			if len(args) > 0: #Check for -c/-g flag
				if args[0] == "-c":
					#Cars
					print("PLATE","MODEL","BRAND","COLOUR",sep=10*" ") #'Table' header
					for car in CARS:
						pla,mod,bra,col=car.getLisencePlate()[:14],car.getModel()[:14],car.getBrand()[:14],car.getColour()[:15] #Truncate to account for limited space
						print(pla,(15-len(pla))*" ",mod,(15-len(mod))*" ",bra,(15-len(bra))*" ",col,sep="") #Loving the oneliners; some simple math to calculate the right whitespacing
					lx=54-len(str(len(CARS))) #Amount of - characters for the footer row	
					if lx%2 == 0: print("-"*int(lx/2),"%s TOTAL"%len(CARS),"-"*int(lx/2),sep="") #Either equally divide it in two
					else: print("-"*int(lx/2),"%s TOTAL-"%len(CARS),"-"*int(lx/2),sep="") #Or shift the remainder to the righthand-side
				elif args[0] == "-g":
					#Garages
					for garage in GARAGES:
						print("%s: (%s/%s)"%(garage.getId(),garage.getCapacity(),garage.maxCapacity)) #garage id: (used/max)
				else: print("Invalid argument at position 1: %s given, expected -c or -g" %args[0]) #Error message
			else: print("Invalid number of arguments: %s given, 1 expected." % len(args)) #Error message
		#Selected garage info
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
				if lx%2 == 0: print("-"*int(lx/2),"%s TOTAL"%len(CARS),"-"*int(lx/2),sep="")
				else: print("-"*int(lx/2),"%s TOTAL-"%len(selectedGarage.parkedCars),"-"*int(lx/2),sep="")
			else:
				print("No garage selected")
		#Selected car info
		case "cinfo":
			if selectedCar:
				print("PLATE:    %s"%selectedCar.getLisencePlate())
				print("MODEL:    %s"%selectedCar.getModel())
				print("BRAND:    %s"%selectedCar.getBrand())
				print("COLOUR:   %s"%selectedCar.getColour())
			else:
				print("No car selected")
		#Park the selected car in the selected garage
		case "park":
			if selectedCar: #check if user selected a car
				if selectedGarage: #check if user selected a garage
					#CONFIRM choice
					print("Trying to park car with plate: %s in garage with ID: %s. Type CONFIRM and press enter to continue."%(selectedCar.getLisencePlate(),selectedGarage.getId()))
					c = input("> ").upper()
					if c == "CONFIRM":
						pt = selectedGarage.parkCar(selectedCar) #Parking logic handled by interactions.py. It returns a boolean (True if it was succesfull)
						if pt:
							print("Car with plate %s succesfully parked in garage with ID %s" %(selectedCar.getLisencePlate(),selectedGarage.getId()))
						else: #Check what the issue was
							if selectedGarage.getCapacity() == selectedGarage.maxCapacity: print("Unable to park car: garage with ID %s is full" %selectedGarage.getId())
							else: print("Unable to park car: lisence of car with plate %s is not valid" %selectedCar.getLisencePlate())
					else: print("Aborting.") #abort
				else: print("No garage selected") #error msg
			else: print("No car selected") #error msg
		#Remove the selected car from the selected garage
		case "unpark":
			if selectedCar: #check if user selected a car
				if selectedGarage: #check if user selected a garage
					if selectedCar in selectedGarage.parkedCars: #Check if the car is in the specified garage
						#CONFIRM choice
						print("Trying to unpark car with plate: %s from garage with ID: %s. Type CONFIRM and press enter to continue."%(selectedCar.getLisencePlate(),selectedGarage.getId()))
						c = input("> ").upper()
						if c == "CONFIRM":
							selectedGarage.unparkCar(selectedCar)
							print("Car with plate %s succesfully removed from garage with ID %s" %(selectedCar.getLisencePlate(),selectedGarage.getId()))
						else: print("Aborting.") #abort
					else: print("Unable to unpark car: car with plate %s is not parked in garage with ID %s"%(selectedCar.getLisencePlate(),selectedGarage.getId())) #error msg
				else: print("No garage selected") #error msg
			else: print("No car selected") #error msg
		#Unknown command
		case _: print("Unknown command: %s" % cmd)

####################################################
#                POSSIBLE ADDITIONS                #
#--------------------------------------------------#
# - Currently parked info for each car             #
# - Fancier garagelist                             #
# - ASCII art logo screen                          #
#                                                  #
####################################################