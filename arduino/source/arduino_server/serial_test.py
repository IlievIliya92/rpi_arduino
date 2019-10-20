
import serial
import time

send_delay = 0.02
send_data_len = 100

port = "/dev/ttyACM0"
ser = ""

        # VAlid
cmds0 = ["S>01<E*", "S>0401DATA<E*", \
        # Invalid
        "0101DAdsdddddddddddddddddTAdssdasdas*",
        "S>0101DAdsdddddddddddddddddTAdssdasdas<E*",
        "S>0101DAdsdddddddddddddddddTAdssdasdas*",
        "S>05<E*",]

cmds1 = ["S>01<E*","S>0401DATA1<E*", "S>05<E*"]

def run_cmds(cmds):
    global ser

    for data in cmds:
        if data == "S>0401DATA1<E*":
            for i in range(send_data_len):
                ser.write(data)
                time.sleep(send_delay)
        ser.write(data)
        time.sleep(send_delay)

def main():
    global ser

    try:
        ser = serial.Serial(port, 38400, timeout=5)
        ser.close()
        ser.open()
    except serial.SerialException:
        print("Failed to open the serial port!")
        pass
    else:
        run_cmds(cmds1)


if __name__ == "__main__":
    main()
