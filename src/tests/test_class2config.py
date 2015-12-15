import unittest
from class2config import *
from test_data import *


class TestClass2Config(unittest.TestCase):
  
  def test_get_class_obj(self):
    self.assertEqual(A.__class__,get_class_obj(load_module("test_data"),"A").__class__)

if __name__ == '__main__':
    unittest.main()
