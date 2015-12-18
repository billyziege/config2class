import inspect
import re

def get_all_init_args(class_obj,skip_classes=[],**kwargs):
  """
  Compares the list of init arguments for the class_obj and
  all base classes to those provided in the code to determine
  what are arguments of class_obj.
  Args:
    class_obj:  The object of the class in question.
  Return value: dict with keys args, default_args, default_values
    args: A list of positional arguments passed.
    default_args: A list of args appearing with default values.
    default_values: A 1-to-1 list of values for the default args.
  """
  output={}

  inherited_classes = inspect.getmro(class_obj)  

  parsed_calls = parse_super_init_call(class_obj,**kwargs)

  output["args"] = list()
  output["default_args"] = list()
  output["default_values"] = list()
  try:
    arg_spec = inspect.getargspec(class_obj.__init__)
  except TypeError:
    return output

  output["args"] = list(arg_spec[0][1:-len(arg_spec[3])])
  output["default_args"] = list(arg_spec[0][len(arg_spec[0])-len(arg_spec[3]):])
  output["default_values"] = list(arg_spec[3])
  for inherited_class in inherited_classes:
    if inherited_class == class_obj:
      continue
    if inherited_class.__name__ not in parsed_calls:
      continue
    current_parsed_calls = parsed_calls[inherited_class.__name__]
    arg_spec = inspect.getargspec(inherited_class.__init__)
    arg_spec_dict = {}
    arg_spec_dict["args"] = arg_spec[0][1:-len(arg_spec[3])]
    arg_spec_dict["default_args"] = arg_spec[0][len(arg_spec[0])-len(arg_spec[3]):]
    arg_spec_dict["default_values"] = arg_spec[3]
    difference_dict = defined_init_minus_called_init(output,arg_spec_dict)
    for arg in difference_dict["args"]:
      output["args"].append(arg)
    for arg in difference_dict["default_args"]:
      output["default_args"].append(arg)
    for value in difference_dict["default_values"]:
      output["default_values"].append(value)
  return output
    

def defined_init_minus_called_init(called_dict,defined_dict):
  """
  Compares the list of init arguments for the class_obj and
  the init arguments previously called.
  Args:
    called_dict: The args as they are called within the code.
    defined_dict: The args as they appear in the __init__ method.
  """  
  output ={}
  output["args"] = []
  output["default_args"] = []
  output["default_values"] = []
  difference = len(called_dict) - len(defined_dict) #If the called dict has more arguments, it overlaps the keyed values...
  for i in range(difference,len(defined_dict["default_args"])):
    arg = defined_dict["default_args"][i]
    if arg in called_dict["default_args"]:
      continue
    value = defined_dict["default_values"][i]
    output["default_args"].append(arg)
    output["default_values"].append(value)
  return output 

def parse_super_init_call(class_obj,**kwargs):
  """
  Returns a dictionary of class_name: arguments for base object's
  init within the class's init method. If init is not called, returns an
  empty dict.
  Args:
    class_obj:  The object of the class in question.
  Return value: dictionary {super_class_name: dict with keys args,default_args,default_args,default__values,single_star,double_star}
    super_class_name: The name of the class for which the init function is called.
    args: A list of positional arguments passed.
    default_args: A list of args appearing with an '=' in the argument string.
    default_values: A 1-to-1 list of values for the default args.
    single_star: A list of referenced arrays passed.
    double_star: A list of referenced dicts passed.
  """
  calling_dict = {}
  init_calls = extract_super_init_calls(class_obj)
  for init_call in init_calls:
    class_name, arg_string = init_call.split(".__init__(")
    arg_string.replace(")","") #gets rid of trailing ")"
    calling_dict[class_name] = parse_arg_string(arg_string,ignore_first = True)
  return calling_dict

