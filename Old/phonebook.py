people = [
    {"name": "Carter", "number": "617-495-1000"},
    {"name": "David", "number": "617-495-1000"},
    {"name": "John", "number": "949-468-2750"},
]

#! This is an equivalent format for the above when only using a single value field
#! people = {
#!     "Carter": "617-495-1000",
#!     "David": "617-495-1000",
#!     "John": "949-468-2750",
#! }

name = input("Name: ")

for person in people:
    if person["name"] == name:
        print(f"Found: {person["number"]}")
        break
else:
    print("Not found")
