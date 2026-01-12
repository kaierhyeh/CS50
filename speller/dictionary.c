// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Choose number of buckets in hash table
const unsigned int N = 20011;

// Hash table
node *table[N];

unsigned int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    unsigned int i = hash(word);
    node *node = table[i];

    while (node)
    {
        if (!strcasecmp(node->word, word))
            return true;
        node = node->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int value = 5381;
    int c;

    while ((c = tolower(*word++)))
        value = value * 3 + c;
    return value % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open the dictionary file
    FILE *source = fopen(dictionary, "r");
    if (!source)
        return false;

    // Read each word in the file
    char word[LENGTH + 1];
    // fscanf stops at whitespaces, ie. \n
    // Using !fscanf will cause infinite loops cuz:
    //     returns  1: successful read
    //     returns  0: failure
    //     returns -1: EOF
    while (fscanf(source, "%s", word) != EOF)
    {
        // Add each word to the hash table
        node *new_node = malloc(sizeof(node));
        if (!new_node)
        {
            fclose(source);
            return false;
        }
        strcpy(new_node->word, word);
        new_node->next = NULL;

        unsigned int i = hash(word);
        if (!table[i])
            table[i] = new_node;
        else
        {
            new_node->next = table[i];
            table[i] = new_node;
        }
        word_count++;
    }

    // Close the dictionary file
    fclose(source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *head = table[i];
        while (head)
        {
            node *temp = head;
            head = head->next;
            free(temp);
        }
    }
    return true;
}
