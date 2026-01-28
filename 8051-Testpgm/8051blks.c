/*
	8051blks - test program: blink slow with pattern on port 1

	20260128, jens with gemini

*/


#include <8051.h>


// gemini: at 11.0592 MHz approx. 120 runs per ms
// copilot: the inner loop count should be closer to 460 (because each iteration is 2 cycles)
void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}


void main(void) {
    while (1) {
        P1 = 0x55;    // pattern 01010101
        delay_ms(500);
        
        P1 = 0xAA;    // pattern 10101010
        delay_ms(500);
    }
}

