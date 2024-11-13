c = 0
while True:
    try:
        n = float(input("Change: "))
        if n >= 0.01 and n <= 250.00:
            break
        else:
            print("Values between 0.01 and 250.00 only.")
    except ValueError:
        print("Not an integer")

n = round(n*100)


while n >= 25:
    n = n - 25
    c += 1

while n >= 10:
    n = n - 10
    c += 1

while n >= 5:
    n = n - 5
    c += 1


while n >= 1:
    n = n - 1
    c += 1

print(f"{c}")
