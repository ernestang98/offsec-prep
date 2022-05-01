#include <stdio.h>
int main(int argc, char *argv[]) {
	unsigned char s[] =
	{

	    0x60, 0x6b, 0x38, 0xf6, 0xe0, 0x5, 0x3e, 0xba,
	    0xfc, 0x32, 0x75, 0x54, 0x59, 0xe6, 0xc1
	};

	for (unsigned int m = 0; m < sizeof(s); ++m)
	{
	    unsigned char c = s[m];
	    c = ~c;
	    c ^= m;
	    c = -c;
	    c = (c >> 0x2) | (c << 0x6);
	    c ^= 0xe1;
	    c = ~c;
	    c ^= 0x2f;
	    c -= 0x1b;
	    c = (c >> 0x2) | (c << 0x6);
	    c -= 0x6a;
	    c ^= m;
	    c -= m;
	    c ^= m;
	    c = (c >> 0x5) | (c << 0x3);
	    c += m;
	    s[m] = c;
	}
	
	printf("%s\n", s);

	if (strcmp(s, argv[1]) == 0) {
		printf("Correct!\n");
	} else {
		printf("Wrong Password!\n");
	}
}

