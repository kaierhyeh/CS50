#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BUFFER_SIZE 512

int is_jpg(uint8_t *buffer)
{
    if (buffer \
        && *buffer == 0xff \
        && *(buffer + 1) == 0xd8 \
        && *(buffer + 2) == 0xff \
        && (*(buffer + 3) & 0xf0) == 0xe0)
        return 1;
    return 0;
}
// nn & f0: multiplied by f0 in bit operation
//     The first 4 bits are multiplied by 1 and the latter by 0.
//     (nn) x (1111 0000) = (n 0000) = n0
//     Keeping only the first 4 bits.

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");
    if (!card)
    {
        printf("[Error] Invalid image.\n");
        return 1;
    }

    // Create a buffer for a block of data
    uint8_t buffer[BUFFER_SIZE];

    // While there's still data left to read from the memory card
    int i = 0;
    FILE *img = NULL;
    char filename[8];

    while (fread(buffer, 1, BUFFER_SIZE, card))
    {
        // Create JPEGs from the data
        if (is_jpg(buffer))
        {
            if (img)
                fclose(img);
            sprintf(filename, "%03i.jpg", i++);
            img = fopen(filename, "w");
            if (!img)
            {
                printf("[Error] Failed to create image.\n");
                fclose(card);
                return 1;
            }
        }
        if (img)
            fwrite(buffer, 1, BUFFER_SIZE, img);
    }
    if (img)
        fclose(img);
    fclose(card);
    return 0;
}
