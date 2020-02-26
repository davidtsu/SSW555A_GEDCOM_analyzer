import unittest
import os

loader = unittest.TestLoader()
start_dir = os.path.join(os.getcwd(), 'test_directory')
suite = loader.discover(start_dir, pattern='US*_Test.py')

runner = unittest.TextTestRunner()
runner.run(suite)