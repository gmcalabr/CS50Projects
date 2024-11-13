#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool onlyDigits(string x);

int main(int argc, string argv[])
{
    string p = 0; // p is plaintext
    string c = 0; // c is cyphertext
    int k = 0;    // k is the key

    // get plaintext from user
    if (argc == 2)
    {
        // employ onlyDigits()
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            bool YYY = onlyDigits(argv[1]);
            if (YYY == 0)
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
        p = get_string("plaintext:  ");
        c = p;
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // convert argv[1] key into integer
    k = atoi(argv[1]);

    // cypher and output
    for (int i = 0, n = strlen(p); i < n; i++)
    {
        char h1 = p[i];
        if (isalpha(h1))
        {
            if (islower(h1))
            {
                int h2 = h1 - 97;
                int h3 = (h2 + k) % 26;
                char h4 = h3 + 97;
                c[i] = h4;
            }
            else if (isupper(h1))
            {
                int h2 = h1 - 65;
                int h3 = (h2 + k) % 26;
                char h4 = h3 + 65;
                c[i] = h4;
            }
        }
    }
    printf("ciphertext: %s\n", c);
}

// onlyDigits function
bool onlyDigits(string XXX)
{
    int q = 0;

    for (int i = 0, n = strlen(XXX); i < n; i++)
    {
        if (isdigit(XXX[i]) == 0)
        {
            q++;
        }
    }

    if (q > 0)
    {
        return 0;
    }
    else
    {
        return 1;
    }
}
