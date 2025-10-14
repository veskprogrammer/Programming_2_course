from typing import Callable
def gen_bin_tree(height = 5, root = 6) -> dict: 
    
    """Генерация бинарного дерева в виде вложенных словарей.

    params:
        height - высота дерева
        root - значение корня
        left_leaf - функция для вычисления значения левого листа
        right_leaf - функция для вычисления значения правого листа
        """ 
    left_leaf = (root * 2) - 2
    right_leaf = root + 4

    if height == 0:
        return None
    
    return {'value': root,
            'left': gen_bin_tree(height-1, left_leaf),
            'right': gen_bin_tree(height-1, right_leaf)}
