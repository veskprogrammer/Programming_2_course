from typing import Callable, Dict, List

class ValidationError(Exception):
    pass

BinaryTreeType = Dict[int, List["BinaryTreeType"]]

def __gen_bin_tree_without_validation(root: int = 6,
                                     height: int = 5,
                                     left_leaf: Callable[[int], int] = lambda x: (x * 2) - 2,
                                     right_leaf: Callable[[int], int] = lambda y: y + 4) -> BinaryTreeType:
    
    """
    Генерирует бинарное дерево в виде словаря.
    
    Args:
        root: Корень дерева. По умолчанию 6.
        height: Высота дерева. По умолчанию 5.
        left_leaf: Функция для вычисления значения левого потомка.
                  По умолчанию lambda x: (x * 2) - 2.
        right_leaf: Функция для вычисления значения правого потомка.
                   По умолчанию lambda y: y + 4.
    
    Returns:
        BinaryTreeType: Бинарное дерево в формате {value: [left_child, right_child]},
                       где left_child и right_child имеют такую же структуру.
    """

    if not isinstance(height, int):
        raise ValidationError("height должна быть целым числом")
    if not isinstance(root, int):
        raise ValidationError("root должен быть числом")
    if height < 0:
        raise ValidationError("height дерева не может быть отрицательной")
    if not callable(left_leaf) or not callable(right_leaf):
        raise ValidationError("left_leaf и right_leaf должны быть функциями")
    if height == 0:
        return {root: []}

    lst = [[] for _ in range(height + 1)]
    lst[0].append(str(root))
    for level in range(1, height + 1):
        countOfChildren = 2 ** level
        for i in range(0, countOfChildren, 2):
            stringLeft = str(left_leaf(int(lst[level - 1][i // 2])))
            stringRight = str(right_leaf(int(lst[level - 1][i // 2])))
            lst[level].append(stringLeft)
            lst[level].append(stringRight)

    res = [[] for _ in range(len(lst))]  
    res[0] = [{lst[0][0]: []}] 
    for level in range(1, len(lst)):
        for i in range(0, len(lst[level]), 2):
            parent_index = i // 2
            parent_root = res[level-1][parent_index]
            parent_key = list(parent_root.keys())[0]
            
            child_node_l = {lst[level][i]: []} 
            child_node_r = {lst[level][i+1]: []} 
            
            parent_root[parent_key] = [child_node_l]
            parent_root[parent_key].append(child_node_r)
                
            res[level].append(child_node_l) 
            res[level].append(child_node_r)

    return res[0][0]

def gen_bin_tree(root: int = 6,
                 height: int = 5,
                 left_leaf: Callable[[int], int] = lambda x: (x * 2) - 2,
                 right_leaf: Callable[[int], int] = lambda y: y + 4):
    try:
        result = __gen_bin_tree_without_validation(root, height, left_leaf, right_leaf) 
        return result
    except ValidationError as e:
        print(e)
        return None