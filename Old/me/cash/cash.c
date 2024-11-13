#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int c = 0;
    // ASK FOR CHANGE HERE
    int n = get_int("How much change have you been handed?\n");
    while (n < 1 || n > 2500)
    {
        printf("We were looking for something between 1 and 100 cents. Try again.\n");
        n = get_int("How much change have you been handed?\n");
    }
    //

    // COUNTING COINS HERE
    while (n > 24)
    {
        n = n - 25;
        c = c + 1;
    }
    while (n > 9)
    {
        n = n - 10;
        c = c + 1;
    }
    while (n > 4)
    {
        n = n - 5;
        c = c + 1;
    }
    while (n > 0)
    {
         n = n - 1;
        c = c + 1;
    }
    //

    // DECLARE COINS HERE
    printf("%i\n", c);
}
