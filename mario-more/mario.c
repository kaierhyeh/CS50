#include <cs50.h>
#include <stdio.h>

void build(int n);

int main(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || 8 < n);
    build(n);
}

void build(int n)
{
    for (int i = 0; i < n; i++)
    {
        for (int space = 0; space < n - i - 1; space++)
            printf(" ");
        for (int block = 0; block <= i; block++)
            printf("#");
        printf("  ");
        for (int block = 0; block <= i; block++)
            printf("#");
        printf("\n");
    }
}
