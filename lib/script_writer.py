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
            flags.rstrip(",")
            flags+=" "
        elif key == "output_directory":
            flags+="-d OUTPUT %s "%(subdetails[key])
        elif key == "input_files":
            if len(subdetails[key])>0:
                for f in subdetails[key]:
                    flags+="-f %s "%(f)
        else:
            flags+="--%s=%s "%(key,subdetails[key])
        if newline:
            flags+="\\\n"
        newline = not newline
    submitline = "jobsub_submit %s"%(flags)
    submitline += "file://%s"%(jobsubmitscript)
    ourfile.write(submitline)
    ourfile.close()
    

def WriteTAScript(fileloc,configdict):
    '''Write out the full TA script using the details given within
    the input configuration file.
      Inputs:
          fileloc [string]
          Specify the location to open the bash script at and ultimate save.
          
          configdict [dictionary]
          Configuration dictionary that contains details necessary for 
          successful job submission.  See config/submit_default.json for
          an example of a configuration dictionary.'''
    ourfile = open(fileloc,"w")
    ourfile.write("source %s\n\n"%(configdict["GRIDSOURCE"]))
    comment1=("#Touch a dummy file in the working directory. \n"+
              "#This is a hack that helps stalled jobs close faster\n\n")
    ourfile.write(comment1)
    dummyline=("DUMMY_OUTPUT_FILE=${CONDOR_DIR_OUTPUT}/${JOBSUBID}"+
               "_${STEM}_dummy_output \n")
    ourfile.write(dummyline)
    ourfile.write("touch ${DUMMY_OUTPUT_FILE}\n")
    ourfile.write("tar xfz config_tar.tar.gz\n")
    ourfile.write("Analyse ./ToolChainConfig")
    ourfile.close()

