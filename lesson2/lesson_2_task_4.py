def fizz_buzz(n):
    for x in range(1, n+1):
        if n % 5 == 0 and n % 3 == 0:
            print("FizzBuzz")
        elif n % 3 == 0:
            print("Fizz")
        elif n % 5 == 0:
            print("Buzz")
        else:
            print(n)


num = int(input("Введите число: "))
fizz_buzz(num)
