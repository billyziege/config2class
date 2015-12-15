import argparse
import sys
from ConfigParser import SafeConfigParser
from warpoptions import *
parser.description='Finds the given class(es) and writes a config file corresponding to the init parameters for the importer.'
parser.add_argument('class_name', nargs='+', type=str, help='The class name and optional instance name separatd by ":".  Can be more than one if they are separated by spaces. Eg. ZCylinder:First ZCylinder.')
parser.add_argument('-o', dest="output_file", type=str, help='The output file path to which the output should be written.  Default is stdout.', default=None)
args = parser.parse_args()
from class_and_config_conversion import export_class_as_config

def my_parse_args(arg_string):
  """
  Splits the arg_string into it module_name, class_name,
  and optional instance_name components.
  """
  pieces = arg_string.split(":")
  class_name = pieces[0]
  instance_name = None
  if len(pieces) > 1:
    instance_name = pieces[1]
  return (class_name, instance_name)

config = SafeConfigParser()
for arg_string in args.class_name:
  class_name, instance_name = my_parse_args(arg_string) 
  config = export_class_as_config("warp",class_name,instance_name,config)

if args.output_file is None:
  f = sys.stdout
else:
  f = open(args.output_file,'w')
config.write(f)
f.close()
