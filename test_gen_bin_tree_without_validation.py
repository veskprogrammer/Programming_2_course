import unittest
from main import gen_bin_tree

class TestBinaryTree(unittest.TestCase):
    def test_tree_structure(self):
        result = gen_bin_tree(
            root=6,
            height=5,
            left_leaf=lambda x: (x * 2) - 2,
            right_leaf=lambda y: y + 4
        )
        
        # Проверка корня
        self.assertIn(6, result)
        self.assertEqual(len(result[6]), 2)
        
        # Проверка первого уровня
        left_child_1 = result[6][0]
        right_child_1 = result[6][1]
        self.assertIn(10, left_child_1)
        self.assertIn(10, right_child_1)
        
        # Проверка второго уровня
        left_child_2 = left_child_1[10][0]
        right_child_2 = left_child_1[10][1]
        self.assertIn(18, left_child_2)
        self.assertIn(14, right_child_2)
        
        # Проверка третьего уровня
        left_child_3 = left_child_2[18][0]
        right_child_3 = left_child_2[18][1]
        self.assertIn(34, left_child_3)
        self.assertIn(22, right_child_3)
        
        # Проверка четвертого уровня
        left_child_4 = left_child_3[34][0]
        right_child_4 = left_child_3[34][1]
        self.assertIn(66, left_child_4)
        self.assertIn(38, right_child_4)
        
        # Проверка пятого уровня
        left_child_5 = left_child_4[66][0]
        right_child_5 = left_child_4[66][1]
        self.assertIn(130, left_child_5)
        self.assertIn(70, right_child_5)

    def test_validation_errors(self):
        # Проверка неверного типа height
        self.assertIsNone(gen_bin_tree(height="invalid"))
        
        # Проверка отрицательной height
        self.assertIsNone(gen_bin_tree(height=-1))
        
        # Проверка неверного типа root
        self.assertIsNone(gen_bin_tree(root="invalid"))
        
        # Проверка неверного типа left_leaf
        self.assertIsNone(gen_bin_tree(left_leaf="not_callable"))

if __name__ == '__main__':
    unittest.main()