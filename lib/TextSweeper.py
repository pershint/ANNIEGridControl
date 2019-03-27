import json
import glob
import os

class TextSweeper(object):
    '''
    Class for replacing text in text files in different ways.

    Input:
    scandict (dictionary)
    Dictionary used to inform what text to replace in files.
    If any key is found in a text file, it is replaced with the
    value.
    '''

    def __init__(self,scandict=None):
        if scandict is not None:
            self.scandict = scandict

    def OpenJSON(self,loc):
        with open(loc,"r") as f:
            self.scandict = json.load(loc)

    def ReplaceInFile(self,infile,outfile):
        '''Given an input file, open the file and replace any keys in
        the scandict object with their values.  Save to output file location.'''
        newfile = []
        with open(infile,"r") as f:
            oldfile = f.readlines()
            newfile = []
            for l in oldfile:
                for key in self.scandict:
                    if l.find(key)!=-1:
                        l=l.replace(key,self.scandict[key])
                newfile.append(l)
            f.close()
        with open(outfile,"w") as f:
            for line in newfile:
                f.write(line)
            f.close()

    def ReplaceInDirectoryFiles(self,infiledir,outfiledir):
        '''Given an input directory, scan all files in the directory for
        keys in the scandict, and replace with values.  Save the files to
        the outfiledir'''
        if not os.path.exists(outfiledir):
            os.mkdir(outfiledir)
        infiles = glob.glob("%s/*"%(infiledir))
        print("INFILEDIR: %s"%(infiledir))
        for fi in infiles:
            infiletail = fi.replace(infiledir,"")
            print("INFILETAIL: %s"%(infiletail))
            self.ReplaceInFile(fi,"%s/%s"%(outfiledir,infiletail))