def extract_super_init_calls(class_obj):
  """
  Returns the string of any occurences of init that occur in the 
  init method of class_obj.
  Args:
    class_obj: The class object for which the init method will be 
    inspected.
  Return value:
    output_calls: A list of strings detailing calls to init.
  """
  init_calls = []
  if not hasattr(class_obj,'__init__'):
    return init_calls
  try:
    init_code_lines = list(inspect.getsourcelines(class_obj.__init__))[0]
  except TypeError:
    return init_calls
  if len(init_code_lines) == 0:
    return init_calls
  init_code_lines.pop(0) #Remove and ignore the first, definition, line.
  line = init_code_lines.pop(0)
  while len(init_code_lines) > 0:
    while not re.search(r"init",line):
      if len(init_code_lines) == 0:
        break
      line = init_code_lines.pop(0)
    if len(init_code_lines) == 0:
      break
    line = line.strip()
    open_count = line.count("(")
    closed_count = line.count(")")
    while open_count != closed_count:
      line += " "+init_code_lines.pop(0).strip()
      open_count = line.count("(")
      closed_count = line.count(")")
    init_calls.append(line)
    if len(init_code_lines) == 0:
      break
    line = init_code_lines.pop(0)
  return init_calls

def get_class_documentation(class_obj):
  """
  Returns the string of the documentation with the
  convention that the comments come right after the __init__ line.
  Args:
    class_obj: The class object for which the init method will be 
    inspected.
  Return value:
    documentation: A list of strings detailing the documentation to init.
  """
  documentation = []
  try:
    code_lines = list(inspect.getsourcelines(class_obj))[0]
  except TypeError:
    return documentation
  if len(code_lines) == 0:
    return documentation
  code_lines.pop(0) #Remove and ignore the first, definition, line.
  line = code_lines.pop(0).strip()
  if not line.startswith('"""'):
    return documentation
  if len(code_lines) == 0:
    return documentation
  documentation.append(line)
  line = code_lines.pop(0).strip()
  documentation.append(line)
  while not line.startswith('"""'):
    if len(code_lines) == 0:
      return documentation
    line = code_lines.pop(0).strip()
    documentation.append(line)
  return documentation
     
  
  while len > 0:
    while not re.search(r"init",line):
      if len(init_code_lines) == 0:
        break
      line = init_code_lines.pop(0)
    if len(init_code_lines) == 0:
      break
    line = line.strip()
    open_count = line.count("(")
    closed_count = line.count(")")
    while open_count != closed_count:
      line += " "+init_code_lines.pop(0).strip()
      open_count = line.count("(")
      closed_count = line.count(")")
    init_calls.append(line)
    line = init_code_lines.pop(0)
  return init_calls

def parse_arg_string(arg_string,ignore_first=False):
  """
  Takes the raw code for a list of function arguments and returns the arguments
  in a similar fashion to inspect.  It is assumed that the arguments contain
  no reference to any function or a list (like [a, b] although a_list where a_list
  is a list is fine) or a dictionary (again like, {a: b}).
  Args:
    arg_string: A string of arguments separated by a ','
    ignore_first: Boolean describing whether the first argument should be skipped. 
      Allows the use of this function with methods (where self should be skipped).
  Return value: dict with keys args,default_args,default_args default_values,single_star,double_star
    args: A list of positional arguments passed.
    default_args: A list of args appearing with an '=' in the argument string.
    default_values: A 1-to-1 list of values for the default args.
    single_star: A list of referenced arrays passed.
    double_star: A list of referenced dicts passed.
  """
  output = {}
  output["args"] = []
  output["default_args"] = []
  output["default_values"] = []
  output["single_star"] = []
  output["double_star"] = []
  arg_list =  arg_string.split(",")
  if len(arg_list) == 0:
    return output
  if ignore_first:
    arg_list.pop(0)
  for arg in arg_list:
    arg = arg.replace(" ","")
    if arg.startswith('**'):
      output["double_star"].append(arg)
    elif arg.startswith('*'):
      output["single_star"].append(arg)
    elif re.search(r'=',arg):
      key, value = arg.split('=')
      output["default_args"].append(key)
      output["default_values"].append(value)
    else:
      output["args"].append(arg)
  return output
