#Class is used to create, load, and save a JSON file that contains
#The indices of jobs that have been run with the current iteration of
#ANNIEGridControl.
import json

class JobLogger(object):
    def __init__(self, logpath=None):
        self._logfile = {}
        if logpath is not None:
            with open(logpath,"r") as f:
                self._logfile = json.load(f)

    def setsetuptype(self,thetype):
        self.logfile["SETUP"] = thetype

    def getsetuptype(self):
        return self.logfile["SETUP"]

    def loadlog(self,logpath):
        with open(logpath,"r") as f:
            self._logfile = json.load(f)

    def savelog(self,logpath):
        with open(logpath,"r") as f:
            json.dump(self._logfile,f,indent=4,sort_keys=True)

    def addindex(self,indexnum):
        if indexnum in self._logfile["INDICES_PROCESSED"]:
            print(("File with this index has been processed!"+
                   "Not adding to list again."))
            return
        self._logfile["INDICES_PROCESSED"].append(indexnum)
