import json

def readExperiencesFile(fileName="experiences.json"):

	with open(fileName, 'r') as file:
		experiences = json.load(file)

	return experiences # list of lists, each list is an experience tuple