import interactions as interface
import time, os, random, json
from sys import platform

HELP = {
    "exit":
    "exit\n exits the program",
    "help":
    "help [cmd]\n displays a help message for a given command, or a list of commands if none is given",
    "select":
    "select {-c|-g} {lisenceplate|garageID}\n selects either a car by lisenceplate (-c) or a garage by ID (-g)",
}
CARS = []
GARAGES = []
VERSION = "1.0"
hour = time.localtime()[3]
running = True
gdict = {}

with open("state.json", "r") as f:
    state = json.load(f)

for car in state["cars"]:
	CARS.append(interface.Car(car["plate"], car["brand"], car["model"], car["colour"]))
for garage in state["garages"]: 
	n = interface.Garage([], garage["cap"])
	GARAGES.append(n)
	gdict[n.getId()] = n
	
#Not specified how lisence instances should be instanced. COde below will iterate over the car list and create a lisence instance assigned to each car. For testing this can be modified. The lisences are not saved to a list as they should be evaluted as needed when parking cars. The distributed lisences are valid for a randomly chosen garage. Might move it to state.json later.

for car in CARS:
	interface.Lisence(car, random.randint(0, len(GARAGES) - 1))

if 12 > hour > 6: print("Доброе утро")
elif 18 > hour > 12: print("Добрый день")
else: print("Добрый вечер")
print("VESTI Parking Manager CLI version %s" % VERSION)
print("By WeeScottishPuffin")
time.sleep(3)


def sf(car):
	return car.getLisencePlate()
CARS.sort(key=sf)

def clear():
	match platform:
		case "linux" | "linux2" | "darwin":
			# shell or zsh (I don't judge)
			os.system("clear")
		case "win32" | "cygwin":
			# msdos
			os.system("cls")

while running:
	ioIN = input("> ").lower().split(" ")
	cmd = ioIN[0]
	args: list = ioIN[1:]

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
					if args[1]: pass
				elif args[0] == "-g":
					pass
				else:
					print("Invalid argument at position 1: %s given, expected -c or -g" %
					      args[0])
			else:
				print("Invalid number of arguments: %s given, 2 expected." % len(args))
