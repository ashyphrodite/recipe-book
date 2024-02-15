'''
Recipe Book Functions
'''

from lib import supply
from lib import supplier
from lib import log
from lib import misc
import random			# for generating random shift for cyper every time


# save recipes dictionary data to file 
def storeRecipes(recipes_dict):
	# for each recipe, its data will be stored in the file as:
		# <recipe name>
		# <recipe description>
		# <number of ingredients>
		# for each ingredient, its data will be stored as
			# <item name>
			# <amount>

	# open recipes file for writing
	with open('savefiles/recipe.txt', 'w') as f_ptr:
		# generate random cypher shift and write it to file before the recipes
		shift = random.randint(0, 26)
		f_ptr.write(str(shift) + "\n")
		
		# get number of recipes in the dictionary, cypher, then write it to file
		num = len(recipes_dict)
		f_ptr.write(misc.cypher(str(num), shift) + "\n")

		# for each recipe in the recipes dictionary...
		for recipe, value in recipes_dict.items():
			# cypher then write to file: <recipe name> <newline>
			f_ptr.write(misc.cypher(recipe, shift) + "\n")

			# cypher then write to file: <recipe description> <newline>
			f_ptr.write(misc.cypher(value[0], shift) + "\n")
			
			# cypher then write to file: <number of ingredients> <newline>
			f_ptr.write(misc.cypher(str(len(value[1])), shift) + "\n")

			# for each ingredient
			for item, amount in value[1].items():
				# write to file: <item name> <newline>
				f_ptr.write(misc.cypher(item, shift) + "\n")

				# write to file: <amount> <newline>
				f_ptr.write(misc.cypher(str(amount), shift) + "\n")


# retrieve data from file
def getRecipes():
	# open recipes file for reading
	with open('savefiles/recipe.txt', 'r') as f_ptr:
		# first line is the cypher shift
		shift = int(f_ptr.readline())

		# second line is the number of recipes
		num = int(misc.decypher(f_ptr.readline(), shift))

		# initialize empty dictionary for recipes
		recipes_dict = {}

		# loop num times
		for i in range(num):
			name = misc.decypher(f_ptr.readline()[:-1], shift)
			desc = misc.decypher(f_ptr.readline()[:-1], shift)

			# add entry to recipes dictionaries with name as key and
			# a list containing description and empty dictionary (for ingredients) as value
			recipes_dict[name] = [desc, {}]

			# the number after description is the amount of items for ingredients
			num_items = int(misc.decypher(f_ptr.readline(), shift))

			# repeat num_item times
			for j in range(num_items):
				item = misc.decypher(f_ptr.readline()[:-1], shift)
				amount = int(misc.decypher(f_ptr.readline(), shift))

				# add entry to ingredients dcitionary with item as key and amount as value
				recipes_dict[name][1][item] = amount

	return recipes_dict		# return the recipes dictionary


# input recipe name, and its description and ingredientsS
def addRecipe(dict_li):
	misc.printTitle("RECIPE BOOK: Add Recipe")
	
	# input name and description. loop until valid input name
	while True:
		name = input("  Enter recipe name: ")

		if name != "":
			break
		else:
			print("  Enter valid recipe name!")

	desc = input("  Enter recipe description: ")

	# add entry to recipe dictionaries with name as key and a list containing description and empty dictionary as value
	dict_li[0][name] = [desc, {}]

	# log adding recipe
	log.addLog(dict_li[3], "Added " + name + " to recipes.")

	# loop until no more ingredients to be added
	while True:
		misc.printTitle("RECIPE BOOK: Add Recipe - " + name)		# add the recipe name

		item = misc.validInputLoop("  Enter item name: ", "  Enter valid item name!", "")
		
		# loop until valid input
		while True:
			amount = input("  Enter amount: ")

			if misc.isPositiveInt(amount):
				amount = int(amount)
				break
			else:
				print("  Enter valid input (positive integer)!")	
		
		# add item to ingredients dictionary of recipes dictionary
		dict_li[0][name][1][item] = amount			# dict_li[0][name][1]: ingredients dictionary

		# if the item is not in the supplies dictionary, call addSupply() from supply
		if item not in dict_li[1]:
			print("\n\n ", item, "is not in the supplies record yet!")
			input("  Press Enter key to continue and add it...")	# artificial pause

			dict_li = supply.addSupply(dict_li, item)
		
		# ask to input another ingredient or quit then break from the main loop if want to quit
		print("\n  READ: Add another ingredient to", name, "(n to quit)? ", end="")
		ch = input()
		if ch == 'n' or ch == 'N':
			break

	return dict_li


