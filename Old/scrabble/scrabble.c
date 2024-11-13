#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    string word[2];
    int wscore[2] = {0, 0};
    word[0] = get_string("Player1: ");
    word[1] = get_string("Player2: ");
    int ltr[27] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10, 0};

    for (int j = 0; j < 2; j++)
    {
        for (int i = 0, n = strlen(word[j]); i < n; i++)
        {
            word[j][i] = toupper(word[j][i]);
            if (word[j][i] < 65 || word[j][i] > 90)
            {
                word[j][i] = 91;
            }
            wscore[j] = wscore[j] + (ltr[(word[j][i] - 64) - 1]);
        }
    }

    if (wscore[0] == wscore[1])
    {
        printf("Tie!\n");
    }
    else if (wscore[0] > wscore[1])
    {
        printf("Player 1 Wins!\n");
    }
    else if (wscore[0] < wscore[1])
    {
        printf("Player 2 Wins!\n");
    }
}
