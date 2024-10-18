// Simulate genetic inheritance of blood type

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Each person has two parents and two alleles
typedef struct person
{
    struct person *parents[2];
    char alleles[2];
} person;

const int GENERATIONS = 3;
const int INDENT_LENGTH = 4;

person *create_family(int generations);
void print_family(person *p, int generation);
void free_family(person *p);
char random_allele();

int main(void)
{
    // Seed random number generator
    srand(time(0));

    // Create a new family with three generations
    person *p = create_family(GENERATIONS);

    // Print family tree of blood types
    print_family(p, 0);

    // Free memory
    free_family(p);
}

// Create a new individual with `generations`
person *create_family(int generations)
{
    // Allocate memory for new person (exciting, isn't it?)
    person *new_person = malloc(sizeof(person));

    // If there are still generations left to create, dive deeper into the family tree
    if (generations > 1)
    {
        // Recursively create two new parents for the current person
        person *parent0 = create_family(generations - 1);
        person *parent1 = create_family(generations - 1);

        // Set parent pointers for the current person
        new_person->parents[0] = parent0;
        new_person->parents[1] = parent1;

        // Randomly assign current person's alleles based on their parents' alleles
        new_person->alleles[0] = parent0->alleles[rand() % 2];
        new_person->alleles[1] = parent1->alleles[rand() % 2];
    }
    else
    {
        // The oldest generation has no parents; they're at the top of the family tree
        new_person->parents[0] = NULL;
        new_person->parents[1] = NULL;

        // Assign random alleles because the ancestors are long gone
        new_person->alleles[0] = random_allele();
        new_person->alleles[1] = random_allele();
    }

    // Return the newly minted person
    return new_person;
}

// Free `p` and all ancestors of `p`
void free_family(person *p)
{
    // Base case: If there's no one to free, just return
    if (p == NULL)
    {
        return;
    }

    // Free the ancestors (parents first)
    free_family(p->parents[0]);
    free_family(p->parents[1]);

    // Free the current person (goodbye, memory!)
    free(p);
}

// Print each family member and their alleles (with some added flair)
void print_family(person *p, int generation)
{
    // Base case: If there's no one to print, just return
    if (p == NULL)
    {
        return;
    }

    // Print indentation to represent the depth of the family tree
    for (int i = 0; i < generation * INDENT_LENGTH; i++)
    {
        printf(" ");
    }

    // Print the current person
    if (generation == 0)
    {
        printf("Child (Generation %i): blood type %c%c\n", generation, p->alleles[0],
               p->alleles[1]);
    }
    else if (generation == 1)
    {
        printf("Parent (Generation %i): blood type %c%c\n", generation, p->alleles[0],
               p->alleles[1]);
    }
    else
    {
        for (int i = 0; i < generation - 2; i++)
        {
            printf("Great-");
        }
        printf("Grandparent (Generation %i): blood type %c%c\n", generation, p->alleles[0],
               p->alleles[1]);
    }

    // Recursively print the parents of the current generation
    print_family(p->parents[0], generation + 1);
    print_family(p->parents[1], generation + 1);
}

// Randomly choose a blood type allele (we can't all be O-positive)
char random_allele()
{
    int r = rand() % 3;
    if (r == 0)
    {
        return 'A';
    }
    else if (r == 1)
    {
        return 'B';
    }
    else
    {
        return 'O';
    }
}
