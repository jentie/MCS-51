/*
	8051mtst - test program: check external RAM

	20260128, jens with gemini

*/


#include <8051.h>
#include <stdio.h>


// init serial interface (9600 Baud @ 11.0592 MHz)
void serial_init(void) {
    SCON = 0x50;  // 8-Bit UART
    TMOD |= 0x20; // timer 1, mode 2
    TH1 = 0xFD;   
    TR1 = 1;      
    TI = 1;       
}


int putchar(int c) {
    while (!TI);
    TI = 0;
    SBUF = (char)c;
    return c;
}


void main(void) {
    // pointer to external / data memory (XDATA)
    __xdata unsigned char *ptr;
    volatile unsigned char val;		// val can change outside program
    unsigned char cnt;
    unsigned int addr;

    serial_init();
    printf("\n8051 RAM test\r\n");
    printf("sequence: write 0x00 -> write 0xAA -> write 0x55 -> read & check\r\n");

    addr = 0x0000;
    for (cnt = 0; cnt < 16; cnt++) {

        ptr = (__xdata unsigned char *) addr;

        // step 1: init with 0x00
        *ptr = 0x00;
        
        // step 2: write test pattern 0xAA
        *ptr = 0xAA;

        // step 3: write test pattern 0x55
        *ptr = 0x55;

        // step 4: read and check if last pattern
        val = *ptr;

        printf("0x%04X -> read: 0x%02X ", addr, (unsigned int)val);
        
        if (val == 0x55) {
            printf("[OK]\r\n");
        } else {
            printf("[fail]\r\n");
        }

	addr += 0x1000;	    // test in 4K steps (0x1000)
    }

    while(1); 	// stop, no further outputs, restart with reset
}

