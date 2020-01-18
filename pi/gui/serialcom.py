import serial
import json
import time
import glob

from constants import *
from logger import *

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

    logger.info("Serial ports detected: " + str(res))

    return res[0]


class SerialCom:
    def __init__(self):
        self.ser = None
        self.port =  _findPort()
        self.send_delay = 0.08
        self.connected = False

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, 38400, timeout=1,
                                     parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE,
                                     bytesize=serial.EIGHTBITS)
            self.ser.close()
            self.ser.open()
            self.connected = True
        except Exception as e:
            logger.error("Failed to open serial port! " + str(e))
            return False
        else:
            ret = self.sendCmd(START_CMD)
            while not ret:
                if POSITIVE_RESPONSE not in ret:
                    #ret = self.sendCmd(STOP_CMD)
                    ret = self.sendCmd(START_CMD)

            logger.info("Serial port opened & start confirmed.")
            return True

    def disconnect(self):
        ret = self.sendCmd(STOP_CMD)
        while not ret:
            if POSITIVE_RESPONSE not in ret:
                ret = self.sendCmd(STOP_CMD)

        self.connected = False
        try:
            self.ser.close()
        except Exception as e:
            logger.error("Failed to close serial port! " + str(e))
            return False
        else:
            logger.info("Serial port closed & stop confirmed.")
            return True

    def toggle(self):
        if self.connected:
            self.disconnect()
        else:
            self.connect()

    def isConnected(self):
        return self.connected

    def sendCmd(self, cmd):
        if self.isConnected():
            try:
                self.ser.write(cmd.encode('utf-8'))
            except Exception as e:
                logger.error("Failed to send command! " + str(e))
                return ''
            else:
                time.sleep(self.send_delay)
                response = self.ser.readline().decode()
                #print(response)
                return response
        else:
            return ''

    def readAdcData(self):
        ret = self.sendCmd(ADC_CMD)

        try:
            while not ret:
                if POSITIVE_RESPONSE not in ret:
                    ret = self.sendCmd(ADC_CMD)
            adc = json.loads(ret)
            return adc['value']['c0'], adc['value']['c1'], adc['value']['c2'], adc['value']['c3'], adc['value']['c4']

        except Exception as e:
            logger.error("Failed to read ADC data. " + str(e))
            return None, None, None, None, None

    def lightEnable(self, light, enb):
        lightCmd = DIO_CMD + "0" + str(light)  + str(enb) + CMD_TRAILER
        ret = self.sendCmd(lightCmd)
        if POSITIVE_RESPONSE not in ret:
            logger.info("Setting up light "  + str(light) + " failed.")
            return False

        logger.info("Light "  + str(light) + " status " + str(enb) + " updated.")
        return True
