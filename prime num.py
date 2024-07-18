def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True
def print_prime_numbers(n):
    count = 0
    num = 2
    
    while count < n:
        if is_prime(num):
            print(num, end=" ")
            count += 1
        num += 1
n = int(input("Enter a number: "))
if n <= 0:
    print("Please enter a positive integer.")
else:
    print_prime_numbers(n)
