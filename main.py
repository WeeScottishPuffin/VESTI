import interactions as interface
import time, os, random
from sys import platform

HELP={
	"exit": "exit\n exits the program",
	"help": "help [cmd]\n displays a help message for a given command, or a list of commands if none is given",
	"select": "select {-c|-g} {lisenceplate|garageID}\n selects either a car by lisenceplate (-c) or a garage by ID (-g)",
}
CARS=[interface.Car("BAN ONE","Firebird (\'77)","Pontiac","Black"),
	  interface.Car("LU 6789","DB5","Aston Martin","Silver"),
	  interface.Car("XAB 235","Mustang (\'69)","Ford","Grey"),
	  interface.Car("OUTATIME","DeLorean","DMC","Sliver"),
	  interface.Car(" 1971 ","Duster 340 (\'71)","Plymouth","Green")
]
GARAGES=[interface.Garage([],3),interface.Garage([],2)]
gdict={}
for garage in GARAGES: gdict[garage.getId()] = garage

#Not specified how lisence instances should be instanced. COde below will iterate over the car list and create a lisence instance assigned to each car. For testing this can be modified. The lisences are not saved to a list as they should be evaluted as needed when parking cars. The distributed lisences are valid for a randomly chosen garage.

for car in CARS:
	interface.Lisence(car,random.randint(0,len(GARAGES)-1))
	
VERSION="1.0"
hour = time.localtime()[3]
running = True

if 12 > hour > 6: print("Доброе утро")
elif 18 > hour > 12: print("Добрый день")
else: print("Добрый вечер")
print("Parking Manager CLI version %s"%VERSION)
print("By WeeScottishPuffin")
time.sleep(3)

def sf(car):return car.getLisencePlate()
CARS.sort(key=sf)

def clear():
	match platform:
		case "linux"|"linux2"|"darwin":
			# shell or zsh (I don't judge)
			os.system("clear")
		case "win32"|"cygwin":
			# msdos
			os.system("cls")

while running:
	ioIN = input("> ").lower().split(" ")
	cmd = ioIN[0]
	args:list = ioIN[1:]

	match cmd:
		case "quit"|"exit":
			running = False
			print("До свидания!")
			time.sleep(1)

		case "help":
			if args:print(HELP[args[0]])
			else:
				for msg in HELP.values(): print(msg,"\n")

		case "select":
			if args and len(args) > 1:
				if args[0] == "-c":
					#selecting a car by lisence
					if args[1]:pass
				elif args[0] == "-g":
					pass
				else:print("Invalid argument at position 1: %s given, expected -c or -g"%args[0]")
			else:print("Invalid number of arguments: %s given, 2 expected."%len(args))