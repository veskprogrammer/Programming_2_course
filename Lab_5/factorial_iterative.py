from cache import cache

def factorial_iterative(n):
    if n == 0:
        return 1
    
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

@cache
def factorial_iterative_cached(n):
    return factorial_iterative(n)