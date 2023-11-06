import json
from constants import TOTAL_BUFFER_SIZE

def readExperiencesFile(fileName="experiences.json"):

	with open(fileName, 'r') as file:
		experiences = json.load(file)

	return experiences # list of lists, each list is an experience tuple

def expToFile(gameExperiences, fileName="experiences.json"):        
        with open(fileName, 'r') as file:
            previousExperiences = json.load(file)
        
        totalBufferSize = TOTAL_BUFFER_SIZE
        previousExperiences.extend(gameExperiences)
        previousExperiences = previousExperiences[-totalBufferSize:]

        with open(fileName, 'w') as file:
            json.dump(previousExperiences, file)