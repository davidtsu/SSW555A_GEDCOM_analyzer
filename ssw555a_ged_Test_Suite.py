import unittest
import os

loader = unittest.TestLoader()
start_dir = os.path.join(os.getcwd(), 'test_directory')
suite = loader.discover(start_dir, pattern='US*_Test.py')

runner = unittest.TextTestRunner()
runner.run(suite)

# removes most of the .cpy files that show up every time this is run.

for folder in [x for x in os.listdir(os.path.join(os.getcwd(), 'test_directory')) if os.path.isdir(os.path.join(os.getcwd(), 'test_directory', x))]:
    try:
        l = [os.path.join(os.getcwd(), 'test_directory', folder, f) for f in os.listdir(os.path.join(os.getcwd(), 'test_directory', folder)) if f == '__pycache__']
        for item in l:
            for bad_cpy in os.listdir(item):
                os.remove(os.path.join(item, bad_cpy))
            os.rmdir(item)
    except ValueError as v:
        print(v)
    except FileNotFoundError as f:
        print(f)
    except OSError as o:
        print(o)