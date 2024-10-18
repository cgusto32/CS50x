from cs50 import get_float


def main():
    # Prompt user for input using get_float until a non-negative value is entered
    while True:
        change_owed = get_float("Change owed: ")
        if change_owed >= 0:
            break

    # Convert the amount to cents to avoid floating-point precision issues
    cents = round(change_owed * 100)

    # Initialize the coin counter
    coins = 0

    # Calculate the number of quarters (25¢)
    coins += cents // 25
    cents %= 25

    # Calculate the number of dimes (10¢)
    coins += cents // 10
    cents %= 10

    # Calculate the number of nickels (5¢)
    coins += cents // 5
    cents %= 5

    # Calculate the number of pennies (1¢)
    coins += cents

    # Print the total number of coins
    print(coins)


if __name__ == "__main__":
    main()
