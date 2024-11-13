// Implements a dictionary's functionality

#include "dictionary.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Define other global variables here
int wrdcnt = 0;
int delcnt = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO - check if the word in the text is in the dictionary
    int wl = strlen(word);
    char wordx[wl + 1];
    wordx[wl] = '\0';
    // make all letters in word lowercase
    for (int i = 0; i < wl; i++)
    {
        wordx[i] = tolower(word[i]);
    }
    // If the word is found in the dictionary, True. Case insensitive. Apostrophies - see
    // instructions Hash the word to return a hash value
    int id = hash(wordx);
    // create a second pointer variable in order to crawl along the list without orphaning the whole
    // list at its index start it at the table[id];
    node *cursor = table[id];
    if (cursor == NULL)
    {
        return false;
    }
    while (strcmp(wordx, cursor->word) != 0)
    {
        cursor = cursor->next;
        if (cursor == NULL)
        {
            return false;
        }
    }
    return true;
}

// Traverse linked list, looking for the word (strcasecmp)
// setup a variable that looks at the first node in the linked list.
// if the same, true. If not, check next word in linked list (cursor = cursor->next;)
// if cursor *node next == NULL, then false

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash
    // functionXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Ensure all pointers in hash table are 0
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }
    // Open the dictionary file
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        printf("Could not open");
        return false;
    }
    // Read each word in the file
    char word[LENGTH + 1];
    while (fscanf(source, "%s", word) != EOF)
    {
        int id = hash(word);
        node *n = malloc(sizeof(node));
        strcpy(n->word, word);
        n->next = NULL;
        if (table[id] != NULL)
        {
            n->next = table[id];
        }
        table[id] = n;
        wrdcnt++;
    }

    // Close the dictionary file
    fclose(source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return wrdcnt;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO - run free() on anything malloc()ed.
    // start at first node, store the *next in a temp variable, then free(node).
    int i = 0;
    for (i = 0; i < N; i++)
    {
        node *cursor = table[i];
        node *tmp = table[i];
        while (cursor != NULL)
        {
            tmp = cursor;
            cursor = cursor->next;
            free(tmp);
            delcnt++;
        }
        table[i] = NULL;
    }

    // int err = wrdcnt - delcnt;
    // printf("Relative Memory Link: %i\n", err);

    return true;
}
