import imp
import inspect
import ConfigParser

def config_to_class(config_file):
  """
  Takes a config file and returns an initialized object
  according to the parameters specified in the config
  file.
  """
