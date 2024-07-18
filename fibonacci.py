def factorial(num):
    if num == 0 or num == 1:
        return 1
    else:
        return num * factorial(num - 1)
def fibonacci_series(count):
    fib_list = []
    a, b = 0, 1
    fib_list.append(a)
    fib_list.append(b)
    for _ in range(2, count):
        a, b = b, a + b
        fib_list.append(b)
    return fib_list
n = int(input("Enter a number: "))
if n >= 0:
    fact = factorial(n)
    print(f"Factorial of {n} is:", fact)
    print(f"Fibonacci series up to {fact} numbers:")
    fib_series = fibonacci_series(fact)
    print(fib_series)
else:
    print("Please enter a non-negative integer.")
