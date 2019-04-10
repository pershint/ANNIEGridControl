import argparse
import os,sys
import json

#Controls location to save output fit results
basepath = os.path.dirname(__file__)
configpath = os.path.abspath(os.path.join(basepath, "..","config"))

parser = argparse.ArgumentParser(description='Parser to decide what analysis to do')
parser.add_argument('--debug', dest='DEBUG',action='store_true',
        help='Run in debug mode and get some extra outputs and stuff')
parser.add_argument('-n','--nosaveconfigs', dest='NOSAVE',action='store_true',
        help='Choose whether or not to save all TAConfigs submitted to grid')
parser.add_argument('-c','--configfile', dest='CONFIG',action='store',type=str,
        help='Path to configuration file used to generate job scripts')
parser.add_argument('-R','--resetscripts', dest='RESET',action='store_true',
        help='Remove all files in script and ToolAnalysis config directories')
parser.add_argument('--keyinput', dest='KEYINPUT', action='store',nargs="+",
        help='Specify a key found in your config files; replace it with the' + \
                ' second input (usage: --inputfiles #CONFIG_INPUT# file2.txt')
parser.add_argument('-d','--inputdirs', dest='INPUTDIRS', action='store',nargs="+",
        help='Specify a key found in your config files; files in the directory ' + \
                ' will populate the configs (usage: ' +\
                '#INPUT_FILE_PMT# /path/to/dir1/ #INPUT_FILE_LAPPD# /path/to/dir2/')
parser.add_argument('-r','--replacerule', dest='REPLACEMENTRULE', action='store',nargs="+",
        help='Any inputs specified here will be populated simultaneously in config ' +\
                'files based on the rule given. Usage: PMTLAPPDRECO #INPUT_FILE_PMT# #INPUT_FILE_LAPPD#')

defcon = "%s/submit_default.json"%(configpath)

parser.set_defaults(DEBUG=False,CONFIG=defcon, RESET=False,KEYINPUT=None,INPUTDIRS=None,
        NOSAVE=False,REPLACEMENTRULE=None)
args = parser.parse_args()

