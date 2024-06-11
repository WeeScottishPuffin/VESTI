import interactions as interface
import time

VERSION="1.0"
hour = time.gmtime()[3]

if 12 > hour > 6: print("Доброе утро")
elif 18 > hour > 12: print("Добрый день")
else: print("Добрый вечер")
print("Parking Manager CLI version %s\n"%VERSION)

def menu():
  print('''
1) View cars
2) View Garages
  ''')
  