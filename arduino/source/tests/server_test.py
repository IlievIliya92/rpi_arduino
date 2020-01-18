import serial
import time
import glob

send_delay = 0.02
send_data_len = 10

START_CMD = "S>01<E*"
STOP_CMD = "S>05<E*"
ADC_CMD = "S>04<E*"
PWM_CMD = "S>02"
DIO_CMD = "S>03"
CMD_TRAILER = "<E*"

port = ""
ser = ""

def _findPort():
    ports = glob.glob('/dev/ttyACM[0-9]*')

    res = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            res.append(port)
        except:
            pass

    return res[0]


def sendCmd(data):
    global ser

    ser.write(data)
    time.sleep(send_delay)
    response = ser.readline()
    print(response)
    if "Ok" in response:
        return True
    else:
        return False

def run_pwm(pwInit = 300, channel ="00"):
    global ser
    pwmCmd = ""
    pwmCmdPayload = pwInit

    ret = sendCmd(START_CMD)
    while not ret:
        ret = sendCmd(STOP_CMD)
        ret = sendCmd(START_CMD)

    if ret:
        for i in range(send_data_len):
            pwmCmd = PWM_CMD + channel + str(pwmCmdPayload + i*50) + CMD_TRAILER
            print(pwmCmd)
            ret = sendCmd(pwmCmd)
            if not ret:
                sendCmd(STOP_CMD)
                return

            while not ret:
                pass
    sendCmd(STOP_CMD)

def run_dio(enb):
    global ser
    dioCmd = ""

    ret = sendCmd(START_CMD)
    while not ret:
        ret = sendCmd(STOP_CMD)
        ret = sendCmd(START_CMD)

    if ret:
        for i in range(5):
            led = i
            dioCmd = DIO_CMD + "0" + str(led)  + str(enb) + CMD_TRAILER
            print(dioCmd)
            time.sleep(1)
            ret = sendCmd(dioCmd)
            if not ret:
                sendCmd(STOP_CMD)
                return
            while not ret:
                pass
    sendCmd(STOP_CMD)


def run_adc():
    global ser
    dioCmd = ""

    ret = sendCmd(START_CMD)
    while not ret:
        ret = sendCmd(STOP_CMD)
        ret = sendCmd(START_CMD)

    if ret:
        for i in range(5):
            led = i
            adcCmd = ADC_CMD
            print(adcCmd)
            time.sleep(1)
            ret = sendCmd(adcCmd)
            if not ret:
                sendCmd(STOP_CMD)
                return
            while not ret:
                pass
    sendCmd(STOP_CMD)

def main():
    global ser

    port = _findPort()

    try:
        ser = serial.Serial(port, 38400, timeout=1)
        ser.close()
        ser.open()
    except serial.SerialException:
        print("Failed to open the serial port!")
        pass
    else:
        run_pwm()
        run_adc()
        run_dio(1)
        time.sleep(1)
        run_dio(0)

    print("PASSED SUCCESFULY!")

if __name__ == "__main__":
    main()
