import pytest
from fibonacci import FibGetItem, FibIterator, fib_coroutine

def test_fib_get_item():
    fib = FibGetItem()
    assert fib[0] == 0
    assert fib[6] == 8
    with pytest.raises(IndexError):
        _ = fib[-1]

def test_fib_iterator():
    it = FibIterator(limit=3)
    assert list(it) == [0, 1, 1]

def test_fib_coroutine():
    coro = fib_coroutine()
    assert next(coro) == 0
    assert next(coro) == 1
    assert next(coro) == 1
    # Проверка сброса через send
    assert coro.send(True) == 0 
