########################################################################
#
#                            I M P O R T S
#
########################################################################
import time
import datetime
import threading
import copy
import re
import json
import os

import log

########################################################################
#
#           E N V I R O N M E N T    V A R I A B L E S
#
########################################################################

#default values for environment variables
ES_EVAL_PERIOD_DEFAULT = 3						#check scheduling rules every 3 seconds



#set environment-based variables
rule_eval_period = os.getenv("ES_EVAL_PERIOD", ES_EVAL_PERIOD_DEFAULT)
rules_file_path = os.getenv("ES_RULES_PATH", ES_RULES_PATH_DEFAULT)


########################################################################
#
#                 G L O B A L    V A R I A B L E S
#
########################################################################



#rule registry
rule_registry = dict()


#rule registry changed flag
rule_registry_changed = False

########################################################################
#
#                        C O N S T A N T S
#
########################################################################

#rule scheduling types


#time period the rule is active
RULE_VALIDITY_NOT_BEFORE			= 0
RULE_VALIDITY_NOT_AFTER				= 1

#number of times rule can be executed
RULE_EXECUTION_LIMIT_FOREVER		= -1
RULE_EXECUTION_LIMIT_EXPIRED		=  0
RULE_EXECUTION_LIMIT_ONCE			=  1
RULE_EXECUTION_LIMIT_COUNTER		=  2

#when the rule is executed
RULE_TRIGGER_EXTERNAL				= 0
RULE_TRIGGER_DATETIME				= 1
RULE_TRIGGER_PERIODIC				= 2

########################################################################
#
#                 I N I T I A L I Z A T I O N S
#
########################################################################


log.setLogLevel(log.LOG_DEBUG)


########################################################################
#
#                U T I L I T Y    F U N C T I O N S
#
########################################################################
def log(level, message):

	print "(LOG): 
	
	
########################################################################
#
#                        F U N C T I O N S
#
########################################################################

def periodicScheduler():

	#log eval start
	log.log(log.LOG_DEBUG, "Scheduling event occured.") 
	
	#schedule function invocation upon period expiration
	threading.Timer(rule_eval_period, periodicScheduler).start()

	#if the registry was changed, save it to the file
	if rule_registry_changed == True:
		saveRegistry()
		
	#perform schedule rule evaluation
	evaluateRules()
	
	#clean expired rules
	purgeRules()



def evaluateRules():

	#create snapshot of the curent registry status for thread-safe iteration
	safe_registry = copy.deepcopy(rule_registry)
	
	#iterate over rule registry
	
	pass
	
	
	
	
def setRule(user, name, selector, not_before=None, not_after=None, exec_limit=None, 
	trigger_ext=None, trigger_datetime=None, trigger_periodic=None):


	#check arguments sanity
	if user == None or name == None or selector == None:
		return False
	
	#new rule definition
	rdef = dict()
	
	#set rule name
	rdef["name"] = name
	
	#set docker image selector as precompiled regex
	regex = re.compile(selector)
	rdef["selector"] = regex
	
	#set the timeline this rule is valid
	rdef["time-validity"] = dict()
	rdef["time-validity"]["not-before"] = not_before
	rdef["time-validity"]["not-after"] = not_after
	
	#set execution limit for this rule
	rdef["exec-limit"] = exec_limit
	
	#set trigger types
	rdef["triggers"] = dict()
	rdef["triggers"]["trigger-external"] = trigger_ext
	rdef["triggers"]["trigger-datetime"] = trigger_datetime
	rdef["triggers"]["trigger-periodic"] = trigger_periodic
	
	#add rule to rule registry
	rule_registry[user] = rule_definition
	
	#return success
	return True
	
	
def deleteRule(user, name):

	try:
		#get rules for user 
		rules = rule_registry[user]
		
		#delete the rule with the give name
		del rules[name]

	except KeyError: 
		log.log(log.LOG_DEBUG, "Error deleting rule " + name + " for user " + user) 
		return False
	
	return True
	
	
	
	
def getRule(user, name):

	try:
		#get rules for user 
		rules = rule_registry[user]
		
		#return the rule with the give name
		return json.dumps(rules[name])

	except KeyError: 
		log.log(log.LOG_DEBUG, "Error retrieving rule " + name + " for user " + user) 
		return None
	
	

def getRules(user):

	try:
		#get rules for user 
		rules = rule_registry[user]
		
		#return all rules
		return json.dumps(rules)

	except KeyError: 
		log.log(log.LOG_DEBUG, "Error retrieving all rules for user " + user) 
		return None



def saveRegistry():

	global rule_registry_changed
	
	#create snapshot of the curent registry status for thread-safe iteration
	safe_registry = copy.deepcopy(rule_registry)

	#rename original rules file (backup)
	try:
      os.rename(rules_file_path,  rules_file_path + "~")
	 except IOError:
		log.log(log.LOG_WARNING, "Failed to rename rules file for backup to: " + rules_file_path + "~")
	
	 #save new rules file
	 try:
        with open(rules_file_path, 'w') as outfile:
			json.dump(safe_registry, outfile, sort_keys=True, indent=2, separators=(",", ": "))
		rule_registry_changed = False
        log.log(log.LOG_DEBUG, "Saved new rules data to " + rules_file_path)
      except IOError:
      	log.log(log.LOG_WARNING, "Failed to save rules data to file "  + rules_file_path)
      	return False
	
    return True
	
	
	
def loadRegistry():

	global rule_registry
	
	try:
		with open(rules_file_path) as rules_file:
			rules_data = json.load(rules_file)
		rule_registry = rules_data
    	log.log(log.LOG_DEBUG, "Loaded rules data from " + rules_file_path)
	except IOError:
		log.log(log.LOG_WARNING, "Falied to load rules data from " + rules_file_path)

	return True


########################################################################
#
#                 I N I T I A L I Z A T I O N
#
########################################################################

#start scheduling thread
periodicScheduler()




