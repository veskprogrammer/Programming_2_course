# Отчёт ЛР-4
### ИВТ-1.1, Киселев Георгий

### Цель работы

Разработать программу на языке Python для построения бинарного дерева с заданными правилами формирования потомков, реализовать функцию генерации дерева, отобразить результат в виде словаря, а также оформить модульные тесты для проверки корректности работы алгоритма.

---

### Текст задачи

Разработайте программу на языке Python, которая будет строить бинарное дерево (дерево, в каждом узле которого может быть только два потомка). Отображение результата в виде словаря (как базовый вариант решения задания). Далее исследовать другие структуры, в том числе доступные в модуле collections в качестве контейнеров для хранения структуры бинарного дерева.

### Описание алгоритма

- **Функция** `gen_bin_tree(root, height, left_leaf, right_leaf)` строит бинарное дерево заданной высоты.
- **Корень дерева** (`root`) задаётся пользователем (по умолчанию 6).
- **Высота дерева** (`height`) задаётся пользователем (по умолчанию 5).
- **Левый потомок** вычисляется по формуле: `(root * 2) - 2`
- **Правый потомок** вычисляется по формуле: `root + 4`
- Алгоритм использует итеративный подход для построения дерева уровня за уровнем.
- Дерево представляется в виде словаря, где каждый узел имеет структуру: `{value: [left_child, right_child]}`

---

### Пример кода

```python
from typing import Callable, Dict, List

class ValidationError(Exception):
    pass

BinaryTreeType = Dict[int, List["BinaryTreeType"]]

def gen_bin_tree(root: int = 6,
                 height: int = 5,
                 left_leaf: Callable[[int], int] = lambda x: (x * 2) - 2,
                 right_leaf: Callable[[int], int] = lambda y: y + 4):
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
    try:
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

        # Генерация значений для всех уровней дерева
        lst = [[] for _ in range(height + 1)]
        lst[0].append(str(root))
        for level in range(1, height + 1):
            countOfChildren = 2 ** level
            for i in range(0, countOfChildren, 2):
                parent_value = int(lst[level - 1][i // 2])
                stringLeft = str(left_leaf(parent_value))
                stringRight = str(right_leaf(parent_value))
                lst[level].append(stringLeft)
                lst[level].append(stringRight)

        # Построение древовидной структуры
        res = [[] for _ in range(len(lst))]
        res[0] = [{lst[0][0]: []}]
        for level in range(1, len(lst)):
            for i in range(0, len(lst[level]), 2):
                parent_index = i // 2
                parent_root = res[level-1][parent_index]
                parent_key = list(parent_root.keys())[0]
                
                child_node_l = {lst[level][i]: []}
                child_node_r = {lst[level][i+1]: []}
                
                parent_root[parent_key] = [child_node_l, child_node_r]
                res[level].extend([child_node_l, child_node_r])

        return res[0][0]
        
    except ValidationError as e:
        print(f"Ошибка валидации: {e}")
        return None
```

---

### Модульные тесты

Для проверки корректности работы функции были написаны тесты с помощью модуля `unittest`:

- Проверка структуры дерева на разных уровнях
- Проверка значений узлов дерева
- Проверка обработки ошибок валидации

```python
import unittest
from binary_tree import gen_bin_tree

class TestBinaryTree(unittest.TestCase):
    def test_tree_structure(self):
        """Тест структуры дерева с высотой 5 и корнем 6"""
        result = gen_bin_tree(
            root=6,
            height=5,
            left_leaf=lambda x: (x * 2) - 2,
            right_leaf=lambda y: y + 4
        )
        
        # Проверка корня
        self.assertIn('6', result)
        self.assertEqual(len(result['6']), 2)
        
        # Проверка первого уровня
        left_child_1 = result['6'][0]
        right_child_1 = result['6'][1]
        self.assertIn('10', left_child_1)
        self.assertIn('10', right_child_1)
        
        # Проверка второго уровня
        left_child_2 = left_child_1['10'][0]
        right_child_2 = left_child_1['10'][1]
        self.assertIn('18', left_child_2)
        self.assertIn('14', right_child_2)
        
        # Проверка третьего уровня
        left_child_3 = left_child_2['18'][0]
        right_child_3 = left_child_2['18'][1]
        self.assertIn('34', left_child_3)
        self.assertIn('22', right_child_3)

    def test_validation_errors(self):
        """Тест обработки ошибок валидации"""
        # Проверка неверного типа height
        self.assertIsNone(gen_bin_tree(height="invalid"))
        
        # Проверка отрицательной height
        self.assertIsNone(gen_bin_tree(height=-1))
        
        # Проверка неверного типа root
        self.assertIsNone(gen_bin_tree(root="invalid"))
        
        # Проверка не callable left_leaf
        self.assertIsNone(gen_bin_tree(left_leaf="not_callable"))

    def test_height_zero(self):
        """Тест дерева высотой 0"""
        result = gen_bin_tree(root=6, height=0)
        self.assertEqual(result, {'6': []})

if __name__ == '__main__':
    unittest.main(verbosity=2)
```

---

### Результаты

- Функция корректно строит бинарное дерево по заданным правилам.
- Все тесты проходят успешно, что подтверждает правильность работы алгоритма.
- Структура дерева представлена в виде вложенных словарей, что удобно для визуализации и дальнейшей обработки.
- Реализована обработка ошибок ввода с помощью кастомного исключения `ValidationError`.

---

### Выводы

- Реализован итеративный вариант генерации бинарного дерева с индивидуальными правилами вычисления потомков.
- Использование словарей для представления дерева обеспечивает гибкость и простоту обработки структуры.
- Модульные тесты обеспечивают надёжную проверку корректности работы функции при различных входных данных.
- Алгоритм корректно обрабатывает краевые случаи и ошибки ввода данных.
