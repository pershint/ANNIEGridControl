#Class is used to create, load, and save a JSON file that contains
#The indices of jobs that have been run with the current iteration of
#ANNIEGridControl.
import json
import os

class JobLogger(object):
    def __init__(self, logfilepath=None):
        self._logfile = {"INDICES_PROCESSED": []}
        if logfilepath is not None:
            with open(logfilepath,"r") as f:
                self._logfile = json.load(f)

    def showlogfile(self):
        print(self._logfile)

    def setsetuptype(self,thetype):
        self.logfile["SETUP"] = thetype

    def getsetuptype(self):
        return self.logfile["SETUP"]

    def loadlog(self,logfilepath):
        if os.path.exists(logfilepath):
            with open(logfilepath,"r") as f:
                self._logfile = json.load(f)
        else:
            print(("JobLogger: Logfile does not exist for setup. " +
                   "Continuing assuming no previous jobs have been processed."))

    def indexexists(self,index):
        if index in self._logfile["INDICES_PROCESSED"]:
            return True
        else:
            return False

    def savelog(self,logfilepath):
        with open(logfilepath,"w") as f:
            json.dump(self._logfile,f,indent=4,sort_keys=True)

    def addindextolog(self,indexnum):
        self._logfile["INDICES_PROCESSED"].append(indexnum)
