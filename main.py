'''
Made by Ronaldo D. Dimaano Jr.
Section B4-L

This program simulates a Recipe Book with an inventory system.
The inventory system includes items, amount on stock, price,
and the items' suppliers and contact information. The recipe book 
also allows to execute recipe which will update the state of 
the items on stock accordingly.
'''

from lib import recipe
from lib import supply
from lib import supplier
from lib import log
from lib import misc


# the dictionaries will be stored in a list
# dict_list[0]: recipes dictionary
# dict_list[1]: supplies dictionary
# dict_list[2]: suppliers dictionary
# dict_list[3]: logs dictionary
dict_list = []

# functions to execute at the start of the program
def initialize():
	misc.checkFiles()
	misc.changeColor("0a")						# 0c: 0 = black bg, c = light green text


# execute upon exiting program
def exitProgram():
	misc.changeColor("07")						# 0c: 0 = black bg, 7 = white text

	misc.printTitle("GOODBYE!")


# prints the main menu, call printMenu() from misc and return choice
def mainMenu():
	misc.printTitle("MAIN MENU")

	# store menu options into the list for organization purposes
	menu = {
		'1': "Enter Recipe Book",
		'2': "Enter Supplies Record",
		'3': "Enter Suppliers Record",
		'4': "View Logs",
		'0': "Save and Exit"
	}

	return misc.printMenu(menu)


# main loop of the program
def mainLoop():
	global dict_list

	# loop until user chooses to exit
	while True:
		main_menu_choice = mainMenu()
	
		if main_menu_choice == '1':
			dict_list = recipe.recipeBookLoop(dict_list)
		elif main_menu_choice == '2':
			dict_list = supply.supplyLoop(dict_list)
		elif main_menu_choice == '3':
			dict_list = supplier.supplierLoop(dict_list)
		elif main_menu_choice == '4':
			dict_list = log.logsLoop(dict_list)
		else:
			exitProgram()
			break


# main function of the script
def main():
	initialize()
	
	# get data from save files
	global dict_list	
	dict_list = misc.getData()

	mainLoop()
	

# execute main() is the script is being ran
if __name__ == "__main__":
	main()