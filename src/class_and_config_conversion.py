from ConfigParser import ConfigParser, SafeConfigParser, NoSectionError
import inspect
import re
from class_retrieval import load_module, get_class_obj
from method_parsing import get_all_init_args, get_class_documentation

def export_class_as_config(module_name,class_name,instance_name=None,config=None,**kwargs):
  """
  Takes a class from the specified module and returns a config object with the
  section specifying the instance name and the options specifying the arguments
  for the __init__() method. 
  Args:
    module_name: The name of the module where the code for the class is.
    class_name: The name of the class to be converted to a config object.
    instance_name: The name of the section in the config file.  If 
      this is None, the section will be assumed to be class_name.
    config: A SageConfigParser object to which the class will be added.
      If this object is None, then a new object is initialized and
      passed back as the output.
  Return value:
    config: A SafeConfigParser object now containing the class_name
    from module_name. 
  """
  #Handle optional arguments
  if config is None:
    config = SafeConfigParser()
    config.read('allow_no_value.ini')
  if instance_name is None:
    instance_name = class_name
  
  #Load module and get the needed class objects.
  class_obj = get_class_obj(module_name,class_name)

  #Obtain all of the arguments for initiatilization of the class.
  all_args = get_all_init_args(class_obj,**kwargs)
  documentation = get_class_documentation(class_obj)

  #Create the section.
  config.add_section(instance_name)
  for line in documentation:
    config.set(instance_name,";" + line,"")
  config.set(instance_name,"config2class_import_module_name",module_name)
  config.set(instance_name,"config2class_import_class_name",class_name)
  for arg in all_args["args"]:
    config.set(instance_name,arg,"")
  for i in range(len(all_args["default_args"])):
    arg = "#"+all_args["default_args"][i]
    value = str(all_args["default_values"][i])
    config.set(instance_name,arg,value)
  return config 

def set_attributes_with_config_section(obj, config, section,key_processing_dict=None, safe=False):
  """
  Uses the keys and values in the config's section to set
  attributes of the obj.
  Args:
    obj: The object for which attributes will be set.
    config: A config parser object.
    section: A section in the config parser object
      from which the keys will be used to set attributes.
    key_processing_callback_dict: A dict with string keys and function
      values.  If None, key processing will be skipped.  Otherwise,
      the key will be re.matched to the the string, and if it matches,
      the obj, string, key, and value will be passed to the function.
    safe: If set to true and the section is not in the cofig,
      exits without raising an exception.
  Return value:
    None --- but sets the attributes of the obj in place.  
  """
  if not config.has_section(section):
    if not safe:
      return
    raise NoSectionError("Section named " + section + " is not present in the config.")
  for key in config.options(section):
    value = config.get(section,key) #Enforce that the value goes through the get routine.
    if key_processing_dict is not None:
      prev_key = key
      for string, callback in key_processing_dict.iteritems():
        parsed_key = callback(obj,string,prev_key, value)
        prev_key = parsed_key
      if parsed_key != key:
        continue
    setattr(obj, key, value)
  return
        
def import_classes_from_config_file(config_file,config_parser_class=ConfigParser,**kwargs):
  """
  Does the reverse of the export command above.  Reads in a config file with
  the 2 config2class attributes in each section and loads up the class
  using the parametes in the config section to initialize the instances.
  Args:
    config_file: The config file holding the parameters to be used in instance
      initialization.
    config_parser_class: Allows the passing of alternative config parsers.
  Return value:
    class_dict: A dictionary of classes with the section (or instance_name) of the
      config used as a key.
  """
  class_dict = {}
  config = config_parser_class()
  config.read(config_file)

  for section in config.sections():
    instance = import_class_from_config_section(config,section)
    class_dict[section] = instance
  
  return class_dict

def import_class_from_config_section(config,section):
  """
  Imports the section as a class, calling the relevant class initialization
  method using the options as parameters. 
  """
  if not config.has_option(section,"config2class_import_module_name") or not config.has_option(section,"config2class_import_class_name"):
    raise Exception("The config file, " + config_file + ", does not have the appropriate"
      "required config2class options in the section name "+ section)
  module_name = config.get(section,"config2class_import_module_name")
  class_name = config.get(section,"config2class_import_class_name")
  config2class_options = ["config2class_import_module_name",
                          "config2class_import_class_name"]
  
  class_obj = get_class_obj(module_name,class_name)
  arg_spec = inspect.getargspec(class_obj.__init__)
  args_list = list(arg_spec[0][1:-len(arg_spec[3])]) #This is a list of the required args in order.

  input_args =[]
  for arg in arg_list:
    input_args.append(config.get(section,arg))
  kwargs = {}
  for option in config.options(section):
    if option in args_list + config2class_options:
      continue
    kwargs[option] = config.get(section,option)
  
  return class_obj.__init__(*input_args,**kwargs)
