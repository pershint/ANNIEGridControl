#Method that looks at a rule for linking inputs in ToolAnalysis
#Configuration files.  Returns the relevant TA_REPLACEMENTS dictionaries
#Used to write the ToolAnalysis configurations.

import glob

def GetReplacementDicts(ruleInput, *argv):
    '''
    Given a rule input ,
    will produce an array of replacements to make to help produce all configuration
    files for submitting ToolAnalysis jobs.
    Inputs:
        ruleInput Array
            Input of the form ["RULENAME", "RULEARG1", "RULEARG2",...].  
        *argv
            Any additional inputs necessary to form the dictionaries used to make
            replacements in ToolAnalysis config files.
    Output array of dictionaries
        Array of dictionaries.  Each dictionary can be used by the TextSweeper class to replace
        keys typed into the template config files with the value in the dictionary entry.
    '''
    if ruleInput[0] == "PMTLAPPDRECO":
        if len(ruleInput) > 4:
            print(("Rule LAPPDPMTPAIRS only takes in two directories; the"+
                   " PMT data directory and the LAPPD data directory."))
        PMT_ReplacementKey = ruleInput[1]
        LAPPD_ReplacementKey = ruleInput[2]
        OutputKey = ruleInput[3]
        InputDirs = argv[0]
        if PMT_ReplacementKey in InputDirs:
            PMTFiles = glob.glob("%s/*.root"%(InputDirs[PMT_ReplacementKey]))
        if LAPPD_ReplacementKey in InputDirs:
            LAPPDFiles = glob.glob("%s/*.root"%(InputDirs[LAPPD_ReplacementKey]))
        file_pairs = []
        for pf in PMTFiles:
            found_LAPPD_match = False
            pf_split = pf.split("_")
            for lf in LAPPDFiles:
                lf_split = lf.split("_")
                if pf_split[1] == lf_split[2]:
                    outsuffix = lf_split[2]
                    apair = [pf,lf,"output_%s"%(outsuffix)]
                    file_pairs.append(apair)
                    found_LAPPD_match = True
            if not found_LAPPD_match:
                print("WARNING: COULD NOT FIND LAPPD PAIR TO PMT FILE %s"%(pf))

        if len(file_pairs)==0:
            print("WARNING: No PMT/LAPPD file matches found for processing!")
            return None
        replacement_dicts = []
        for apair in file_pairs:
            replacement_dict = {}
            replacement_dict[PMT_ReplacementKey] = apair[0]
            replacement_dict[LAPPD_ReplacementKey] = apair[1]
            replacement_dict[OutputKey] = apair[2]
            replacement_dicts.append(replacement_dict)
        return replacement_dicts

