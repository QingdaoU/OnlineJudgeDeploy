#include <stdio.h>

void unbuffer() __attribute__((constructor));

void unbuffer()
{
    setvbuf(stdout, NULL, _IONBF, 0);
}