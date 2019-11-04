import serial
import sys
import time

send_delay = 0.02
send_data_len = 20


def main():
    portc = "/dev/ttyACM0"
    serc = ""

    try:
        serc = serial.Serial(portc, 38400, timeout=1)
        serc.close()
        serc.open()
    except serial.SerialException:
        print("Failed to open the client serial port!")
        sys.exit()

    ports = "/dev/ttyUSB0"
    sers = ""

    try:
        sers = serial.Serial(ports, 38400, timeout=1)
        sers.close()
        sers.open()
    except serial.SerialException:
        print("Failed to open the server serial port!")
        sys.exit()

    while True:
        cmd = serc.readline()
#        print(cmd)
        time.sleep(0.01)
        sers.write(cmd)

if __name__ == "__main__":
    main()
