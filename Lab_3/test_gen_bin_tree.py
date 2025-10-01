import unittest
from main import gen_bin_tree

class TestGenBinTree(unittest.TestCase):
    def test_default_tree(self):
        tree = gen_bin_tree()
        self.assertIsInstance(tree, dict)
        self.assertEqual(tree['value'], 6)
        self.assertIn('left', tree)
        self.assertIn('right', tree)

    def test_height_zero(self):
        tree = gen_bin_tree(height=0, root=10)
        self.assertIsNone(tree)

    def test_custom_root_and_height(self):
        tree = gen_bin_tree(height=2, root=3)
        self.assertEqual(tree['value'], 3)
        self.assertEqual(tree['left']['value'], 4)
        self.assertEqual(tree['right']['value'], 7)
        self.assertIsNone(tree['left']['left'])
        self.assertIsNone(tree['left']['right'])
        self.assertIsNone(tree['right']['left'])
        self.assertIsNone(tree['right']['right'])

if __name__ == '__main__':
    unittest.main()