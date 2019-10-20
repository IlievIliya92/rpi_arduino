import serial
import time

port = "/dev/ttyACM0"

        # VAlid
cmds = ["S>01<E*", "S>0401DATA<E*", \
        # Invalid
        "0101DAdsdddddddddddddddddTAdssdasdas*",
        "S>0101DAdsdddddddddddddddddTAdssdasdas<E*",
        "S>0101DAdsdddddddddddddddddTAdssdasdas*"]

try:
    ser = serial.Serial(port, 9600, timeout=5)
    ser.close()
    ser.open()

    for data in cmds:
        ser.write(data.encode())
        time.sleep(2)
        read_val = ser.readline()
        print(read_val)
except serial.SerialException:
    pass
