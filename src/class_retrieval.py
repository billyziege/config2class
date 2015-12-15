import imp
import inspect

def load_module(module_name):
  """
  Loads the provide module or throws an exception.
  Args:
    module_name: The name of the module where the code for the class is.
  """
  find_return = imp.find_module(module_name)
  if find_return is None:
    raise Exception("No module " + module_name + " found in your python path.")
  else:
    f, filename, description = find_return
  return imp.load_module(module_name, f, filename, description)


def get_class_obj(module_name,class_name):
  """
  Retrieves the class object with the class name class_name
  from the module with module_name.
  Args:
    module_name: The name of the module where the code for the class is.
    class_name: The name of the class to be returned.
  Return value:
    class_obj: The class object itself.
  """
  module_obj = load_module(module_name)
  if hasattr(module_obj,class_name):
    return getattr(module_obj,class_name)
  #If class_name not present, throw exception.
  raise Exception("No class " + class_name + " found in " + module_obj.__module__ + ".")
