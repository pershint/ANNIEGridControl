import json
import glob
import tarfile
import sys, os
import shutil
import lib.ArgParser as ap
import lib.TextSweeper as ts
import lib.script_writer as sw

#Controls location to save output fit results
BASEPATH = os.path.dirname(__file__)
CONFIGPATH = os.path.abspath(os.path.join(BASEPATH, "config"))
OUTCONFIGPATH = os.path.abspath(os.path.join(BASEPATH,"TAConfig_out"))
OUTSCRIPTPATH = os.path.abspath(os.path.join(BASEPATH,"script_out"))

if __name__=='__main__':
    print("WE BEGIN THE CONTROL")
    #Open the configuration dictionary
    with open(ap.args.CONFIG,"r") as f:
        ourconfig = json.load(f)

    #Fill in the input/output files on the ToolAnalysis config template
    replacements = ourconfig["TA_REPLACEMENTS"]
    TASweeper = ts.TextSweeper(scandict=replacements)
    configtemp = ourconfig["TOOLANALYSISCONFIGNAME"]
    TASweeper.ReplaceInDirectoryFiles("%s/%s"%(CONFIGPATH,configtemp),
                                      OUTCONFIGPATH)
    #Tar up the configs
    with tarfile.open("%s/config_tar.tar.gz"%(OUTCONFIGPATH),"w:gz") as tar:
        tar.add(OUTCONFIGPATH, arcname=os.path.basename(OUTCONFIGPATH))
    if ap.args.NOSAVE:
        contents = glob.glob("%s/*"%(OUTCONFIGPATH))
        [os.remove(c) for c in contents]

    #Now, lets test our script writers
    sw.WriteTAScript("./script_out/TAjobtest.sh",ourconfig)
    sw.WriteJobSubmission("./script_out/submittest.sh","./TAjobtest.sh",ourconfig)
