#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n = get_int("Pyramid Height: ");
    while (n <= 0 || n > 50)
    {
        printf("Please try a more reasonable number.\n");
        n = get_int("Pyramid Height: ");
    }


    while (n < 0);

    for (int i = 0; i < n; i++)
    {
        for (int j = n-1; j >= 0; j--)
        {
            if (j > i)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        printf("  ");
        for (int j = 0; j < n; j++)
        {
            if (j <= i)
            {
                printf("#");
            }
        }
        printf("\n");
    }
}
