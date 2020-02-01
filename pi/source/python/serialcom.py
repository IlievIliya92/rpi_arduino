import json
import time
import glob

from serial import *
from constants import *
from logger import *

def _findPorts():
    ports = glob.glob('/dev/ttyACM[0-9]*')

    res = []
    for port in ports:
        s = Serial(port)
        s.close()
        res.append(port)

    logger.info("Serial ports detected: " + str(res))

    return res


class SerialCom:
    def __init__(self, dev_id):
        self.ser = None
        self.send_delay = 0.08
        self.connected = False
        self.dev_id = dev_id
        try:
            self.ports = _findPorts()
        except Exception as e:
            logger.error("Failed to find the serial device! " + str(e))


    def verifyResponse(self, response):
        if POSITIVE_RESPONSE in response:
            return True
        else:
            return False

    def connect(self):
            for port in self.ports:
                try:

                    self.ser = Serial(port, 38400, timeout=1,
                                      parity=PARITY_NONE,
                                      stopbits=STOPBITS_ONE,
                                      bytesize=EIGHTBITS)
                    self.ser.close()
                    self.ser.open()
                except Exception as e:
                    logger.error("Failed to open serial port! " + str(e))
                    return False
                else:
                    ret = self.sendCmd(START_CMD)
                    while not self.verifyResponse(ret):
                        ret = self.sendCmd(STOP_CMD)
                        ret = self.sendCmd(START_CMD)

                    device_ID = json.loads(ret)['ID']
                    if device_ID == self.dev_id:
                        logger.info("Serial port opened & start confirmed.")
                        self.connected = True
                        return True
                    else:
                        self.connected = False
                        logger.info("Failed to recognize serial device.")

            return False

    def disconnect(self):
        ret = self.sendCmd(STOP_CMD)
        while not self.verifyResponse(ret):
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

    def isConnected(self):
        return self.connected

    def sendCmd(self, cmd):
            try:
                self.ser.write(cmd.encode('utf-8'))
            except Exception as e:
                logger.error("Failed to send command! " + str(e))
                return ''
            else:
                time.sleep(self.send_delay)
                response = self.ser.readline().decode()
                return response

    def readAdcData(self):
        ret = self.sendCmd(ADC_CMD)

        try:
            while not self.verifyResponse(ret):
                ret = self.sendCmd(ADC_CMD)

            adc = json.loads(ret)
            return adc['value']['c0'], adc['value']['c1'], adc['value']['c2'], adc['value']['c3'], adc['value']['c4']

        except Exception as e:
            logger.error("Failed to read ADC data. " + str(e))
            return None, None, None, None, None

    def lightEnable(self, light, enb):
        lightCmd = DIO_CMD + "0" + str(light)  + str(enb) + CMD_TRAILER
        ret = self.sendCmd(lightCmd)
        if not self.verifyResponse(ret):
            logger.info("Setting up light "  + str(light) + " failed.")
            return False

        logger.info("Light "  + str(light) + " status " + str(enb) + " updated.")
        return True
