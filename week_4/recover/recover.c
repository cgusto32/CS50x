#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Ensure correct usage
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Open the forensic image file
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open file %s.\n", argv[1]);
        return 1;
    }

    // Buffer to hold 512-byte blocks
    BYTE buffer[512];

    // Variables to track JPEG files
    FILE *img = NULL;
    int file_count = 0;
    char filename[8];

    // Read the forensic image file in 512-byte chunks
    while (fread(buffer, sizeof(BYTE), 512, file) == 512)
    {
        // Check if the block starts with a JPEG header
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // If a JPEG file is already open, close it
            if (img != NULL)
            {
                fclose(img);
            }

            // Create a new JPEG file
            sprintf(filename, "%03i.jpg", file_count);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                printf("Could not create file %s.\n", filename);
                fclose(file);
                return 1;
            }

            file_count++;
        }

        // If a JPEG file is open, write to it
        if (img != NULL)
        {
            fwrite(buffer, sizeof(BYTE), 512, img);
        }
    }

    // Close any remaining open files
    if (img != NULL)
    {
        fclose(img);
    }
    fclose(file);

    return 0;
}
