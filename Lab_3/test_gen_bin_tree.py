import unittest
from main import gen_bin_tree

class TestGenBinTree(unittest.TestCase):
    def test_height_0(self):
        self.assertEqual(gen_bin_tree(0), None)

    def test_height_1(self):
        self.assertEqual(gen_bin_tree(1), {'value': 6, 'left': None, 'right': None})

    def test_height_2(self):
        self.assertEqual(gen_bin_tree(2), 
                         {'value': 6, 
                          'left': {'value': 10, 'left': None, 'right': None}, 
                          'right': {'value': 10, 'left': None, 'right': None}})
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
