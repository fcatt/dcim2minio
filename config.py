from argparse import ArgumentParser
from configparser import ConfigParser
import json


argparser = ArgumentParser(description='Backup camera images in the cloud')
argparser.add_argument("-c", "--config", required=True,
                       help="Configuration file")
argparser.add_argument("-s", "--source", required=True,
                       help="Source directory (usually the root of the SDCard)")
argparser.add_argument("--verify", required=False, action="store_true",
                       help="NOT IMPLEMENTED! Verify if each file has a corresponding object")
argparser.add_argument("--initdb", required=False, action="store_true",
                       help="NOT IMPLEMENTED! Create database table and index if non existent")
argparser.add_argument("--verbose", help="Write some informations about the process",
                       required=False, action="store_true")
argparser.add_argument("--backupdb", required=False, action="store_true",
                       help="Backup the SQLite database in the object storage after operations")
args = argparser.parse_args()


def vprint(*arguments, **kwarguments):
    if args.verbose:
        print(*arguments, **kwarguments)


config = ConfigParser(delimiters='=')
if config.read(args.config):
    vprint("Configuration file: " + args.config)
else:
    quit("ERROR: No configuration file at path [" + args.config + "]")

filetypes_json = 'filetypes.json'
if config['DEFAULT']['filetypes']:
    filetypes_json = config['DEFAULT']['filetypes']
filetypes = open(filetypes_json)
fileinfo = json.load(filetypes)

# Following "hack" is… horrible :(
# Putting the file extensions in two tuples,
# one with the dot and one without the dot
exts = []
dot_exts = []
for fileext in fileinfo:
    exts.append(str(fileext).upper())
    dot_exts.append('.'+str(fileext).upper())
exts = tuple(exts)
dot_exts = tuple(dot_exts)

