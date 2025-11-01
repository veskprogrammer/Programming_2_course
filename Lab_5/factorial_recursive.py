from cache import cache

def factorial_recursive(n):
    if n == 0:
        return 1
    return n * factorial_recursive(n - 1)

@cache
def factorial_recursive_cached(n):
    if n == 0:
        return 1
    return n * factorial_recursive_cached(n - 1)