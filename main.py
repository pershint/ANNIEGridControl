import json
import glob
import tarfile
import sys, os
import shutil
import lib.ArgParser as ap
import lib.TextSweeper as ts

#Controls location to save output fit results
basepath = os.path.dirname(__file__)
configpath = os.path.abspath(os.path.join(basepath, "config"))
outconfigpath = os.path.abspath(os.path.join(basepath,"TAConfig_out"))
outscriptpath = os.path.abspath(os.path.join(basepath,"script_out"))

if __name__=='__main__':
    print("WE BEGIN THE CONTROL")
    #Open the configuration dictionary
    with open(ap.args.CONFIG,"r") as f:
        ourconfig = json.load(f)
    replacements = ourconfig["TA_REPLACEMENTS"]
    TASweeper = ts.TextSweeper(scandict=replacements)
    configtemp = ourconfig["TOOLANALYSISCONFIGNAME"]
    TASweeper.ReplaceInDirectoryFiles("%s/%s"%(configpath,configtemp),
                                      outconfigpath)
    with tarfile.open("%s/config_tar.tar.gz"%(outconfigpath),"w:gz") as tar:
        tar.add(outconfigpath, arcname=os.path.basename(outconfigpath))
    if ap.args.NOSAVE:
        contents = glob.glob("%s/*"%(outconfigpath))
        [os.remove(c) for c in contents]
    #So, let's compartamentalize what we need to do here.
    # - Need a class that writes the bash script which will be sent
    #   to the cluster and used to run ToolAnalysis.
    # - Have a class that writes a simple bash script which sources
    #   the annie_setup, sets up the jobsub_client, then actually submits
    #   the bash script described in the previous step
