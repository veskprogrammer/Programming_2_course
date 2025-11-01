from factorial_iterative import factorial_iterative, factorial_iterative_cached
from factorial_recursive import factorial_recursive, factorial_recursive_cached

# Простые тесты
def test_factorials():
    print("Тестирование функций факториала:")
    print("n | Рекурсив | Итератив | Рекурсив(кэш) | Итератив(кэш)")
    print("-" * 60)
    
    for n in [0, 1, 5, 10]:
        rec = factorial_recursive(n)
        it = factorial_iterative(n)
        rec_c = factorial_recursive_cached(n)
        it_c = factorial_iterative_cached(n)
        
        print(f"{n} | {rec:8} | {it:8} | {rec_c:13} | {it_c:12}")

if __name__ == "__main__":
    test_factorials()