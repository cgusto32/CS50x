// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h> // Include for strcasecmp

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Number of buckets in hash table
// A novice developer might choose a very small number, not realizing the impact on performance
const unsigned int N = 26;

// Hash table
node *table[N];

// Keeps track of the number of words loaded
unsigned int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash the word to obtain the corresponding index
    // Using the hash function that only uses the first letter
    unsigned int index = hash(word);

    // Now we'll traverse the linked list at this index
    node *cursor = table[index];
    while (cursor != NULL)
    {
        // Convert both strings to lowercase before comparison (not necessary, but done out of
        // caution)
        char lower_word[LENGTH + 1];
        for (int i = 0; word[i] != '\0'; i++)
        {
            lower_word[i] = tolower(word[i]);
        }
        lower_word[strlen(word)] = '\0';

        char lower_cursor[LENGTH + 1];
        for (int i = 0; cursor->word[i] != '\0'; i++)
        {
            lower_cursor[i] = tolower(cursor->word[i]);
        }
        lower_cursor[strlen(cursor->word)] = '\0';

        if (strcmp(lower_word, lower_cursor) == 0)
        {
            return true;
        }

        // Move to the next node
        cursor = cursor->next;
    }

    // If word is not found, return false
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Novice hash function: just convert the first letter to a number
    // This hash function is very simplistic and might cause lots of collisions
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open the dictionary file (assuming it always exists and is formatted correctly)
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        return false;
    }

    // Initialize the hash table (though this might be unnecessary since global variables are zeroed
    // out)
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    char word[LENGTH + 1];
    while (fscanf(source, "%45s", word) != EOF)
    {
        // Create a new node for each word
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            fclose(source);
            return false;
        }

        // Copy the word into the node
        // Not using strcpy might be risky, but I trust my input
        strcpy(new_node->word, word);

        // Hash the word to find the correct bucket
        unsigned int index = hash(word);

        // Insert the node at the beginning of the linked list
        new_node->next = table[index];
        table[index] = new_node;

        // Increase word count
        word_count++;
    }

    // Close the dictionary file (always good practice to close files)
    fclose(source);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // Just return the global counter variable
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Loop over each bucket in the hash table
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;

            // Free each node one at a time
            free(temp);
        }
    }

    // I am so tired of C
    return true;
}
