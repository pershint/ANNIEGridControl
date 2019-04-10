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
    if ap.args.RESET:
        configs_toclear = glob.glob("%s/*"%(OUTCONFIGPATH))
        scripts_toclear = glob.glob("%s/*"%(OUTSCRIPTPATH))
        clears = configs_toclear + scripts_toclear
        for f in clears:
            shutil.rmtree(f)
        sys.exit(0)
    if args.REPLACEMENTRULE is None:
        print(("You must specify a replacement rule; necessary for ANNIEGridControl "+
              "to know how the keyinputs and inputdirs are used"))
        sys.exit(1)

    #Parse input directories
    inputdirs = {}
    print("REPRULE: %s"%(str(ap.args.REPLACEMENTRULE)))
    print("INPUTDIRS: %s"%(str(ap.args.INPUTDIRS)))
    for j,val in enumerate(ap.args.INPUTDIRS):
        if (j%2==0): inputdirs[val] = ap.args.INPUTDIRS[j+1]
            
    #Fill in the input/output files on the ToolAnalysis config template
    replacements = [{}]
    input_file_arrays = []
    if ap.args.REPLACEMENTRULE is not None:
        replacements,input_file_arrays = rp.GetReplacementDicts(ap.args.REPLACEMENTRULE,inputdirs)

    for j,replacement_dict in enumerate(replacements):
        configtarname = "%s/config_tar_job_%i.tar.gz"%(ThisJobOutputDir,j)
        input_files = input_file_arrays[j]
        input_files.append(configtarname)
        print("REPLACEMENT DICT: " + str(replacement_dict))
        ThisJobOutputDir = "%s/jobsubmit_%i"%(OUTCONFIGPATH,j)
        ThisScriptOutputDir = "%s/jobsubmit_%i"%(OUTSCRIPTPATH,j)
        TASweeper = ts.TextSweeper(scandict=replacement_dict)
        configtemp = ourconfig["TOOLANALYSISCONFIGNAME"]
        TASweeper.ReplaceInDirectoryFiles("%s/%s"%(CONFIGPATH,configtemp),
                                          ThisJobOutputDir)
        #Tar up the configs
        with tarfile.open(configtarname,"w:gz") as tar:
            tar.add(OUTCONFIGPATH, arcname=os.path.basename(ThisJobOutputDir))
        if ap.args.NOSAVE:
            contents = glob.glob("%s/*"%(ThisJobOutputDir))
            [os.remove(c) for c in contents]

        #Now, lets test our script writers
        sw.WriteTAScript("./script_out/TAjobtest_%i.sh"%(j),ourconfig)
        sw.WriteJobSubmission("%s/submittest_%i.sh"%(ThisScriptOutputDir,j),
                              "%s/TAjobtest_%i.sh"%(ThisScriptOutputDir,j),
                              ourconfig,input_files)
