#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Take average of rgb
            int rval = image[i][j].rgbtRed;
            int gval = image[i][j].rgbtGreen;
            int bval = image[i][j].rgbtBlue;
            int wval = round(((float) rval + (float) gval + (float) bval) / 3);
            // Update pixel values
            image[i][j].rgbtRed = wval;
            image[i][j].rgbtGreen = wval;
            image[i][j].rgbtBlue = wval;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Take original RGB values
            float originalRed = image[i][j].rgbtRed;
            float originalGreen = image[i][j].rgbtGreen;
            float originalBlue = image[i][j].rgbtBlue;
            // Convert to sepia RGB values
            int sepiaRed = round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue);
            int sepiaGreen = round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue);
            int sepiaBlue = round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue);
            // Max out each RGB value to 255
            if (sepiaRed > 255)
                sepiaRed = 255;
            if (sepiaGreen > 255)
                sepiaGreen = 255;
            if (sepiaBlue > 255)
                sepiaBlue = 255;
            // Update pixel values
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int halfwidth = round(width / 2);
    for (int i = 0; i < height; i++)
        {
            for (int j = 0; j < halfwidth ; j++)
            {
                //get original pixel value 1 and store into temp
                int Red1 = image[i][j].rgbtRed;
                int Green1 = image[i][j].rgbtGreen;
                int Blue1 = image[i][j].rgbtBlue;
                //get original pixel value 2
                int Red2 = image[i][(width-1)-j].rgbtRed;
                int Green2 = image[i][(width-1)-j].rgbtGreen;
                int Blue2 = image[i][(width-1)-j].rgbtBlue;
                //write original pixel value 1 into pixel value 2 original
                image[i][(width-1)-j].rgbtRed = Red1;
                image[i][(width-1)-j].rgbtGreen = Green1;
                image[i][(width-1)-j].rgbtBlue = Blue1;
                //write original pixel value 2 into pixel value 1 original
                image[i][j].rgbtRed = Red2;
                image[i][j].rgbtGreen = Green2;
                image[i][j].rgbtBlue = Blue2;
            }
        }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }
    // Read original pixel 3x3 grid from copy
    // Start the image i x j
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
    // Zero out the blurGrid and valid pixel count
            int validPX = 0;
            int expSumR = 0;
            int expSumG = 0;
            int expSumB = 0;
    // Start exposureSum "exposure" x x y
            for (int x = 0; x < 3; x++)
            {
                for (int y = 0; y < 3; y++)
                {
                    int posx = i + x - 1;
                    int posy = j + y - 1;
                    if(posx >= 0 && posx < height && posy >= 0 && posy < width)
                    {
                        expSumR += copy[posx][posy].rgbtRed;
                        expSumG += copy[posx][posy].rgbtGreen;
                        expSumB += copy[posx][posy].rgbtBlue;
                        validPX++;
                    }
                }
            }
    // Divide collected exposure and overwrite original image pixels
            if (validPX != 0)
            {
                image[i][j].rgbtRed = round((float) expSumR / validPX);
                image[i][j].rgbtGreen = round((float) expSumG / validPX);
                image[i][j].rgbtBlue = round((float) expSumB / validPX);
            }
        }
    }
    return;
}
