#include <cs50.h>
#include <stdio.h>
#include <string.h>

void draw(int n);

int main(void)
{
    int height = get_int("Height: ");
    draw(height);
}

void draw(int n)
{
    //if array length is less than 2, merge
    //declare left variable to 0 and right variable to n-1
    //find mid by medium mid = (left+right)/2
    //create secondary array for left half
    //create secondary array for right half
    //call sort of left half
size of left = size of list/2
left = array[0 to size of left]

size of right = size of list-size of left



    if (n <=0)
    {
        return;
    }

    draw(n - 1);

    for (int i = 0; i < n; i++)
    {
        printf("#");
    }
    printf("\n");
}
