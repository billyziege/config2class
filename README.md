This package is intended to provide a link between ConfigParser
and the __init__() of classes.  Specifically, since the parameters
of a class are generally define by the __init__() method, this 
package provides the ability to store these parameters in a config
file which can be loaded as the object.

The main scripts are:
  class2config.py: Takes a class from a module and prints out a config file 
    template that needs to be editted to pass the parameters to the read in function.

The main function is:
  read_config_as_class()

Make sure that any module referenced is within the PYTHONPATH.  Specifically,
for Unix and MacOS systems:

  % export PYTHONPATH = $PYTHONPATH:${path to directory containing module}
