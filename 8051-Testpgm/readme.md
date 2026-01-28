
8051 Test Programs
------------------


* 8051blkf - test program: blink fast with pattern on port 1
* 8051blks - test program: blink slow with pattern on port 1

* 8051serc - test program: print "hello" on serial port at 9600 baud
* 8051serl - test program: print "hello" on serial port at 9600 baud,
             lightweight version without printf

* 8051mtst - test program: check external RAM


```
> sdcc --code-loc 0x0000 8051blks.c
> sdcc --code-loc 0x0000 8051blkf.c

> sdcc 8051serc.c
> sdcc --code-loc 0x0000 8051serl.c

C:\Users\jentie\Desktop\8051 - Testpgm>sdcc --code-loc 0x0000 8051mtst.c
```



