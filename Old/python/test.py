def get_int(prompt):
    return int(input(prompt))


def main():
    x = get_int("x: ")
    y = get_int("y: ")

    print(x+y)
if __name__ == "__main__": main()
