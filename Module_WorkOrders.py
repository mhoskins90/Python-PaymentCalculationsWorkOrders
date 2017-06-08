import framework as framework
import Module_Utilities as utilities

class AbstractWorkOrderFactory():
	def make_work_order_kitchen(self): 
		pass
	def make_work_order_bedroom(self): 
		pass

class WorkOrderFactory(AbstractWorkOrderFactory, metaclass=framework.Singleton):
	def select(self, type):
		if type.lower()=="bedroom":
			return WorkOrderBedroom()
		elif type.lower()=='kitchen':
			return WorkOrderKitchen()
		else:
			print('Error, wrong payment type entered.')
	def make_work_order_kitchen(self): 
		pass
	def make_work_order_bedroom(self): 
		pass

class WorkOrderBedroom():
	def __init__(self):
		self.final_work_order_list = []
		#self.mediator = mediator

	def ask_work_order_questions(self):
		QuestionInputValidation = framework.QuestionInputValidation()
		'''
		METHOD WILL ASK ALL QUESTIONS FOR WORK ORDER DATA ENTRY
		QUESTIONS WILL INCLUDE:
		UNIT NUMBER, DESCRIPTION OF ISSUE, POTENTIALLY ALSO STATUS (OPEN OR CLOSED)
		'''
		continue_asking_work_order_questions = "yes"
		valid = "Y"
		while continue_asking_work_order_questions.lower() == "y" or continue_asking_work_order_questions.lower() == "yes":
			dict_of_answers = {'unit_number': '', 'issue': '','type': 'Bedroom'}
			while True:
				self.unit_number = input("Please enter the appropriate unit number:  ")
				if QuestionInputValidation.validate_integer(self.unit_number) == "bad":
					continue
				self.unit_number = QuestionInputValidation.validate_integer(self.unit_number)

				dict_of_answers['unit_number'] = self.unit_number
				break
			while True:
				self.issue = input("Please enter a brief description of the issue:  ")
				if QuestionInputValidation.validate_string_length(self.issue) == "bad":
					continue
				self.issue = QuestionInputValidation.validate_string_length(self.issue)
				dict_of_answers['issue'] = self.issue
				break
			
			self.final_work_order_list.append(dict_of_answers)

			continue_asking_work_order_questions = input("Continue entering Work Orders? (Y) Yes | Enter any other key to stop:  ")
			if continue_asking_work_order_questions.lower() != "y" and continue_asking_work_order_questions.lower() != "yes":
				valid ="Y"
				break
			else:
				valid ="Y"
				mediator = utilities.ConcreteMediator()
				mediator.WorkOrderStorage.store(self.final_work_order_list)
				continue

class WorkOrderKitchen():
	def __init__(self):
		self.final_work_order_list = []

	def ask_work_order_questions(self):
		QuestionInputValidation = framework.QuestionInputValidation()
		'''
		METHOD WILL ASK ALL QUESTIONS FOR WORK ORDER DATA ENTRY
		QUESTIONS WILL INCLUDE:
		UNIT NUMBER, DESCRIPTION OF ISSUE, POTENTIALLY ALSO STATUS (OPEN OR CLOSED)

		'''
		continue_asking_work_order_questions = "yes"
		valid = "Y"
		while continue_asking_work_order_questions.lower() == "y" or continue_asking_work_order_questions.lower() == "yes":
			dict_of_answers = {'unit_number': '', 'issue': '','type': 'Kitchen'}
			while True:
				self.unit_number = input("Please enter the appropriate unit number:  ")
				if QuestionInputValidation.validate_integer(self.unit_number) == "bad":#PASSED BY MEDIATOR
					continue
				self.unit_number = QuestionInputValidation.validate_integer(self.unit_number)#PASSED BY MEDIATOR

				dict_of_answers['unit_number'] = self.unit_number
				break
			while True:
				self.issue = input("Please enter a brief description of the issue:  ")
				if QuestionInputValidation.validate_string_length(self.issue) == "bad":#PASSED BY MEDIATOR
					continue
				self.issue = QuestionInputValidation.validate_string_length(self.issue)#PASSED BY MEDIATOR
				dict_of_answers['issue'] = self.issue
				break
			
			self.final_work_order_list.append(dict_of_answers)#THIS ALLOWS FOR MULTPLE ENTRIES

			continue_asking_work_order_questions = input("Continue entering Work Orders? (Y) Yes | Enter any other key to stop:  ")
			if continue_asking_work_order_questions.lower() != "y" and continue_asking_work_order_questions.lower() != "yes":
				valid ="Y"
				break
			else:
				valid ="Y"
				mediator = utilities.ConcreteMediator()
				mediator.WorkOrderStorage.store(self.final_work_order_list)
				continue

class WorkOrderManager():
	def make_work_order(self):
		return WorkOrderFactory()

class WorkOrderOutput(utilities.GenericOutput):
	def __init__(self):
		pass
		
class WorkOrderDetermine(WorkOrderOutput):
	def __init__(self, mediator):
		self.mediator = mediator

	def determine(self):
		'''
		METHOD WILL DETERMINE ENTERED WORK ORDERS
		'''
		results = self.mediator.dbHandler.query("SELECT * FROM workOrders")
		selected = results.fetchall()
		return selected
	def display(self, tuple_to_display):
		'''
		METHOD WILL DISPLAY WORK ORDER ENTRIES
		'''
		if len(tuple_to_display) < 1:
			print("\nSorry, no work order entries.")
		else:
			for row in tuple_to_display:#0,1,2,3,4
				
				print("{0}: ({1}) Unit {2} has a {4} in the {3}. ".format(row[0], row[1], row[2], row[3], row[4]))	


class WorkOrderStorage(WorkOrderOutput):
	def __init__(self, mediator):
		self.mediator = mediator

	def delete(self,item_to_delete):
		'''
		METHOD WILL DELETE WORK ORDER ENTRIES
		'''
		query = 'DELETE FROM workOrders WHERE workOrderID ={0}'.format(item_to_delete)
		self.mediator.dbHandler.query(query)
		if self.mediator.dbHandler.cursor.rowcount == 0:
			return 'No rows deleted, incorrect entry.'
		else:
			return 'Row Deleted'

	def store(self, entered_data):
		'''
		METHOD WILL STORE WORK ORDER ENTRIES
		'''
		for dictionary in entered_data:
			unit_number = dictionary['unit_number']
			type = dictionary['type']
			issue = dictionary['issue']

			query = 'INSERT INTO workOrders (workOrderID, entry_date, unitNumber, type, issue)VALUES (null,CURRENT_DATE,{0},"{1}","{2}")'.format(unit_number, type, issue)
			#print(query)#TESTING
		#self.dbHandler.query('"INSERT INTO workOrders (workOrderID, entry_date, unitNumber, type, issue)VALUES (?,?,?,?,?)",(1,2,3,4,5)')#ISSUE BECAUSE IT LOOKS LIKE MULTIPLE ARUGMENTS
		self.mediator.dbHandler.query(query)
		print('\n------Entry has been saved in DB.------\n')		