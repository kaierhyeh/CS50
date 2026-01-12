#include <cs50.h>
#include <math.h>
#include <stdio.h>

int check_digit(long n)
{
    int digit = 1;
    long i = 10;

    if (0 <= n && n <= 9)
        return digit;
    while (10 <= n)
    {
        n /= i;
        digit++;
    }
    return digit;
}

long Luhn_extract(long n, int d, bool even_digit)
{
    long r;
    long result = 0;

    if (even_digit)
        n /= 10;
    for (int i = 0; i < d; i++)
    {
        r = n % 10;
        if (even_digit)
            r *= 2;
        if (9 < r)
            result += r / 10 + r % 10;
        else
            result += r;
        n /= 100;
    }
    return result;
}

long Luhn(long n)
{
    long res;

    res = Luhn_extract(n, check_digit(n), 1) + Luhn_extract(n, check_digit(n), 0);
    return res;
}

int main(void)
{
    long n = get_long("Number: ");
	int d = check_digit(n);
    long company = n / pow(10, d - 2);

    if (Luhn(n) % 10)
        printf("INVALID\n");
    else
    {
        if (company / 10 == 4 && (d == 13 || d ==  16))
            printf("VISA\n");
        else if ((company == 34 || company == 37) && d == 15)
            printf("AMEX\n");
        else if ((51 <= company && company <= 55) && d == 16)
            printf("MASTERCARD\n");
        else
            printf("INVALID\n"); // Invalid by unknown company.
    }
}
