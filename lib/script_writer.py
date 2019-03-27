#Contains classes for writing bash scripts that are submitted on
#The Fermilab Cluster


class BashScript(object):
    def __init__(self,origfileloc=None):
        if origfileloc is not None:
            self.scriptfile = open(origfileloc,"w")
        self.scriptloc = None

    def LoadBashScript(self,fileloc):
        '''Given a file location, open the file and load it into the
        class' scriptfile object for appending new stuff'''
        self.scriptfile = open(fileloc,"a")
        if not self.scriptfile.name.endswith("sh"):
            print("WARNING: file being loaded does not end with sh...")

    def SaveBashScript(self,fileloc):
        '''Cloase the loaded scriptfile to finalize writing'''
    

