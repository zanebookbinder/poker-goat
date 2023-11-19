import json
from constants import TOTAL_BUFFER_SIZE

def readExperiencesFile(fileName="experiences.json"):
	with open(fileName, 'r') as file:
		return json.load(file) # list of lists, each list is an experience tuple

def expToFile(gameExperiences, fileName="experiences.json"):        
        with open(fileName, 'r') as file:
            previousExperiences = json.load(file)
        
        previousExperiences.extend(gameExperiences)
        previousExperiences = previousExperiences[-TOTAL_BUFFER_SIZE:]

        with open(fileName, 'w') as file:
            json.dump(previousExperiences, file)

def deleteFileContent(fileName="experiences.json"):
      with open(fileName, 'w') as file:
            json.dump([], file)