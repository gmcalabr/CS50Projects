#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
} candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

bool vote(string name)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            candidates[i].votes++;
            return true;
        }
    }
    return false;
}

void print_winner(void)
{
    int y1 = 0;
    string x1 = 0;
    int y2 = 0;
    string x2 = 0;
    int y3 = 0;
    string x3 = 0;

    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > y1)
        {
            y1 = candidates[i].votes;
            x1 = candidates[i].name;
        }
        else if (candidates[i].votes == y1)
        {
            if(y1 == y2)
            {
                y3 = candidates[i].votes;
                x3 = candidates[i].name;
            }
            else
            {
                y2 = candidates[i].votes;
                x2 = candidates[i].name;
            }

        }
    }

    printf("%s\n", x1);
    if (y1 == y2)
    {
        printf("%s\n", x2);
    }
    if (y1 == y2 && y2 == y3)
    {
        printf("%s\n", x3);
    }
}
