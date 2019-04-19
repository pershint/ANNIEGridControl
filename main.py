import json
import copy
import glob
import tarfile
import sys, os
import shutil
import lib.ArgParser as ap
import lib.TextSweeper as ts
import lib.script_writer as sw
import lib.SetupParser as sp #Controls location to save output fit results

BASEPATH = os.path.dirname(__file__)
CONFIGPATH = os.path.abspath(os.path.join(BASEPATH, "config"))
OUTCONFIGPATH = os.path.abspath(os.path.join(BASEPATH,"output","Configured_Files"))
OUTSCRIPTPATH = os.path.abspath(os.path.join(BASEPATH,"output","Scripts"))
OUTLOGPATH = os.path.abspath(os.path.join(BASEPATH,"output","JobLogs"))

if __name__=='__main__':
    print("\n#############################################")
    print("###### INITIALIZING ANNIE GRID CONTROL ######")
    print("#############################################\n")
    
    #Open the configuration dictionary
    with open(ap.args.CONFIG,"r") as f:
        mainconfig = json.load(f)
    if ap.args.RESET:
        print("CLEARING ALL GRID JOB OUTPUTS IN output DIRECTORY")
        configs_toclear = glob.glob("%s/*"%(OUTCONFIGPATH))
        scripts_toclear = glob.glob("%s/*"%(OUTSCRIPTPATH))
        logs_toclear = glob.glob("%s/*"%(OUTLOGPATH))
        dirclears = configs_toclear + scripts_toclear
        for f in logs_toclear:
            os.remove(f)
        for f in dirclears:
            shutil.rmtree(f)
        sys.exit(0)
    if ap.args.SETUP is None:
        print(("No specific script setup specified.  Writing sob submission" +
               " scripts with default grid script structure"))

    #Parse input directories
    if ap.args.DEBUG:
        print("SETUP: %s"%(str(ap.args.SETUP)))
        print("SETUP_INPUTS: \n")
        print(ap.args.SETUPINPUTS)

    #Prepare input files
    input_files = []  
    for infile in ap.args.FILEINPUT:
        input_files.append(infile)

    #Check that output directory specified exists
    MainOutputDir = mainconfig["SUBMISSION_SPECS"]["output_directory"]
    if not os.path.exists(MainOutputDir):
        print("Output file given in main configuration does not exist!")
        sys.exit(1)

    #Prepare any replacements to be made in the input files
    #Or configuration files for each job.
    replacements = [{}] #Key/value replacements to make
    if ap.args.SETUP is not None:
        replacements,setup_infiles = sp.GetReplacementDicts(ap.args.SETUP,
                                                          ap.args.SETUPINPUTS)
    for jnum,replacement_dict in enumerate(replacements):
        if (ap.args.MAXJOBS>0 and jnum > ap.args.MAXJOBS):
            break
        thisjobconfig = copy.deepcopy(mainconfig)
        if ap.args.DEBUG:
            print("REPLACEMENT DICT FOR THIS JOB: " + str(replacement_dict))
            print("ABSOLUTE PMT/LAPPD FILE PATHS FOR JOB: " + str(setup_infiles))
        if not replacement_dict:
            print(("SENDING SINGLE JOB WITH " +
                   "NO REPLACEMENTS MADE TO INPUT FILES"))
            jnum = int(ap.args.JOBNUM)
        print("WRITING SCRIPTS FOR JOB %i"%(jnum))
        ThisJobfilesDir = "%s/jobsubmit_%i/"%(OUTCONFIGPATH,jnum)
        tarname = "%sinputfiles_tar_job_%i.tar.gz"%(ThisJobfilesDir,jnum)
        TASweeper = ts.TextSweeper(scandict=replacement_dict)
        TASweeper.ReplaceInDirectoryFiles("%s/%s"%(CONFIGPATH,thisjobconfig["FILES_FOR_REPLACING"]),
                                          ThisJobfilesDir)
        #Tar up the config
        with tarfile.open(tarname,"w:gz") as tar:
            tar.add(ThisJobfilesDir, arcname=os.path.basename(ThisJobfilesDir))
        
        #Make a subdirectory in the specified output directory for this job
        thisjobconfig["SUBMISSION_SPECS"]["output_directory"] = \
                "%s/joboutput_%i"%(mainconfig["SUBMISSION_SPECS"]["output_directory"],jnum)
        ThisJobsOutputDir = thisjobconfig["SUBMISSION_SPECS"]["output_directory"]
        if not os.path.exists(ThisJobsOutputDir):
            os.mkdir(ThisJobsOutputDir)

        #Now, lets test our script writers
        ThisJobsScriptsDir = "%s/jobsubmit_%i"%(OUTSCRIPTPATH,jnum)
        if not os.path.exists(ThisJobsScriptsDir): os.mkdir(ThisJobsScriptsDir)
        jobfilepath = "%s/gridjob_%i.sh"%(ThisJobsScriptsDir,jnum)
        jobsubmitterpath = "%s/jobsubmitter_%i.sh"%(ThisJobsScriptsDir,jnum)
        if ap.args.SETUP is None:
            input_files.append(tarname)
            sw.WriteGenericJob(jobfilepath,thisjobconfig,input_files)
            sw.WriteJobSubmission(jobsubmitterpath, jobfilepath,
                                  thisjobconfig)
        elif ap.args.SETUP == "TOOLANALYSISRECO":
            thisjob_input_files = input_files + setup_infiles[jnum]
            thisjob_input_files.append(tarname)
            sw.WriteTAJob(jobfilepath,thisjobconfig,thisjob_input_files)
            sw.WriteJobSubmission(jobsubmitterpath, jobfilepath,
                                  thisjobconfig)
        if not ap.args.NOSUBMIT:
            #Shoot off the job script now.
            print("SUBMITTING JOB %i"%(jnum))
            joblogpath = "%s/jobsubmit_log_%i"%(OUTLOGPATH,jnum)
            os.system("bash %s > %s & "%(jobsubmitterpath,joblogpath))
