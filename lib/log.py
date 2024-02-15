'''
Functions for Logs
'''

from lib import misc
import random			# for generating random shift for cyper every time


def storeLogs(logs_dict):
	# for each day, the logs record will be stored in the file as:
		# day
		# action
		# action
	
	# open logs file for writing
	with open('savefiles/logs.txt', 'w') as f_ptr:
		# generate 
		shift = random.randint(0, 26)
		f_ptr.write(str(shift) + "\n")

		for day, actions in logs_dict.items():
			f_ptr.write(misc.cypher(day, shift) + "\n")

			for action in actions:
				f_ptr.write(misc.cypher(action, shift) + "\n")


# retrieve data from file
def getLogs():
	# open logs file for reading
	with open('savefiles/logs.txt', 'r') as f_ptr:
		# first line is the cypher shift
		shift = int(f_ptr.readline())

		# initialize empty dictionary for logs
		logs_dict = {}

		# for each line in the file...
		for line in f_ptr.readlines():
			# if the line is enclosed in square brackets, it is day
			if line[0] == '[' and line[-2] == ']':
				date = misc.decypher(line[:-1], shift)
				logs_dict[date] = []
			
			# else it is an action
			else:
				logs_dict[date] += [misc.decypher(line[:-1], shift)]
	
	return logs_dict	# return the logs dictionary


# add log entry to logs dictionary
def addLog(logs_dict, action, list=False):
	date, time = misc.getDateAndTime()

	# if current date is not in the dictionary, add it
	if date not in logs_dict:
		logs_dict[date] = []

	# if it is a list, do not prepend
	if not list:
		logs_dict[date] += [time + " " + action]
	else:
		logs_dict[date] += [" "*8 + "- " + action]


# prints all of the logs
def viewLogs(dict_li):
	misc.printTitle("LOGS: View Logs")

	# print the date for each day
	for date, actions in dict_li[3].items():
		print(" ", date)

		for action in actions:
			print("   ", action)
	
	input("\n\n  Press Enter key to continue...")


# delete all logs
def deleteLogs(dict_li):
	misc.printTitle("LOGS: Delete Logs")

	# print confirmation warning and input confirmation from user
	print("  There really isn't a reason to do this.\n  This action can't be reversed! Enter DELETE to confirm.")
	ch = input("  Confirm: ")
	print("\n")

	if ch == "DELETE":
		dict_li[3] = {}
		input("  All recipes have been deleted! Press Enter key to continue...")	# artificial pause
	else:
		input("  Logs were NOT deleted. Press Enter key to continue...")	
	
	return dict_li


# back to main menu, save the logs
def backToMain(dict_li):
	storeLogs(dict_li[3])	


# prints the logs menu, call printMenu() from misc and return choice
def logsMenu():
	misc.printTitle("LOGS")

	# store menu options into a dictionary for organization
	menu = {
		'1': "View Logs",
		'2': "Delete Logs",
		'0': "Return to Main Menu"
	}

	return misc.printMenu(menu)


def logsLoop(dict_li):
	while True:
		logs_menu_choice = logsMenu()

		if logs_menu_choice == '1':
			viewLogs(dict_li)
		elif logs_menu_choice == '2':
			dict_li = deleteLogs(dict_li)
		else:
			backToMain(dict_li)
			return dict_li