import cs50

x = cs50.get_int("x: ")
y = cs50.get_int("y: ")

print(x + y)

if x < y:
    print("x is less than y")
elif x > y:
    print("x is greater than y")
else:
    print("x and y are equal")

z = x / y
print(f"{z:.50f}")
