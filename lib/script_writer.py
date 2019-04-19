#Functions used to write particular types of bash scripts used
#in grid submission

def WriteJobSubmission(fileloc,jobsubmitscript,configdict):
    '''Write out the full TA script using the details given within
    the input configuration file
    Inputs: 
          fileloc [string]
          Specify the location to open this bash script at and ultimate save.
          
          jobsubmitscript [string]
          Location of the script that will be submitted for running on the 
          cluster.

          configdict [dictionary]
          Configuration dictionary that contains details necessary for 
          successful job submission.  See config/submit_default.json for
          an example of a configuration dictionary.

          Array of strings with the names of files to give as input when
          running the job

          jnum [int]
          Specifies this job number to label this job's output subdirectory
    '''
    ourfile = open(fileloc,"w")
    ourfile.write("source %s\n\n"%(configdict["GRIDSOURCE"]))
    ourfile.write("setup jobsub_client\n\n")
    subdetails = configdict["SUBMISSION_SPECS"]

    #Write all flags that append to the job submission
    flags = ""
    newline = False
    for key in subdetails:
        if key == "resource-provides":
            if len(subdetails[key])>0:
                flags+="--%s=usage_model="%(key)
            for resource in subdetails[key]:
                flags+="%s,"%(resource)
            flags = flags.rstrip(",")
            flags+=" "
        elif key == "output_directory":
            flags+="-d OUTPUT %s "%(subdetails[key])
        else:
            flags+="--%s=%s "%(key,subdetails[key])
        if newline:
            flags+="\\\n"
        newline = not newline
    submitline = "jobsub_submit %s"%(flags)
    submitline += "file://%s"%(jobsubmitscript)
    ourfile.write(submitline)
    ourfile.close()
    

def WriteTAJob(fileloc,configdict,infiles):
    '''Write out the full TA script using the details given within
    the input configuration file.
    Any files ending with tar.gz have a line written to untar them.
      Inputs:
          fileloc [string]
          Specify the location to open the bash script at and ultimate save.
          
          configdict [dictionary]
          Configuration dictionary that contains details necessary for 
          successful job submission.  See config/submit_default.json for
          an example of a configuration dictionary.

          infiles [array]
          List of input files that should be in the job running directory.
          Used to untar ToolAnalysis config files.
    '''
    ourfile = open(fileloc,"w")
    ourfile.write("#Source some common UPS setups for transferring files\n")
    ourfile.write("source /cvmfs/fermilab.opensciencegrid.org/products/common/etc/setups\n")
    ourfile.write("setup ifdhc\n")
    ourfile.write("setup fife_utils\n")
    comment1=("\n#Touch a dummy file in the working directory. \n"+
              "#This is a hack that helps stalled jobs close faster\n")
    ourfile.write(comment1)
    dummyline=("DUMMY_OUTPUT_FILE=${CONDOR_DIR_OUTPUT}/__dummy_output \n")
    ourfile.write(dummyline)
    ourfile.write("touch ${DUMMY_OUTPUT_FILE}\n")
    for entry in infiles:
        ourfile.write("ifdh cp -D %s .\n"%(entry))
    #Move tarred text files that have replacements into the output dir. for debugging
    for f in infiles:
        if f.endswith("tar.gz"):
            localtar_arr = f.split("/")
            localtar = localtar_arr[len(localtar_arr)-1]
            ourfile.write("cp %s ${CONDOR_DIR_OUTPUT}/\n"%(localtar))
    #Whatever temp output directory is used, fill it's path into the Config
    ourfile.write("\n#Source the ANNIE-specific UPS products for running ToolAnalysis\n")
    ourfile.write("source %s\n\n"%(configdict["GRIDSOURCE"]))
    #Have to untar after sourcing ANNIE
    for f in infiles:
        if f.endswith("tar.gz"):
            localtar_arr = f.split("/")
            localtar = localtar_arr[len(localtar_arr)-1]
            ourfile.write("tar xfz %s\n"%(localtar))
    ourfile.write('sed -i "s|CONDOR_DIR_OUTPUT|${CONDOR_DIR_OUTPUT}|g" *Config\n')
    ourfile.write("echo 'FILES IN OUR DIRECTORY:'\n")
    ourfile.write('ls\n')
    ourfile.write('\n#Execute main program\n')
    ourfile.write("%s ./ToolChainConfig"%(configdict["MAIN_PROGRAM"]))
    ourfile.close()

def WriteGenericJob(fileloc,configdict,infiles):
    '''Write out a generic job script using the input configuration file.
    Any files ending with tar.gz have a line written to untar them.
      Args:
          fileloc [string]
          Specify the location to open the bash script at and ultimate save.
          
          configdict [dictionary]
          Configuration dictionary that contains details necessary for 
          successful job submission.  See config/submit_default.json for
          an example of a configuration dictionary.
          
          infiles [array]
          List of input files that should be in the job running directory.
          Used to untar ToolAnalysis config files and get any local files needed.
    '''
    ourfile = open(fileloc,"w")
    ourfile.write("#Source some common UPS setups for transferring files\n")
    ourfile.write("source /cvmfs/fermilab.opensciencegrid.org/products/common/etc/setups\n")
    ourfile.write("setup ifdhc\n")
    ourfile.write("setup fife_utils\n")
    comment1=("#Touch a dummy file in the working directory. \n"+
              "#This is a hack that helps stalled jobs close faster\n\n")
    ourfile.write(comment1)
    dummyline=("DUMMY_OUTPUT_FILE=${CONDOR_DIR_OUTPUT}/_dummy_output \n")
    ourfile.write(dummyline)
    ourfile.write("touch ${DUMMY_OUTPUT_FILE}\n")
    for entry in infiles:
        ourfile.write("ifdh cp %s .\n"%(entry))
    #Let's save the configfiles untarred in a directory
    for f in infiles:
        if f.endswith("tar.gz"):
            localtar_arr = f.split("/")
            localtar = localtar_arr[len(localtar_arr)-1]
            ourfile.write("cp %s ${CONDOR_DIR_OUTPUT}/\n"%(localtar))
    ourfile.write("#Source the ANNIE-specific UPS products for running ToolAnalysis\n")
    ourfile.write("source %s\n\n"%(configdict["GRIDSOURCE"]))
    #Have to untar after sourcing ANNIE
    for f in infiles:
        if f.endswith("tar.gz"):
            localtar_arr = f.split("/")
            localtar = localtar_arr[len(localtar_arr)-1]
            ourfile.write("tar xfz %s\n"%(localtar))
    ourfile.write('sed -i "s|CONDOR_DIR_OUTPUT|${CONDOR_DIR_OUTPUT}|g" *Config\n')
    ourfile.write("echo 'FILES IN OUR DIRECTORY:'\n")
    ourfile.write('ls\n\n')
    ourfile.write('#Execute main program\n')
    ourfile.write(configdict["MAIN_PROGRAM"])
    ourfile.close()

