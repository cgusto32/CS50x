#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // Make sure program was run with just one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Make sure every character in argv[1] is a digit
    for (int i = 0, len = strlen(argv[1]); i < len; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    // Convert argv[1] from a `string` to an `int`
    int k = atoi(argv[1]);

    // Prompt user for plaintext
    string plaintext = get_string("plaintext:  ");

    // Print the ciphertext
    printf("ciphertext: ");

    // For each character in the plaintext:
    for (int i = 0, len = strlen(plaintext); i < len; i++)
    {
        char c = plaintext[i];

        // Rotate the character if it's a letter
        if (isalpha(c))
        {
            // Preserve case
            char offset = isupper(c) ? 'A' : 'a';
            c = (c - offset + k) % 26 + offset;
        }

        // Print the rotated character
        printf("%c", c);
    }

    // Print a newline
    printf("\n");

    // Exit the program
    return 0;
}