# input recipe name and delete if it exists
def deleteRecipe(dict_li):
	misc.printTitle("RECIPE BOOK: Delete Recipe")
	# input recipe name. if it doesn't exist print an error
	name = input("  Enter recipe name (case-sensitive): ")
	if name not in dict_li[0]:
		print("  ", name, "is not an existing recipe!\n\n")
		input("  Press Enter key to continue...")		# artificial pause
		return dict_li
	
	# delete entry and print delete message
	del dict_li[0][name]
	print("\n ", name, "deleted! ")
	input("  Press Enter key to continue...")

	# log deleting recipe
	log.addLog(dict_li[3], "Deleted " + name + " from recipes.")

	return dict_li


# delete all recipes
def deleteAllRecipes(dict_li):
	misc.printTitle("RECIPE BOOK: Delete All Recipes")

	# print confirmation warning and input confirmation from user
	print("  This action can't be reversed! Enter DELETE to confirm.")
	ch = input("  Confirm: ")
	print("\n")

	if ch == "DELETE":
		# log deleting recipes
		log.addLog(dict_li[3], "Deleted all recipes.")
		for supplier in dict_li[0]:
			log.addLog(dict_li[3], "Deleted " + supplier + ".", True)

		dict_li[0] = {}
		input("  All recipes have been deleted! Press Enter key to continue...")	# artificial pause
	else:
		input("  Recipes were NOT deleted. Press Enter key to continue...")			# artificial pause
	
	return dict_li


# input recipe name, then print its description and its ingredients (with supplier's name and contact)
def viewRecipe(dict_li):
	misc.printTitle("RECIPE BOOK: View Recipe")

	# input recipe name, print an error if it doesn't exist
	name = input("  Enter recipe name (case-sensitive): ")
	if name not in dict_li[0]:
		print(" ", name, "is not an existing recipe!\n\n")
		input("  Press Enter key to continue...")		# artificial pause
		return dict_li

	# print the recipe name, its description and ingredients
	print("\n ", name)
	print("  +--", dict_li[0][name][0])
	print("  `-- Ingredients:")
	
	missing_item = []
	missing_supp = []

	# print the details for each ingredient
	for item, amount in dict_li[0][name][1].items():
		print("      +--", item)
		print("      |   +-- Amount:", amount)

		# if item is not in supplies dictionary (deleted)
		# then add the item to missing list and skip supplier
		if item not in dict_li[1]:
			missing_item += [item]
			continue

		supp = dict_li[1][item][2]
		print("      |   +-- Supplier:", supp)

		# if supplier is not in suppliers dictionary (deleted)
		# then add item to missing list and skip contact
		if supp not in dict_li[2]:
			missing_supp += [supp]
			continue

		print("      |   `-- Supplier's Contact:", dict_li[2][supp])
	
	# for each missing item, call addSupply() from supply
	for item in missing_item:
		print("\n\n ", item, "is not in supplies record (deleted)!")
		input("  Press Enter key to continue and add it...")

		dict_li = supply.addSupply(dict_li, item)
	
	# for each missing supplier, call addSupplier() from supplier
	for supp in missing_supp:
		print("\n ", supp, "is not in suppliers record (deleted)!")
		input("  Press Enter key to continue and add it...")

		dict_li = supplier.addSupplier(dict_li, supp)
	
	input("\n\n  Press Enter key to continue...")		# artificial pause

	return dict_li


# view recipe list
def viewAllRecipes(dict_li):
	misc.printTitle("RECIPE BOOK: View All Recipes")

	print("  Recipe List")

	# recipe name and description of eac recipe in recipes dictionary
	for recipe, value in dict_li[0].items():
		print("  +--", recipe)
		print("  |   `", value[0])
	
	input("\n\n  Press Enter key to continue...")		# artificial pause


