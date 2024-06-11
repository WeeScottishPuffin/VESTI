import interactions as interface
import time, os
from sys import platform

CARS=[interface.Car("BAN ONE","Firebird (\'77)","Pontiac","Black"),
	  interface.Car("LU 6789","DB5","Aston Martin","Silver"),
	  interface.Car("XAB 235","Mustang (\'69)","Ford","Grey"),
	  interface.Car("OUTATIME","DeLorean","DMC","Sliver"),
	  interface.Car(" 1971 ","Duster 340 (\'71)","Plymouth","Green")
]
GARAGES=[interface.Garage([],3)]
gdict={}
for garage in GARAGES: gdict[garage.getId()] = garage
VERSION="1.0"
hour = time.localtime()[3]

if 12 > hour > 6: print("Доброе утро")
elif 18 > hour > 12: print("Добрый день")
else: print("Добрый вечер")
print("Parking Manager CLI version %s"%VERSION)
print("By WeeScottishPuffin")
time.sleep(3)

def sf(car):return car.getLisencePlate()
CARS.sort(key=sf)

def clear():
	if platform in ["linux","linux2","darwin"]:
		# shell or zsh (I don't judge)
		os.system("clear")
	elif platform in ["win32","cygwin"]:
		# msdos
		os.system("cls")

def menu():
	choice=""
	while choice not in ["1","2","q"]:
		clear()
		print('''1) View cars
2) View Garages
q) Quit''')
		choice=input("> ").lower()
	match choice:
		case "1":
			carview()
		case "2":
			garageview()
		case "q":
			print("До свидания!")
			time.sleep(2)
			quit()  
       

def carview():
	choice=""
	while choice not in ["1","2","3"]:
		clear()
		print("Total unparked cars instanced: %s"%len(CARS))
		print('''1) List cars
2) Select car
3) Back''')
		choice=input("> ")
	match choice:
		case "1":
			clear()
			print("PLATE","MODEL","BRAND","COLOUR",sep=10*" ")
			for car in CARS:
				pla,mod,bra,col=car.getLisencePlate()[:14],car.getModel()[:14],car.getBrand()[:14],car.getColour()[:15]
				print(pla,(15-len(pla))*" ",mod,(15-len(mod))*" ",bra,(15-len(bra))*" ",col,sep="")
			print("--%s TOTAL --"%len(CARS))
			print("Press ENTER to return to menu")
			input()
			carview()
		case "2":
			print("Lisence plate?")
			plate=input("> ").upper()
			selectedCar=None
			for car in CARS:
				if car.getLisencePlate().upper() == plate:
					selectedCar = car
			if selectedCar:
				carinfo(selectedCar)
			else:
				print("Unable to find car!")
				time.sleep(2)
				carview()
		case "3":
			menu()

def carinfo(car):
	choice=""
	while choice not in ["1","2"]:
		clear()
		print("PLATE:    %s"%car.getLisencePlate())
		print("MODEL:    %s"%car.getModel())
		print("BRAND:    %s"%car.getBrand())
		print("COLOUR:   %s\n"%car.getColour())
		print("ACTIONS:")
		print('''1) Park car
2) Back''')
		choice=input("> ")
	match choice:
		case "1":
			garageChoice=-1
			while garageChoice not in gdict.keys():
				print("Which garage? (0-%s, c to cancel)"%max(gdict.keys()))
				garageChoice = input(" >").lower()
				if garageChoice == "c": carinfo(car)
				try: garageChoice = int(garageChoice)
				except: garageChoice = -1
			if gdict[garageChoice].parkCar(car,interface.lisenceList[car]): 
				print("Parked car in garage with ID: %s"%garageChoice)
				CARS.remove(car)
			else: 
				print("Unable to park car in garage with ID: %s"%garageChoice)

		case "2":
			carview()
if __name__ == "__main__":
  menu()