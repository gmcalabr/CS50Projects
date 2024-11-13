#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    int blocksize = 512;

    // Check command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./recover filename\n");
        return 1;
    }

    // Open input file
    char *cardname = argv[1];
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open %s.\n", cardname);
        return 1;
    }

    // Create a buffer for a block of data
    uint8_t buffer[blocksize];
    int x = 0;
    char filename[8] = {0};
    FILE *img = NULL;
    int flag = 0;

    // while loop
    while (fread(buffer, 1, sizeof(buffer), card) == 512)
    {
        //    Read the first block
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            flag++;
        }
        if (flag != 0)
        {
            //    if block's first 4 bytes indicate a jpeg
            if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
                (buffer[3] & 0xf0) == 0xe0)
            {
                //        if this jpeg is the first jpeg
                if (flag == 1) // first jpeg
                {
                    //            open file
                    sprintf(filename, "%03i.jpg", x);
                    img = fopen(filename, "wb");
                    //            write to that file
                    fwrite(buffer, blocksize, 1, img);
                    memset(buffer, 0, sizeof(buffer));
                }
                //        else if this is a subsequent new jpeg
                else
                {
                    //            close previous file
                    fclose(img);
                    //            iterate x
                    x++;
                    //            change file name
                    sprintf(filename, "%03i.jpg", x);
                    //            open new file
                    img = fopen(filename, "wb");
                    //            write
                    fwrite(buffer, blocksize, 1, img);
                    memset(buffer, 0, sizeof(buffer));
                }
            }
            //    else if this block is not the start of a new jpeg
            else
            {
                //    write new block to existing file
                fwrite(buffer, blocksize, 1, img);
                memset(buffer, 0, sizeof(buffer));
            }
        }
        else if (flag == 0)
        {
        }
    }
    fclose(img);
    fclose(card);
}
