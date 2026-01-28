/*
	8051serc - test program: print "hello" on serial port at 9600 baud

	20260128, jens with gemini

*/


#include <8051.h>
#include <stdio.h>


int putchar(int c) {
    while (!TI);    // wait until ready
    TI = 0;         // clear flag
    SBUF = (char)c; // send character
    return c;
}


void serial_init(void) {
    SCON = 0x50;  // 8-Bit UART, receive on
    TMOD |= 0x20; // timer 1, modus 2
    TH1 = 0xFD;   // 9600 baud at 11.0592 MHz
    TR1 = 1;      // start timer
    TI = 1;       // set TI
}


void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}


void main(void) {
    unsigned int count = 0;
    
    serial_init();

    while (1) {
        printf("hello %u\r\n", count);
        count++;
        delay_ms(1000);
    }
}
