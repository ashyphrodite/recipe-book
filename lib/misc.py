'''
Miscellaneous functions that will be used collectively by the scripts.
'''

from lib import recipe
from lib import supply
from lib import supplier
from lib import log
from datetime import datetime
import os					# used for file checking and screen clearing


title = '''
  ██████╗ ███████╗ █████╗ ██╗██████╗ ███████╗     ██████╗  █████╗  █████╗ ██╗  ██╗
  ██╔══██╗██╔════╝██╔══██╗██║██╔══██╗██╔════╝     ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝
  ██████╔╝█████╗  ██║  ╚═╝██║██████╔╝█████╗       ██████╦╝██║  ██║██║  ██║█████═╝ 
  ██╔══██╗██╔══╝  ██║  ██╗██║██╔═══╝ ██╔══╝       ██╔══██╗██║  ██║██║  ██║██╔═██╗ 
  ██║  ██║███████╗╚█████╔╝██║██║     ███████╗     ██████╦╝╚█████╔╝╚█████╔╝██║ ╚██╗
  ╚═╝  ╚═╝╚══════╝ ╚════╝ ╚═╝╚═╝     ╚══════╝     ╚═════╝  ╚════╝  ╚════╝ ╚═╝  ╚═╝
                       █▄▄ █▄█   █▀█ █▀█ █▄ █ ▄▀█ █   █▀▄ █▀█
                       █▄█  █    █▀▄ █▄█ █ ▀█ █▀█ █▄▄ █▄▀ █▄█'''



# checks if savefile directory and save files exist
# if they don't exist, then make them
# write 0 in one line for cyper and another 0 for number of items
def checkFiles():
	if not os.path.exists('savefiles'):
		os.mkdir('savefiles')
	
	if not os.path.isfile('savefiles/recipe.txt'):
		with open('savefiles/recipe.txt', 'w') as file:
			file.write("0\n0")
	
	if not os.path.isfile('savefiles/supply.txt'):
		with open('savefiles/supply.txt', 'w') as file:
			file.write("0\n0")
	
	if not os.path.isfile('savefiles/supplier.txt'):
		with open('savefiles/supplier.txt', 'w') as file:
			file.write("0\n0")
	
	if not os.path.isfile('savefiles/logs.txt'):
		with open('savefiles/logs.txt', 'w') as file:
			file.write("0\n")


# retrieves data from save files
def getData():
	recipes = recipe.getRecipes()
	supplies = supply.getSupplies()
	suppliers = supplier.getSuppliers()
	logs = log.getLogs()

	return [recipes, supplies, suppliers, logs]


# clears the terminal
def clearScreen():
	if os.name == "nt":
		os.system('cls')		# for nt (Windows)		
	elif os.name == "posix":
		os.system('clear')		# for unix-based systems such as Linux


# change color on Windows terminal
# purely for aesthetic purposes
def changeColor(color):
	if os.name == "nt":
		os.system("color " + color)


# prints the title, then prints the given subtitle (current menu)
def printTitle(subtitle):
	clearScreen()
	# center the subtitle using the string center() method
	subtitle = subtitle.center(84)		# 84 because the title width is 80 + 2 spaces at the start

	print(title, "\n")
	print("  --------------------------------------------------------------------------------")
	print(subtitle)
	print("  --------------------------------------------------------------------------------\n")


# prints menu, then return choice with validation
def printMenu(menu):
	for option, value in menu.items():
		# put the line to a string so it can be centered
		line = ("[" + option + "]" + " " + value).center(84)
		print(line, "\n")
	
	# store all the menu keys into a list to be used for input validation 
	valid_choice = menu.keys()

	# loop until valid choice, prints an error if not
	while True:
		choice = input("  Enter Choice: ")

		if choice not in valid_choice:
			print("  Enter valid choice!")
		else:
			break
	
	return choice


# gets current date and time and return them in a tuple
def getDateAndTime():
	time = datetime.now()

	# return day and time
	return time.strftime("[%m-%d-%Y]"), time.strftime("[%H:%M]")


# loop until valid input
# 1st param: input message, 2nd param - error message; 3rd param - invalid str
def validInputLoop(input_str: str, error_str: str, invalid_str):
	while True:
		_str = input(input_str)

		if _str != invalid_str:
			break
		else:
			print(error_str)
	
	return _str



# checks if string can be int and is > 0 with type checking
def isPositiveInt(n):
	try:
		if int(n) <= 0:
			return False
		return True

	except ValueError:
		return False


# checks if integer can be float and is >= 0 with type checking
def isNonNegativeFloat(n):
	try:
		if float(n) < 0.0:
			return False
		return True

	except ValueError:
		return False


# define character strings for de/cipher outside for efficiency
uchar_str = "abcdefghijklmnopqrstuvwxyz"
lchar_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
num_str = "0123456789."

# checks if character is number (including '.'), lowercase or uppercase letter
# returns "num" if number, "lchar" if lowecase letter, "uchar" if uppercase letter, "other" if anything else
# also returns an integer depending on the character type. return them as a tuple
def charToTypeAndInt(char):
	for i in range(len(uchar_str)):
		if uchar_str[i] == char:
			return "uchar", i
	
	for i in range(len(lchar_str)):
		if lchar_str[i] == char:
			return "lchar", i
	
	for i in range(len(num_str)):
		if num_str[i] == char:
			return "num", i
	
	return "other", 100


# returns a character from int depending on char type (from charToTypeAndInt())
def typeAndIntToChar(ch_type, n):

	if ch_type == "uchar":
		n %= 26
		return uchar_str[n]
	
	if ch_type == "lchar":
		n %= 26
		return lchar_str[n]
	
	if ch_type == "num":
		n %= 11
		return num_str[n]
	
	return 100


# do caesar cypher on string depending on char type (from charToTypeAndInt()) of each character
def cypher(string, shift):
	cyphered = ""

	for char in string:
		ch_type, ch_int = charToTypeAndInt(char)
		
		if ch_type != "other":
			cyphered += typeAndIntToChar(ch_type, ch_int + shift)
		else:
			cyphered += char
	
	return cyphered


# decypher caesar cypher
def decypher(string, shift):
	decyphered = ""

	for char in string:
		ch_type, ch_int = charToTypeAndInt(char)
		
		if ch_type != "other":
			decyphered += typeAndIntToChar(ch_type, ch_int - shift)
		else:
			decyphered += char
	
	return decyphered