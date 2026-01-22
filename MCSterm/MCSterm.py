#
#   MCSterm - terminal for MCS BASIC-52 on Intel MCS-51 controller
#
#   20260118, Jens with Claude OPUS 4.5R
#   20260122, startup with sending blanks & full line ends for file upload 
#
#   MIT License
#
#   usage: MCSterm [-p PORT] [-b BAUD]
# 


### defaults #####

COMPORT  = 'COM11'
BAUDRATE = 9600

##################

import serial
import threading
import sys
import msvcrt
import signal
import argparse
import time

# global

paused = False
ctrl_c_pressed = False


def sigint_handler(signum, frame):
    global ctrl_c_pressed
    ctrl_c_pressed = True


def read_from_port(ser):
    while ser.is_open:
        try:
            if ser.in_waiting > 0 and not paused:
                data = ser.read(ser.in_waiting).decode('utf-8', errors='replace')
                sys.stdout.write(data)
                sys.stdout.flush()
        except Exception as e:
            print(f"\nserial port reading error: {e}")
            break


def upload_file(ser, filename):
    """BASIC file upload"""
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        print(f"| uploading {filename} ({len(lines)} lines)...")
        
        for i, line in enumerate(lines):
            line = line.rstrip('\r\n')
            if not line:  # skip empty lines
                continue
            
            # send character with delay
            for char in line:
                ser.write(char.encode('utf-8'))
                time.sleep(0.01)  # short delay after each character
                
                # read and display echo
                if ser.in_waiting > 0:
                    data = ser.read(ser.in_waiting).decode('utf-8', errors='replace')
                    sys.stdout.write(data)
                    sys.stdout.flush()
            
            # send line end
            ser.write(b'\r\n')  # both line end for complete lines           
            
            # wait after line
            time.sleep(0.3)
            
            # read and display echo
            while ser.in_waiting > 0:
                data = ser.read(ser.in_waiting).decode('utf-8', errors='replace')
                sys.stdout.write(data)
                sys.stdout.flush()
        
        print(f"| upload complete ({len(lines)} lines)")
        return True
        
    except FileNotFoundError:
        print(f"| error: file '{filename}' not found")
        return False
    except Exception as e:
        print(f"| error: {e}")
        return False


def dump_listing(ser, filename):
    """execute LIST command and write in file"""
    try:
        print(f"| dumping listing to {filename}...")
        
        # clear buffer
        while ser.in_waiting > 0:
            ser.read(ser.in_waiting)
        
        # send LIST command
        ser.write(b'LIST\r')
        
        # collect result 
        output = ""
        timeout = time.time() + 60  # 60s timeout
        ready_found = False
        
        while time.time() < timeout:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting).decode('utf-8', errors='replace')
                output += data
                sys.stdout.write(data)
                sys.stdout.flush()
                
                # detect READY, end of listing 
                if 'READY' in output:
                    ready_found = True
                    break
            time.sleep(0.05)
        
        if not ready_found:
            print("\n| warning: timeout, dump may be incomplete")
        
        # cleanup listing and write
        lines = output.split('\n')
        listing_lines = []
        
        for line in lines:
            line = line.rstrip('\r')
            # delete LIST, READY and empty lines
            if line.strip() == 'LIST':
                continue
            if 'READY' in line:
                continue
            if line.strip() == '>':
                continue
            if line:
                listing_lines.append(line)
        
        with open(filename, 'w') as f:
            f.write('\n'.join(listing_lines))
        
        print(f"\n| dump complete -> {filename} ({len(listing_lines)} lines)")
        return True
        
    except Exception as e:
        print(f"| error: {e}")
        return False


def show_menu():
    print("\n| command mode")
    print("| c          - send ctrl+c")
    print("| s          - serial status")
    print("| u <file>   - upload BASIC file")
    print("| d <file>   - dump LIST to file")
    print("| q          - quit terminal")
    print("| back with enter")


def command_mode(ser):
    global paused
    paused = True
    
    show_menu()

    while True:
        try:
            cmd = input("|> ").strip()
            cmd_lower = cmd.lower()
            
            if cmd == '':
                ser.write(b'\x0D')      # force BASIC prompt
                paused = False
                return True
            
            elif cmd_lower == 'c':
                ser.write(b'\x03')
                print("| ctrl+c sent")
                paused = False
                return True
            
            elif cmd_lower == 's':
                print(f"| port: {ser.port} | baud: {ser.baudrate} | open: {ser.is_open}")
            
            elif cmd_lower.startswith('u '):
                filename = cmd[2:].strip()
                if filename:
                    upload_file(ser, filename)
                    ser.write(b'\x0D')      # force BASIC prompt
                    paused = False
                    return True
                else:
                    print("| usage: u <filename>")

            elif cmd_lower.startswith('d '):
                filename = cmd[2:].strip()
                if filename:
                    dump_listing(ser, filename)
                    ser.write(b'\x0D')      # force BASIC prompt
                    paused = False
                    return True
                else:
                    print("| usage: d <filename>")

            elif cmd_lower == 'q':
                print("| bye")
                return False
            
            else:
                print("| unknown command")
            
        except EOFError:
            return False
        except KeyboardInterrupt:
            print("\n")
            paused = False
            return True


def parse_args():
    parser = argparse.ArgumentParser(
        description='MCSterm - terminal for MCS BASIC-52 on Intel MCS-51 controller'
    )
    parser.add_argument(
        '-p', '--port',
        default=COMPORT,
        help=f'Serial port (default: {COMPORT})'
    )
    parser.add_argument(
        '-b', '--baud',
        type=int,
        default=BAUDRATE,
        help=f'Baud rate (default: {BAUDRATE})'
    )
    return parser.parse_args()


def main():
    global paused, ctrl_c_pressed
    
    args = parse_args()
    
    signal.signal(signal.SIGINT, sigint_handler)
    
    try:
        ser = serial.Serial(args.port, args.baud, timeout=0.1)
        print("| MCSterm - terminal for MCS BASIC-52 on Intel MCS-51 controller")
        print(f"| serial port: {args.port}, {args.baud} baud")
        print("| ctrl-c sends 0x03 to controller")
        print("| ESC - command mode in this terminal")

        read_thread = threading.Thread(target=read_from_port, args=(ser,), daemon=True)
        read_thread.start()

        ser.write(b'  ')      # send blank for baud rate detection, start interactive mode

        ser.write(b'\x0D')    # just in case, force initial BASIC prompt

        while True:
            if ctrl_c_pressed:
                ctrl_c_pressed = False
                ser.write(b'\x03')
                print("^C", end='', flush=True)
            
            if msvcrt.kbhit():
                char = msvcrt.getch()
                
                if char == b'\x1b':  # ESC
                    if not command_mode(ser):
                        break
                    continue
                
                # Backspace (0x08) -> send as DEL (0x7f)
                if char == b'\x08':
                    ser.write(b'\x7f')
                    continue
                
                ser.write(char)

    except serial.SerialException as e:
        print(f"| connection error: {e}")
        time.sleep(1)                       # show message
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("\n| connection closed")
            time.sleep(1)                   # show message

if __name__ == "__main__":
    main()
    
