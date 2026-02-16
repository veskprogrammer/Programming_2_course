from typing import Generator, Optional

class FibGetItem:
    """
    'Упрощенный' итератор Фибоначчи через метод __getitem__.
    Позволяет обращаться к числам Фибоначчи по индексу: obj[n].
    """

    def __getitem__(self, index: int) -> int:
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if index < 0:
            raise IndexError("Индекс не может быть отрицательным")
        
        a, b = 0, 1
        for _ in range(index):
            a, b = b, a + b
        return a


class FibIterator:
    """
    Итератор Фибоначчи, реализующий __iter__ и __next__.
    """

    def __init__(self, limit: Optional[int] = None):
        """
        :param limit: Количество чисел Фибоначчи для генерации. 
                      Если None — итератор бесконечен.
        """
        self.limit = limit
        self.count = 0
        self.a, self.b = 0, 1

    def __iter__(self) -> "FibIterator":
        return self

    def __next__(self) -> int:
        if self.limit is not None and self.count >= self.limit:
            raise StopIteration
        
        res = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return res


def fib_coroutine() -> Generator[int, int, None]:
    """
    Сопрограмма, возвращающая числа ряда Фибоначчи.
    Принимает значение через .send(), которое может сбросить или изменить ряд.
    """
    a, b = 0, 1
    while True:
        # yield возвращает значение и ждет получения новых данных через .send()
        received = yield a
        if received is not None:
            # Для примера: если прислали число, сбрасываем последовательность
            a, b = 0, 1
        else:
            a, b = b, a + b
