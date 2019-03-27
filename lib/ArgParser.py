import argparse
import os,sys

#Controls location to save output fit results
basepath = os.path.dirname(__file__)
configpath = os.path.abspath(os.path.join(basepath, "..","config"))

parser = argparse.ArgumentParser(description='Parser to decide what analysis to do')
parser.add_argument('--debug', dest='DEBUG',action='store_true',
        help='Run in debug mode and get some extra outputs and stuff')
parser.add_argument('--nosaveconfigs', dest='NOSAVE',action='store_true',
        help='Choose whether or not to save all TAConfigs submitted to grid')
parser.add_argument('--configfile', dest='CONFIG',action='store',type=str,
        help='Path to configuration file used to generate job scripts')
parser.add_argument('--inputfiles', dest='ADDLINPUT', action='store',nargs="+",
        help='Specify additional input files to pass to grid job (example' + \
                'usage: --inputfiles File1.root file2.txt')

defcon = "%s/submit_default.json"%(configpath)
parser.set_defaults(DEBUG=False,CONFIG=defcon, ADDLINPUT=None,NOSAVE=False)
args = parser.parse_args()
