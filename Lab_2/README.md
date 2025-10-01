`Киселев Георгий, ИВТ-1.1`
---
# Отчёт по ЛР-2

## Цель работы  
Разработать и протестировать алгоритм поиска индексов двух чисел в массиве, сумма которых равна заданному целевому значению.  

---

## Теоретическая часть  
Алгоритм "Two Sum" решает задачу поиска пары индексов `(i, j)` в массиве `nums`, для которых выполняется условие:  
```
nums[i] + nums[j] = target
```  
где `i ≠ j`.  

### Используемый подход  
- **Метод:** Хэш-таблица (словарь) для хранения чисел и их индексов.  
- **Сложность:**  
  - Время: **O(n)**  
  - Память: **O(n)**  

### Алгоритм  
1. Создать пустой словарь `num_to_index`.  
2. Для каждого элемента `num` в массиве `nums`:  
   - Вычислить `complement = target - num`.  
   - Если `complement` есть в словаре, вернуть индексы `[num_to_index[complement], i]`.  
   - Иначе сохранить `num` в словарь с текущим индексом `i`.  
3. Если решение не найдено, вернуть `None`.  

---

### Код реализации  
[file name]: main.py  
```python
def two_sum(nums, target):
    num_to_index = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_to_index:
            return [num_to_index[complement], i]
        num_to_index[num] = i
    return None
```

### Тестирование  
[file name]: test_two_sum.py  
```python
import unittest
from main import two_sum

class TestTwoSum(unittest.TestCase):
    def test_example1(self):
        self.assertEqual(two_sum([2,7,11,15], 9), [0, 1])

    def test_example2(self):
        self.assertEqual(two_sum([3,2,4], 6), [1, 2])

    def test_example3(self):
        self.assertEqual(two_sum([3,3], 6), [0, 1])

    def test_no_solution(self):
        self.assertIsNone(two_sum([1,2,3], 7))

    def test_negative_numbers(self):
        self.assertEqual(two_sum([-1, -2, -3, -4, -5], -8), [2, 4])

if __name__ == '__main__':
    unittest.main()
```

---

## Результаты тестирования  
```
.....
----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK
```

Все тесты пройдены успешно:  
- ✅ Пример 1: `[2,7,11,15]`, `target=9` → `[0,1]`  
- ✅ Пример 2: `[3,2,4]`, `target=6` → `[1,2]`  
- ✅ Пример 3: `[3,3]`, `target=6` → `[0,1]`  
- ✅ Отсутствие решения: `[1,2,3]`, `target=7` → `None`  
- ✅ Отрицательные числа: `[-1,-2,-3,-4,-5]`, `target=-8` → `[2,4]`  

---

## Вывод  
Алгоритм корректно решает задачу "Two Sum" для всех типов входных данных:  
- Положительные и отрицательные числа  
- Наличие и отсутствие решения  
- Повторяющиеся элементы  
