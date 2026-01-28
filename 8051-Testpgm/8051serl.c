/* 
     8051serl - test program: print "hello" on serial port at 9600 baud, l
                lightweight version without printf

     20260128, jens with gemini

*/


#include <8051.h>


// Initialize UART (9600 Baud @ 11.0592 MHz)
void serial_init(void) {
    SCON = 0x50;  
    TMOD |= 0x20; 
    TH1 = 0xFD;   
    TR1 = 1;      
    TI = 1;       
}


// low-level character output
void send_char(char c) {
    while (!TI);
    TI = 0;
    SBUF = c;
}


// print a string from code memory
void print_str(char *s) {
    while (*s) {
        send_char(*s++);
    }
}


// lightweight unsigned integer to decimal output
void print_uint(unsigned int n) {
    unsigned char buf[5]; // Max 65535 is 5 digits
    signed char i = 0;

    // Handle 0 explicitly
    if (n == 0) {
        send_char('0');
        return;
    }

    // Extract digits in reverse order
    while (n > 0) {
        buf[i++] = (n % 10) + '0';
        n /= 10;
    }

    // Print digits in correct order
    while (--i >= 0) {
        send_char(buf[i]);
    }
}


void delay_ms(volatile unsigned int ms) {
    volatile unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}


void main(void) {
    unsigned int count = 0;
    serial_init();

    while (1) {
        print_str("hello ");
        print_uint(count);
        print_str("\r\n");

        count++;
        delay_ms(1000);
    }
}
