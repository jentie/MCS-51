# MSCterm

MCSterm - terminal for MCS BASIC-52 on Intel MCS-51 controller

MCSterm is a terminal program for Windows for communicating with systems running MCS BASIC-52. MCS BASIC-52 is a BASIC interpreter that runs on Intel MCS-51 microcontrollers (8051/8052). It is operated via a serial interface using a terminal.

inital revision v0.1

### Connection Setup

After starting MCSterm, you may need to press the space bar to trigger the auto-baud detection of BASIC-52. The BASIC interpreter then responds with a version number and the prompt `>`.

### Operation

In terminal mode, all keystrokes are sent directly to the BASIC interpreter, including Ctrl-C to abort a running program. Pressing the ESC key switches to command mode, where a BASIC program can be loaded from a file or saved to a file, and the terminal program can be exited.

## Requirements

- Python 3.x
- Windows (usage of msvcrt)
- pyserial

> pip install pyserial

## usage 

> MCSterm.py [-p PORT] [-b BAUD]

with
  -p PORT   Serieller Port (default: COM5)
  -b BAUD   Baudrate (default: 9600)

examples:
  python MCSterm.py
  python MCSterm.py -p COM3 -b 19200

  or

  change defaults in Python file and double-click on MCSterm

  
## Important Keys:

  Ctrl+C    sends Ctrl-C to BASIC on controller
 
  ESC       enter command mode

Command mode:
-  c - send Ctrl+C
-  s - show serial status
-  q - quit terminal program
-  u *file* - upload BASIC file
-  d *file* - download BASIC file (dump LIST to file)
-  Enter - back to terminal

