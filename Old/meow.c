#include <stdio.h>

int main(void)
{
    int i = 0;
    while (i < 3)
    {
        printf("meow\n");
        i++;
    }

    printf("or, here's another way to do this \n");

    for (int j = 0; j < 3; j++)
        printf("meow\n");

    printf("and if you want this to go on forever, go into this code and remove the bang outs \n");

//    while (true)
//        {
//            printf("meow\m");
//        }
}