# execute recipe
def executeRecipe(dict_li):
	misc.printTitle("RECIPE BOOK: Execute Recipe")

	# input recipe name, print an error if it doesn't exist
	name = input("  Enter recipe name to execute (case-sensitive): ")
	if name not in dict_li[0]:
		print(" ", name, "is not an existing recipe!\n\n")
		input("  Press Enter key to continue...")		# artificial pause
		return dict_li
	
	# print name and ingredients
	print("\n ", name)
	print("  +--", dict_li[0][name][0])
	print("  `-- Ingredients:")
	
	# for each item, print its amount and name
	for item, amount in dict_li[0][name][1].items():
		print("      +--", amount, item)
	
	print("\n  [1] Done")
	print("  [2] Cancel\n")

	# get choice from user, loop until valid choice
	while True:
		choice = input("  Enter choice: ")

		if choice == '1' or choice == '2':
			break
		else:
			print("  Enter valid choice!")
	
	# if chosen to execute...
	if choice == '1':
		lack_items = []				# empty list for list of lacking items

		# for each item, check if sufficient. add to list if not
		for item, amount in dict_li[0][name][1].items():
			if item not in dict_li[1]:
				lack_items += [item]
				continue

			stock = dict_li[1][item][0]

			if stock - amount < 0:
				lack_items += [item]
		
		# if the lacking items list is not empty, print error and list of such items
		if len(lack_items) > 0:
			print("\n  The recipe was unsucessful.")

			for item in lack_items:
				print("  -", item, "is insufficient")
			input("\n  Press Enter key to continue...")
			
			return dict_li
		
		# log executing recipe
		log.addLog(dict_li[3], "Executed " + name + ".")

		# for each ingredient, decrease amount in stock
		for item, amount in dict_li[0][name][1].items():
			# log using items
			log.addLog(dict_li[3], "Used " + str(amount) + " " + item + ". Stock down to " + str(dict_li[1][item][0] - amount) + ".", True)

			dict_li[1][item][0] -= amount

			# delete item from supplies record if <= 0
			if dict_li[1][item][0] <= 0:
				# log automatically deleting item 
				log.addLog(dict_li[3], "Depleted " + item + ". Automatically deleted from supplies.", True)
				
				del dict_li[1][item]
		
		input("\n  Recipe done!\n  Press Enter key to continue...")
	
	# if chosen to execute, print the cancel message
	if choice == '2': 
		print("\n  You cancelled.")
		input("  Press Enter key to continue...")
	
	return dict_li


# back to main menu, save to files
def backToMain(dict_li):
	storeRecipes(dict_li[0])
	supply.storeSupplies(dict_li[1])
	supplier.storeSuppliers(dict_li[2])
	log.storeLogs(dict_li[3])


# prints the recipe book menu, call printMenu() from misc and return choice-
def recipeBookMenu():
	misc.printTitle("RECIPE BOOK")

	# store menu options into the list for organization purposes
	menu = {
		'1': "Add Recipe",
		'2': "Delete Recipe",
		'3': "Delete All Recipes",
		'4': "View Recipe",
		'5': "View All Recipes",
		'6': "Execute Recipe",
		'0': "Save and Return to Main Menu"
	}

	return misc.printMenu(menu)


# recipe book menu loop
def recipeBookLoop(dict_li):
	while True:
		recipe_book_choice = recipeBookMenu()

		if recipe_book_choice == '1':
			dict_li = addRecipe(dict_li)
		elif recipe_book_choice == '2':
			dict_li = deleteRecipe(dict_li)
		elif recipe_book_choice == '3':
			dict_li = deleteAllRecipes(dict_li)
		elif recipe_book_choice == '4':
			dict_li = viewRecipe(dict_li)
		elif recipe_book_choice == '5':
			viewAllRecipes(dict_li)
		elif recipe_book_choice == '6':
			dict_li = executeRecipe(dict_li)
		else:
			backToMain(dict_li)
			return dict_li
