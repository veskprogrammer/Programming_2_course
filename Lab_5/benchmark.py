import timeit
import matplotlib.pyplot as plt
from factorial_iterative import factorial_iterative, factorial_iterative_cached
from factorial_recursive import factorial_recursive, factorial_recursive_cached

def benchmark(func, data, number=10000, repeat=5):
    total = 0
    for n in data:
        times = timeit.repeat(lambda: func(n), number=number, repeat=repeat)
        total += min(times)
    return total / len(data)

def main():
    # тестовые данные
    test_data = list(range(10, 101, 10))

    # результаты для графиков
    res_recursive = []
    res_iterative = []
    res_recursive_cached = []
    res_iterative_cached = []

    print("Запуск бенчмарков...")
    
    for n in test_data:
        # без кэширования
        time_recursive = benchmark(factorial_recursive, [n], number=1000)
        time_iterative = benchmark(factorial_iterative, [n], number=1000)
        
        # с кэшированием
        time_recursive_cached = benchmark(factorial_recursive_cached, [n], number=10000)
        time_iterative_cached = benchmark(factorial_iterative_cached, [n], number=10000)
        
        res_recursive.append(time_recursive)
        res_iterative.append(time_iterative)
        res_recursive_cached.append(time_recursive_cached)
        res_iterative_cached.append(time_iterative_cached)
        
        print(f"n={n}: рекурсив={time_recursive:.6f}s, итератив={time_iterative:.6f}s, рекурсив_кэш={time_recursive_cached:.6f}s, итератив_кэш={time_iterative_cached:.6f}s")

    # График 1: без кэширования
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(test_data, res_recursive, 'ro-', label="Рекурсивный")
    plt.plot(test_data, res_iterative, 'bo-', label="Итеративный")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Без кэширования")
    plt.legend()
    plt.grid(True)

    # График 2: с кэшированием
    plt.subplot(1, 2, 2)
    plt.plot(test_data, res_recursive_cached, 'ro-', label="Рекурсивный (кэш)")
    plt.plot(test_data, res_iterative_cached, 'bo-', label="Итеративный (кэш)")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("С кэшированием")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()