#Method that looks at a rule for linking inputs in ToolAnalysis
#Configuration files.  Returns the relevant TA_REPLACEMENTS dictionaries
#Used to write the ToolAnalysis configurations.

import glob

def GetReplacementDicts(ruleInput, *argv):
    '''
    Given a rule input ,
    will produce an array of replacements to make to help produce all configuration
    files for submitting ToolAnalysis jobs.  Assumes 
    Inputs:
        ruleInput string
            Setup string given on program execution that indicates what setup of
            ANNIEGridControl is being executed.
        *argv
            Any additional inputs necessary to form the dictionaries used to make
            replacements in input text files (specific to rule: see README for 
            inputs needed for each setup).
    Output: array of dictionaries
        Array of dictionaries. Dictionary is used by TextSweeper class to
        make text replacements in input files prior to job submission.
    '''
    if ruleInput == "TOOLANALYSISRECO":
        if len(argv[0]) != 5:
            print(("Rule TOOLANALYSISRECO should have 5 inputs on command line:" +
                   "INPUT_FILE_KEY1 /path/to/pmtdata/ "+
                   "INPUT_FILE_KEY2 /path/to/lappddata/ "+
                   "OUTPUT_FILE_KEY"))
            return None
        TARecoSetupInputs = argv[0]
        PMT_ReplacementKey = TARecoSetupInputs[0]
        PMT_DataDir = TARecoSetupInputs[1]
        LAPPD_ReplacementKey = TARecoSetupInputs[2]
        LAPPD_DataDir = TARecoSetupInputs[3]
        OutputKey = TARecoSetupInputs[4]
        prePMTFiles = glob.glob("%s/*.root"%(PMT_DataDir))
        PMTFiles=[]
        for p in prePMTFiles:
            if p.find("lappd")==-1:
                PMTFiles.append(p)
        preLAPPDFiles = glob.glob("%s/*.root"%(LAPPD_DataDir))
        LAPPDFiles=[]
        for p in preLAPPDFiles:
            if p.find("lappd")!=-1:
                LAPPDFiles.append(p)
        file_pairs = []
        input_file_arrays = [] #Holds 2-element arrays with full PMT/LAPPD paths
        for pf in PMTFiles:
            found_LAPPD_match = False
            split_fullpf = pf.split("/")
            pf_base = split_fullpf[len(split_fullpf)-1]
            pf_split = pf_base.split("_")
            for lf in LAPPDFiles:
                split_fulllf = lf.split("/")
                lf_base = split_fulllf[len(split_fulllf)-1]
                lf_split = lf_base.split("_")
                if pf_split[1] == lf_split[2]:
                    outsuffix = lf_split[2]
                    input_file_arrays.append([pf,lf])
                    apair = [pf.replace(PMT_DataDir,""),
                            lf.replace(LAPPD_DataDir,""),
                            "CONDOR_DIR_OUTPUT/output_%s"%(outsuffix)]
                    file_pairs.append(apair)
                    found_LAPPD_match = True
            if not found_LAPPD_match:
                print("WARNING: COULD NOT FIND LAPPD PAIR TO PMT FILE %s"%(pf))

        if len(file_pairs)==0:
            print(("WARNING: No PMT/LAPPD file matches found for processing!\n"+
                   "Are your directories defined correctly?  Do PMT(LAPPD)"+
                   "datafiles have structure wcsim_(lappd_)N1.N2.N3.root?"))
            return None
        replacement_dicts = [] #Replacements made in each job's Config scripts
        print("FILEPAIRS ARE: " + str(file_pairs))
        for apair in file_pairs:
            replacement_dict = {}
            replacement_dict[PMT_ReplacementKey] = apair[0]
            replacement_dict[LAPPD_ReplacementKey] = apair[1]
            replacement_dict[OutputKey] = apair[2]
            replacement_dicts.append(replacement_dict)
        return replacement_dicts, input_file_arrays
