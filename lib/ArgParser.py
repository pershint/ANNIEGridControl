import argparse
import os,sys
import json

#Controls location to save output fit results
basepath = os.path.dirname(__file__)
configpath = os.path.abspath(os.path.join(basepath, "..","config"))

parser = argparse.ArgumentParser(description='Parser to decide what analysis to do')
parser.add_argument('--debug', dest='DEBUG',action='store_true',
        help='Run in debug mode and get some extra outputs and stuff')
parser.add_argument('-c','--configfile', dest='CONFIG',action='store',type=str,
        help='Path to configuration file used to generate job scripts')
parser.add_argument('-j','--jobnum', dest='JOBNUM',action='store',type=str,
        help='Specify a job number to append to the output files generated.')
parser.add_argument('-M','--maxjobs', dest='MAXJOBS',action='store',type=int,
        help='Maximum number of jobs that will be submitted to the grid.')
parser.add_argument('-N','--nosubmit', dest='NOSUBMIT',action='store_true',
        help="Do not submit the jobs to the cluster; just write the scripts.")
parser.add_argument('-r','--resetscripts', dest='RESET',action='store_true',
        help='Remove all files in output/Config_Files and output/script_out')
parser.add_argument('-f','--fileinput', dest='FILEINPUT', action='store',nargs="+",
        help='Give the path to a file you want sent along with the job ' + \
                " submission. Files are not checked for key inputs. " + \
                '(usage: --fileinput file1.txt file2.json')
parser.add_argument('-k','--keyinput', dest='KEYINPUT', action='store',nargs="+",
        help="Specify a key found in your config's FILES_TO_REPLACE " + \
                "directory; replace it with the" + \
                ' second input (usage: --inputfiles #CONFIG_INPUT# file2.txt')
parser.add_argument('-s','--setupinputs', dest='SETUPINPUTS', action='store',nargs="+",
        help='Specify the inputs specific to a selected setup. See README.md'+\
             ' for inputs needed with available setups. (ex. usage for '+\
             'TOOLANALYSISRECO setup: #INPUT_FILE_PMT# /path/to/dir1/ '+\
             '#INPUT_FILE_LAPPD# /path/to/dir2/')
parser.add_argument('-S','--setup', dest='SETUP', action='store',type=str,
        help='(Optional): Specify a specific kind of job to be run.  See the ' + \
             'README on current job setups and their usage.')

defcon = "%s/submit_default.json"%(configpath)

parser.set_defaults(DEBUG=False,JOBNUM=0,MAXJOBS=0,CONFIG=defcon, RESET=False,KEYINPUT=[],
                    SETUPINPUTS=[],SETUP=None,FILEINPUT=[])
args = parser.parse_args()

