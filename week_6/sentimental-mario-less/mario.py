from cs50 import get_int


def print_half_pyramid(height):
    for i in range(1, height + 1):
        # Print spaces to right-align the pyramid
        print(" " * (height - i), end="")
        # Print the hashes for the pyramid
        print("#" * i)


def main():
    # Prompt the user for the pyramid's height using CS50's get_int
    height = 0
    while height < 1 or height > 8:
        height = get_int("Height: ")

    # Print the half-pyramid
    print_half_pyramid(height)


if __name__ == "__main__":
    main()
