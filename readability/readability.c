#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int word_count(string s)
{
    int res = 1;

    for (int i = 0, n = strlen(s); i < n; i++)
        if (s[i] == ' ')
            res++;
    return res;
}

int letter_count(string s)
{
    int res = 0;

    for (int i = 0, n = strlen(s); i < n; i++)
        if (isalpha(s[i]))
            res++;
    return res;
}

int set_count(string s)
{
    int res = 0;

    for (int i = 0, n = strlen(s); i < n; i++)
        if (s[i] == '.' || s[i] == '!' || s[i] == '?')
            res++;
    return res;
}

float index(string s)
{
    float L = (float) letter_count(s) / (float) word_count(s) * 100;
    float S = (float) set_count(s) / (float) word_count(s) * 100;
    float res = 0.0588 * L - 0.296 * S - 15.8;

    return res;
}

int main(void)
{
    string s1 = get_string("Text: ");
    int i = (int) round(index(s1));

    if (i < 1)
        printf("Before Grade 1\n");
    else if (i >= 16)
        printf("Grade 16+\n");
    else
        printf("Grade %i\n", i);
}
