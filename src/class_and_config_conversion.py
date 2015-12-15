from ConfigParser import SafeConfigParser
import re
from class_retrieval import load_module, get_class_obj
from method_parsing import get_all_init_args, get_class_documentation

def export_class_as_config(module_name,class_name,instance_name=None,config=None):
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
  all_args = get_all_init_args(class_obj)
  documentation = get_class_documentation(class_obj)

  #Create the section.
  config.add_section(instance_name)
  for line in documentation:
    config.set(instance_name,";" + line,"")
  config.set(instance_name,"config2class_import_class_name",class_name)
  for arg in all_args["args"]:
    config.set(instance_name,arg,"")
  for i in range(len(all_args["default_args"])):
    arg = "#"+all_args["default_args"][i]
    value = str(all_args["default_values"][i])
    config.set(instance_name,arg,value)
  return config 

