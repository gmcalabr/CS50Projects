#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    string blurb = get_string("Text: ");
    int values[3] = {0, 0, 0};

    for (int i = 0, n = strlen(blurb); i < n; i++)
    {
        blurb[i] = toupper(blurb[i]);
    }

    for (int i = 0, n = strlen(blurb); i < n; i++)
    {
        if (blurb[i] == 33 || blurb[i] == 46 || blurb[i] == 63)
        {
            values[0]++;
        }
        else if (blurb[i] == 32)
        {
            values[1]++;
        }
        else if (blurb[i] >= 65 && blurb[i] <= 90)
        {
            values[2]++;
        }
    }

    float l = values[2] * (100.0 / (values[1] + 1));
    float s = values[0] * (100.0 / (values[1] + 1));
    float index = 0.0588 * l - 0.296 * s - 15.8;
    double grade = round(index);

    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int) grade);
    }
}
