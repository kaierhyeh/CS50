// This assignment is seriously not easy :(((((

#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Rounding is needed to maintain precision.
            BYTE average = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);

            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE tmp = image[i][j];

            tmp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = tmp;
        }
    }
    return;
}

// Blur image
void blur_color(int height, int width, RGBTRIPLE image[height][width], \
                    int i, int j, RGBTRIPLE tmp[height][width])
{
    int r = 0, g = 0, b = 0;
    int count = 0;

    for (int x = -1; x <= 1; x++)
    {
        for (int y = -1; y <= 1; y++)
        {
            int neighbor_x = i + x;
            int neighbor_y = j + y;

            if (0 <= neighbor_x && neighbor_x < height \
                && 0 <= neighbor_y && neighbor_y < width)
            {
                r += image[neighbor_x][neighbor_y].rgbtRed;
                g += image[neighbor_x][neighbor_y].rgbtGreen;
                b += image[neighbor_x][neighbor_y].rgbtBlue;
                count++;
            }
        }
    }
    // Need to cast into double so as not to lose precision.
    tmp[i][j].rgbtRed = round((double) r / count);
    tmp[i][j].rgbtGreen = round((double) g / count);
    tmp[i][j].rgbtBlue = round((double) b / count);
}

void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp[height][width];

    for (int i = 0; i < height; i++)
        for (int j = 0; j < width; j++)
            blur_color(height, width, image, i, j, tmp);
    for (int i = 0; i < height; i++)
        for (int j = 0; j < width; j++)
            image[i][j] = tmp[i][j];
    return;
}

// Detect edges
int root_mean_square(int Gx, int Gy)
{
    double color = round(sqrt(Gx * Gx + Gy * Gy));

    if (color > 255)
        color = 255;
    return (int) color;
}

// Gx 和 Gy 是以中心像素為計算點的加權表。
// 計算平方時，Gx^2 + Gy^2 是用每個通道的 Gx 和 Gy 值平方後相加，然後取平方根，得到最終顏色值。
void edge_color(int height, int width, RGBTRIPLE image[height][width], \
                    int i, int j, RGBTRIPLE tmp[height][width])
{
    int Gx[3][3] = {{-1, 0, 1},
                    {-2, 0, 2},
                    {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1},
                    {0, 0, 0},
                    {1, 2, 1}};
    int Gx_r = 0, Gx_g = 0, Gx_b = 0;
    int Gy_r = 0, Gy_g = 0, Gy_b = 0;

    for (int x = -1; x <= 1; x++)
    {
        for (int y = -1; y <= 1; y++)
        {
            int neighbor_x = i + x;
            int neighbor_y = j + y;

            if (0 <= neighbor_x && neighbor_x < height \
                && 0 <= neighbor_y && neighbor_y < width)
            {
                // cuz x and y start from -1.
                Gx_r += image[neighbor_x][neighbor_y].rgbtRed * Gx[x + 1][y + 1];
                Gx_g += image[neighbor_x][neighbor_y].rgbtGreen * Gx[x + 1][y + 1];
                Gx_b += image[neighbor_x][neighbor_y].rgbtBlue * Gx[x + 1][y + 1];
                Gy_r += image[neighbor_x][neighbor_y].rgbtRed * Gy[x + 1][y + 1];
                Gy_g += image[neighbor_x][neighbor_y].rgbtGreen * Gy[x + 1][y + 1];
                Gy_b += image[neighbor_x][neighbor_y].rgbtBlue * Gy[x + 1][y + 1];
            }
        }
    }
    tmp[i][j].rgbtRed = root_mean_square(Gx_r, Gy_r);
    tmp[i][j].rgbtGreen = root_mean_square(Gx_g, Gy_g);
    tmp[i][j].rgbtBlue = root_mean_square(Gx_b, Gy_b);
}
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp[height][width];

    for (int i = 0; i < height; i++)
        for (int j = 0; j < width; j++)
            edge_color(height, width, image, i, j, tmp);
    for (int i = 0; i < height; i++)
        for (int j = 0; j < width; j++)
            image[i][j] = tmp[i][j];
    return;
}
