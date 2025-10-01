`Киселев Георгий, ИВТ-1.1`
---
# Отчёт ЛР-3

## **Цель работы**  
Реализовать и протестировать рекурсивную функцию для генерации бинарного дерева с заданной высотой и корневым значением.

---

## **Исходный код**

### **1. Файл `main.py`**
```python
def gen_bin_tree(height=5, root=6):
    if height == 0:
        return None
    left = (root * 2) - 2
    right = root + 4
    return {
        'value': root,
        'left': gen_bin_tree(height - 1, left),
        'right': gen_bin_tree(height - 1, right)
    }
```

### **2. Файл `test_gen_bin_tree.py`**
```python
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
```

---

## **Описание реализации**

### **Алгоритм работы функции `gen_bin_tree`**
1. **Базовый случай**: если высота `height` равна 0, возвращается `None`.
2. **Рекурсивный шаг**:
   - Вычисляются значения для левого и правого потомков:
     - `left = (root * 2) - 2`
     - `right = root + 4`
   - Формируется словарь с ключами:
     - `value`: текущее значение узла,
     - `left`: рекурсивный вызов для левого поддерева с высотой `height - 1`,
     - `right`: рекурсивный вызов для правого поддерева с высотой `height - 1`.

---

## **Тестирование**

### **Тест 1: Проверка дерева по умолчанию**
- **Условия**: вызов функции без параметров.
- **Ожидаемый результат**:
  - Тип возвращаемого значения — `dict`,
  - Корень дерева равен 6,
  - Наличие ключей `left` и `right`.

### **Тест 2: Проверка высоты 0**
- **Условия**: `height=0`, `root=10`.
- **Ожидаемый результат**: `None`.

### **Тест 3: Проверка пользовательских параметров**
- **Условия**: `height=2`, `root=3`.
- **Ожидаемый результат**:
  - Корень: 3,
  - Левый потомок: 4,
  - Правый потомок: 7,
  - Отсутствие потомков у листьев.

---

## **Результаты тестирования**
Все тесты успешно пройдены:
- ✅ `test_default_tree`
- ✅ `test_height_zero`
- ✅ `test_custom_root_and_height`

---

## **Вывод**
В ходе работы была реализована рекурсивная функция генерации бинарного дерева. Алгоритм корректно обрабатывает базовые и рекурсивные случаи. Написаны модульные тесты, подтверждающие правильность работы функции для различных входных данных.
