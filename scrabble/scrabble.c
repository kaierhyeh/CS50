#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

string toupper_str(string s)
{
    for (int i = 0, n = strlen(s); i < n; i++)
        s[i] = toupper(s[i]);
    return s;
}

int score(string s)
{
    int res = 0;

    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (s[i] == 'A' || s[i] == 'E' || s[i] == 'I' || s[i] == 'L' || s[i] == 'N' ||
            s[i] == 'O' || ('R' <= s[i] && s[i] <= 'U'))
            res += 1;
        else if (s[i] == 'D' || s[i] == 'G')
            res += 2;
        else if (s[i] == 'B' || s[i] == 'C' || s[i] == 'M' || s[i] == 'P' || s[i] == 'N' ||
                 s[i] == 'O' || ('R' <= s[i] && s[i] <= 'U'))
            res += 3;
        else if (s[i] == 'F' || s[i] == 'H' || s[i] == 'V' || s[i] == 'W' || s[i] == 'Y')
            res += 4;
        else if (s[i] == 'K')
            res += 5;
        else if (s[i] == 'J' || s[i] == 'X')
            res += 8;
        else if (s[i] == 'Q' || s[i] == 'Z')
            res += 10;
    }
    return res;
}

int main(void)
{
    string str1 = toupper_str(get_string("Player 1: "));
    string str2 = toupper_str(get_string("Player 2: "));
    printf("str1 = %s\n", str1);
    printf("str2 = %s\n", str2);

    if (score(str1) > score(str2))
        printf("Player 1 wins!\n");
    else if (score(str1) < score(str2))
        printf("Player 2 wins!\n");
    else
        printf("Tie!\n");
}
