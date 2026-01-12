#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int parse(string s)
{
    int n = strlen(s);
    char str[n];

    if (n != 26)
        return 1;
    for (int i = 0; i < n; i++)
        str[i] = toupper(s[i]);
    for (int i = 0; i < n; i++)
    {
        if (!isalpha(str[i]))
            return 2;
        for (int j = i + 1; j < n; j++)
            if (str[j] == str[i])
                return 3;
    }
    return 0;
}

int *get_key(string s)
{
    char str[26];
    int *d = (int *) malloc(26 * sizeof(int));
    char c = 'A';

    for (int i = 0; i < 26; i++)
        str[i] = toupper(s[i]);
    for (int i = 0; i < 26; i++)
        d[i] = str[i] - c++;
    return d;
}

string encrypt(string s1, int *key)
{
    int n = strlen(s1);
    char str[n];

    for (int i = 0; i < n; i++)
        str[i] = toupper(s1[i]);
    for (int i = 0; i < n; i++)
        if (isalpha(str[i]))
            s1[i] += key[str[i] - 'A'];
    return s1;
}

int main(int ac, string *av)
{
    if (ac != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else
    {
        if (parse(av[1]) == 1)
        {
            printf("[Error] Key must contain 26 characters.\n");
            return 1;
        }
        else if (parse(av[1]) == 2)
        {
            printf("[Error] Key contains non-alphabetical characters.\n");
            return 1;
        }
        else if (parse(av[1]) == 3)
        {
            printf("[Error] Duplicate characters exist.\n");
            return 1;
        }
        else
        {
            string s1 = get_string("plaintext:  ");
            int *key = get_key(av[1]);
            string s2 = encrypt(s1, key);

            printf("ciphertext: %s\n", s2);
            free(key);
        }
    }
    return 0;
}
