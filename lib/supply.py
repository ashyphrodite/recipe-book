'''
Functions for Supply Records
'''

from lib import recipe
from lib import supplier
from lib import log
from lib import misc
import random			# for generating random shift for cyper every time


# save supply dictionary data to file
def storeSupplies(supplies_dict):
	# for each item, its data will be stored in the file as:
		# <item name>
		# <stock amount>
		# <price>
		# <supplier's name>

	# open supplies file for writing
	with open('savefiles/supply.txt', 'w') as f_ptr:
		# generate random cypher shift and write it to file before the items
		shift = random.randint(0, 26)
		f_ptr.write(str(shift) + "\n")

		# get number of items in the dictionary, cypher, then write to file
		num = len(supplies_dict)
		f_ptr.write(misc.cypher(str(num), shift) + "\n")
		
		# for each item in the supplies dictionary...
		for item, value in supplies_dict.items():
			# cypher then write to file: <item name> <newline>
			f_ptr.write(misc.cypher(item, shift) + "\n")

			# cypher then write to file: <stock amount> <newline>
			f_ptr.write(misc.cypher(str(value[0]), shift) + "\n")

			# cypher then write to file: <price> <newline>
			f_ptr.write(misc.cypher(str(value[1]), shift) + "\n")

			# cypher then write to file: <supplier's name> <newline>
			f_ptr.write(misc.cypher(value[2], shift) + "\n")


# retrieve data from file
def getSupplies():
	# open supplies file for reading
	with open('savefiles/supply.txt', 'r') as f_ptr:
		# first line is the cypher shift
		shift = int(f_ptr.readline())

		# second line is the number of items
		num = int(misc.decypher(f_ptr.readline(), shift))

		# initialize an empty dictionary for supplies
		supplies_dict = {}

		# repeat num times
		for i in range(num):
			name = misc.decypher(f_ptr.readline()[:-1], shift)
			amount = int(misc.decypher(f_ptr.readline(), shift))
			price = float(misc.decypher(f_ptr.readline(), shift))
			supplier = misc.decypher(f_ptr.readline()[:-1], shift)
		
			# add entry to dictionary with item name as key and
			# and a list containing the stock amount, price, and supplier as value
			supplies_dict[name] = [amount, price, supplier]
		
		f_ptr.close()			# close the file
	
	return supplies_dict	# return the supplies dictionary


# add an item to record, including its stock and price, and the supplier
# if supplier does not exist, call addSupplier() from supplier
def addSupply(dict_li, name=None):
	misc.printTitle("SUPPLY RECORDS: Add Record")

	# if name is not None, then it is called from recipe
	if name:
		print("  Item:", name, "\n")
	else:
		name = misc.validInputLoop("  Enter item name: ", "  Enter valid item name!", "")
	
	# if item exists, then only input amount to add to stock. loop until valid input
	if name in dict_li[1]:
		while True:
			stock = input("  Enter amount to add: ")

			if misc.isPositiveInt(stock):
				stock = int(stock)
				break
			else:
				print("  Enter valid input (positive integer)!")
		
		# log adding amount of stock
		log.addLog(dict_li[3], "Added " + str(stock) + " to " + name + " stock.")
		
		dict_li[1][name][0] += stock
		return dict_li

	# log adding an item
	log.addLog(dict_li[3], "Added " + name + " to supplies.")

	# input amount of stock. loop until valid input
	while True:
		stock = input("  Enter stock: ")

		if misc.isPositiveInt(stock):
			stock = int(stock)

			# log setting item stock
			log.addLog(dict_li[3], "Added " + str(stock) + " to " + name + " stock.", True)

			break
		else:
			print("  Enter valid input (positive integer)!")
	
	# input item price. loop until valid input
	while True:
		price = input("  Enter price: ")

		if misc.isNonNegativeFloat(price):
			price = float(price)
			break
		else:
			print("  Enter valid price (positive number)!")

	# input supplier
	supp = input("  Enter associated supplier: ")

	# add entry to supplies dictionary with name as key and stock, price, supplier in a list as value
	dict_li[1][name] = [stock, price, supp]

	# if supplier does not exists, call addSupplier() from supplier
	if supp not in dict_li[2]:
		print("\n ", supp, "is not in the suppliers record yet!")
		input("  Press Enter key to continue and add it...")

		dict_li = supplier.addSupplier(dict_li, supp)

	return dict_li


# input item name and delete if it exists
def deleteSupply(dict_li):
	misc.printTitle("SUPPLY RECORDS: Delete Record")

	name = input("  Enter item name (case-sensitive): ")
	if name not in dict_li[1]:
		print(" ", name, "does not exist!\n\n")
		input("  Press Enter key to continue...")			# artificial pause
		return dict_li
	
	del dict_li[1][name]		# delete entry
	print("\n ", name, "deleted!")
	input("  Press Enter key to continue...")				# artificial pause

	# log deleting item
	log.addLog(dict_li[3], "Deleted " + name + " from supplies.")

	return dict_li


# deletes all supplies, just an empty dictionary
def deleteAllSupplies(dict_li):
	misc.printTitle("SUPPLY RECORDS: Delete All Records")

	# print confirmation warning and input confirmation from user
	print("  This action can't be reversed! Enter DELETE to confirm.")
	ch = input("  Confirm: ")
	print("\n")

	if ch == "DELETE":
		# log deleting supplies
		log.addLog(dict_li[3], "Deleted all                 supplies.")
		for supply in dict_li[1]:
			log.addLog(dict_li[3], "Deleted " + supply + ".", True)

		dict_li[1] = {}
		input("  All records have been deleted!\n  Press Enter key to continue...")		# artificial pause	
	else:
		input("  Records were NOT deleted.\n  Press Enter key to continue...")			# artificial pause
	
	return dict_li


# view all items and their details
def viewSupplies(dict_li):
	misc.printTitle("SUPPLIER RECORDS: View Record")

	# for each item, print its details
	for item, value in dict_li[1].copy().items():
		# delete item from dictionary if out of stock. then continue
		if value[0] <= 0:
			del dict_li[1][item]
			continue

		print("  +--", item)
		print("  |   +-- Stock:", value[0])
		print("  |   +-- Price: " + str(value[1]))
		print("  |   `-- Supplier:", value[2])

	input("\n\n  Press Enter key to continue...")		# artificial pause


# back to main menu, save to files
def backToMain(dict_li):
	recipe.storeRecipes(dict_li[0])
	storeSupplies(dict_li[1])
	supplier.storeSuppliers(dict_li[2])
	log.storeLogs(dict_li[3])


# prints the supply records menu, call printMenu() from misc and return choice
def supplyMenu():
	misc.printTitle("SUPPLY RECORDS")

	# store menu options into the list for organization purposes
	menu = {
		'1': "Add Record",
		'2': "Delete Record",
		'3': "Delete All Records",
		'4': "View Record",
		'0': "Save and Return to Main Menu"
	}

	return misc.printMenu(menu)


# supply records menu loop
def supplyLoop(dict_li):
	while True:
		supply_menu_choice = supplyMenu()

		if supply_menu_choice == '1':
			dict_li = addSupply(dict_li)
		elif supply_menu_choice == '2':
			dict_li = deleteSupply(dict_li)
		elif supply_menu_choice == '3':
			dict_li = deleteAllSupplies(dict_li)
		elif supply_menu_choice == '4':
			viewSupplies(dict_li)
		else:
			backToMain(dict_li)
			return dict_li