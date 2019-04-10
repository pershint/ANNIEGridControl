import json
import glob
import tarfile
import sys, os
import shutil
import lib.ArgParser as ap
import lib.TextSweeper as ts
import lib.script_writer as sw
import lib.RuleParser as rp #Controls location to save output fit results

BASEPATH = os.path.dirname(__file__)
CONFIGPATH = os.path.abspath(os.path.join(BASEPATH, "config"))
OUTCONFIGPATH = os.path.abspath(os.path.join(BASEPATH,"TAConfig_out"))
OUTSCRIPTPATH = os.path.abspath(os.path.join(BASEPATH,"script_out"))

if __name__=='__main__':
    print("WE BEGIN THE CONTROL")
    #Open the configuration dictionary
    with open(ap.args.CONFIG,"r") as f:
        ourconfig = json.load(f)


    #Parse input directories
    inputdirs = {}
    print("REPRULE: %s"%(str(ap.args.REPLACEMENTRULE)))
    print("INPUTDIRS: %s"%(str(ap.args.INPUTDIRS)))
    for j,val in enumerate(ap.args.INPUTDIRS):
        if (j%2==0): inputdirs[val] = ap.args.INPUTDIRS[j+1]
            
    #Fill in the input/output files on the ToolAnalysis config template
    replacements = [{}]
    try:
        replacements = [ourconfig["TA_REPLACEMENTS"]]
    except KeyError:
        print("NOTICE: No file replacements in loaded config.  Need to add a replacement"+\
                " rule, or no replacements are being made")
    if ap.args.REPLACEMENTRULE is not None:
        replacements = rp.GetReplacementDicts(ap.args.REPLACEMENTRULE,inputdirs)

    for j,replacement_dict in enumerate(replacements):
        print("REPLACEMENT DICT: " + str(replacement_dict))
        ThisJobOutputDir = "%s/jobsubmit_%i"%(OUTCONFIGPATH,j)
        TASweeper = ts.TextSweeper(scandict=replacement_dict)
        configtemp = ourconfig["TOOLANALYSISCONFIGNAME"]
        TASweeper.ReplaceInDirectoryFiles("%s/%s"%(CONFIGPATH,configtemp),
                                          ThisJobOutputDir)
        #Tar up the configs
        with tarfile.open("%s/config_tar.tar.gz"%(ThisJobOutputDir),"w:gz") as tar:
            tar.add(OUTCONFIGPATH, arcname=os.path.basename(ThisJobOutputDir))
        if ap.args.NOSAVE:
            contents = glob.glob("%s/*"%(ThisJobOutputDir))
            [os.remove(c) for c in contents]

        #Now, lets test our script writers
        sw.WriteTAScript("./script_out/TAjobtest_%i.sh"%(j),ourconfig)
        sw.WriteJobSubmission("./script_out/submittest_%i.sh"%(j),"./TAjobtest.sh",ourconfig)
