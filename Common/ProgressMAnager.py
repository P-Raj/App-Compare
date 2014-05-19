__author = "Pranav"
__email = "pranav09032@hotmail.com"

import pickle
import Logging

logFile = "ProgressManager.log"
logManager = Logging.Logging(logFile)

def getState(filename=None, *params):

    
    if not filename:
        filename = "ProgressManager.dump"

    logManager.log("Getting state for file : " + filename)

    stateValue = {}

    try:
        with open(filename, 'rb') as stateFile:
            for param in len(params):
                stateValue[param] = pickle.load(stateFile)
    except IOError:
        print "Cannot load saved state because : no state was saved"
        logManager.log("Cannot load saved state because : no state was saved")

    return stateValue

def saveState(filename = None, *params):

    if not filename:
        filename = "ProgressManager.dump"

    with open(filename, 'wb') as stateFile:
        for param in params:
            pickle.dump(params, stateFile)

    logManager.log("Saving state for file : " + filename)

    