def get_int(prompt):
    while True:
        try:
            x = int(input(prompt))
            if x >= 1 and x <= 8:
                return x
            else:
                print("Invalid value")
        except ValueError:
            print("Not an integer")

def main():
    x = get_int("Height: ")

    for i in range(x):
        spaces = x-(i+1)
        blocks = i+1
        print(" " * spaces, end="")
        print("#" * blocks, end="")
        print("  ", end="")
        print("#" * blocks)

if __name__ == "__main__": main()
