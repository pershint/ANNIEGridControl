Python program for submitting single/multiple ToolAnalysis jobs to the cluster.

Note: All input and output files should be somewhere in the /pnfs/ space for
the grid nodes to be able to access them.

QUICK-START: SUBMITTING A SINGLE JOB

Let's say you want to submit a single ToolAnalysis job to 
the cluster.

  0. Open up config/submit_default.json.  Set the submission specs to
     whatever submission details you would like.  For more details on
     each entry, see config/HELP.txt.

  1. Place all the ToolAnalysis configuration files 
     into a single directory.  In submit_default.json, set this directory
     to the value for "FILES_FOR_REPLACING".  All config filenames must
     end with "Config".


  2. Let's assume that your ToolAnalysis job needs a data file that's on pnfs
     somewhere.  Assume the name /pnfs/path/to/myfile.root.

  3. If your ToolAnalysis configuration gives any output, you must preface the
     filepath in the Config with CONDOR_DIR_OUTPUT.  On runtime, this will be
     replaced with the actual output directory for the grid node being used.

  4. Run the command:
     $ python main.py -f /pnfs/path/to/myfile.root

SUBMITTING A SINGLE JOB & REPLACING A VARIABLE FOUND IN THE CONFIGS

This is for if you want to replace a variable found in the ToolAnalysis Config
files prior to job submission.

   1. Repeat steps 1-3 above.

   2. In the config file, replace whatever text you want replaced 
      prior to job submission with a variable. Assume we give it the variable
      MY_VARIABLE and want to replace it with some filename myotherfile.root

   3. Run the command:
    $ python main.py -f /pnfs/path/to/myfile.root -k MY_VARIABLE myotherfile.root


SETUPS

A setup of ANNIEGridControl will submit jobs in a specific manner based on the
setup name given.  A setup will generally also require specific inputs into the 
--setupinputs flag.

Currently implemented setups:

  SETUP NAME: TOOLANALYSISRECO
  This setup is designed to submit a series of jobs 
  to the grid that run the ToolAnalysis Vertex Reconstruction chain.

  Steps to running a TOOLANALYSISRECO setup:

    1. Place all the ToolAnalysis configuration files 
       into a single directory.  In submit_default.json, set this directory
       to the value for "FILES_FOR_REPLACING".  All config filenames must
       end with "Config".

    2. In the LoadWCSimConfig and LoadWCSimLAPPDConfig files, give the InputFile
       variables INPUT_FILE_PMT and INPUT_FILE_LAPPD.

    3. In PhaseIITreeMaker, give the OutputFile term a variable, say OUTPUT_FILE_TREE.

    4. Place your PMT and LAPPD MC data in two separate directories.  Filename
       structure is assumed to be wcsim_N.root and wcsim_lappd_N.root, where
       N is one or several period-delimited numbers.

    5. Run the command:
       $ python main.py -S TOOLANALYSISRECO -s INPUT_FILE_PMT /path/to/pmtdata/
         INTPUT_FILE_LAPPD /path/to/lappddata/ OUTPUT_FILE_TREE
