'''
Functions for Supplier Records
'''

from lib import recipe
from lib import supply
from lib import log
from lib import misc
import random			# for generating random shift for cyper every time


# save to file
def storeSuppliers(suppliers_dict):
	# for each supplier, its data will be stored in the file as:
		# <supplier's name>
		# <supplier's comtact information>

	# open suppliers file for writing
	with open('savefiles/supplier.txt', 'w') as f_ptr:
		# generate random cypher shift and write it to file before the supliers
		shift = random.randint(0, 26)
		f_ptr.write(str(shift) + "\n")

		# get number of suppliers in the dictionary and write to file
		num = len(suppliers_dict)
		f_ptr.write(misc.cypher(str(num), shift) + "\n")

		# for each supplier in the suppliers dictionary...
		for supplier, contact in suppliers_dict.items():
			# cypher then write to file: [n + 1] <space> [supplier's name] <newline>
			f_ptr.write(misc.cypher(supplier, shift) + "\n")

			# cypher then write to file: [n + 2] <space> [supplier's contact information] <newline>
			f_ptr.write(misc.cypher(contact, shift) + "\n")


# retrieve from file
def getSuppliers():
	# open suppliers file for reading
	with open('savefiles/supplier.txt', 'r') as f_ptr:
		# first line is the cypher shift
		shift = int(f_ptr.readline())

		# second line is the number of suppliers
		num = int(misc.decypher(f_ptr.readline(), shift))

		# initialize empty dictionary for suppliers
		suppliers_dict = {}

		for i in range(num):
			name = misc.decypher(f_ptr.readline()[:-1], shift) 
			contact = misc.decypher(f_ptr.readline()[:-1], shift) 

			# add entry to dictionary with supplier's name as key and contact information as value
			suppliers_dict[name] = contact
		
	return suppliers_dict


# input supplier name and contact information
def addSupplier(dict_li, name=None):
	misc.printTitle("SUPLLIER RECORDS: Add Record")

	# if name is not None, then it is called from recipe or supply
	if name:
		print("  Supplier:", name, "\n")
	else:
		name = misc.validInputLoop("  Enter supplier's name: ", "  Enter valid supplier name!", "")
	
	contact = misc.validInputLoop("  Enter supplier's contact information: ", "  Enter valid contact info!", "")

	dict_li[2][name] = contact

	# log adding supplier
	log.addLog(dict_li[3], "Added " + name + " to the supplier list.")

	return dict_li


# input supplier name and delete it if it exists
def deleteSupplier(dict_li):
	misc.printTitle("SUPPLIER RECORDS: Delete Record")

	name = input("  Enter supplier's name (case-sensitive): ")
	if name not in dict_li[2]:
		print(" ", name, "does not exist!\n\n")
		input("  Press Enter key to continue...")		# artificial pause
		return dict_li
	
	del dict_li[2][name]
	print("\n ", name, "deleted!")
	input("  Press Enter key to continue...")			# artificial pause

	# log deleting supplier
	log.addLog(dict_li[3], "Deleted " + name + " from the supplier list.")

	return dict_li


# deletes all supliers, just an empty dictionary
def deleteAllSuppliers(dict_li):
	misc.printTitle("SUPPLIER RECORDS: Delete All Records")

	print("  This action can't be reversed! Enter DELETE to confirm.")
	ch = input("  Confirm: ")
	print("\n")

	if ch == "DELETE":
		# log deleting all suppliers
		log.addLog(dict_li[3], "Deleted all suppliers.")
		for supplier in dict_li[2]:
			log.addLog(dict_li[3], "Deleted " + supplier + ".", True)

		dict_li[2] = {}
		input("  All records have been deleted! Press Enter key to continue...")	# artificial pause
	
	else:
		input("  Records were NOT deleted. Press Enter key to continue...")			# artificial pause
	
	return dict_li
		

# view records
def viewSuppliers(dict_li):
	misc.printTitle("SUPPLIER RECORDS: View Record")

	# for each supplier, print name and contact
	for name, contact in dict_li[2].items():
		print("  +--", name)
		print("  |   `--", contact)

	input("\n\n  Press Enter key to continue...")		# artificial pause


# back to main menu, save to files
def backToMain(dict_li):
	recipe.storeRecipes(dict_li[0])
	supply.storeSupplies(dict_li[1])
	storeSuppliers(dict_li[2])
	log.storeLogs(dict_li[3])


# prints the supplier records menu, call printMenu() from misc and return choice
def supplierMenu():
	misc.printTitle("SUPPLIER RECORDS")

	# store menu options into the list for organization purposes
	menu = {
		'1': "Add Record",
		'2': "Delete Record",
		'3': "Delete All Records",
		'4': "View Record",
		'0': "Save and Return to Main Menu"
	}

	return misc.printMenu(menu)


# supplier records menu loop
def supplierLoop(dict_li):

	while True:
		supplier_menu_choice = supplierMenu()

		if supplier_menu_choice == '1':
			dict_li = addSupplier(dict_li)
		elif supplier_menu_choice == '2':
			dict_li = deleteSupplier(dict_li)
		elif supplier_menu_choice == '3':
			dict_li = deleteAllSuppliers(dict_li)
		elif supplier_menu_choice == '4':
			viewSuppliers(dict_li)
		else:
			backToMain(dict_li)
			return dict_li