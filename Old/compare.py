s = input("s: ")
t = input("t: ")

s = s.lower()
t = t.lower()

if s in ["y", "yes"]:
    print("Same")
elif s in ["n", "no"]:
    print("Different")
