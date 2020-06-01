#!/usr/bin/python3

import json
import time
import glob

from serial import *
from constants import *
from logger import *
from threading import Lock

# --- Constants --- #
# --- Arduino Serial Commands --- #
cmds = {
        'h': 'S>',
        'start': '01',
        'pwm': '02',
        'dio': '03',
        'adc': '04',
        'stop': '05',
        'trl':  '<E*'
        }


START_CMD = cmds['h'] + cmds['start'] + cmds['trl']
STOP_CMD = cmds['h'] + cmds['stop'] + cmds['trl']
ADC_CMD = cmds['h'] + cmds['adc'] + cmds['trl']
DIO_CMD = cmds['h'] + cmds['dio']

POSITIVE_RESPONSE = "Ok"


# --- Local helper functions --- #

def _findPorts():
    ports = glob.glob('/dev/ttyACM[0-9]*')

    res = []
    for port in ports:
        s = Serial(port)
        s.close()
        res.append(port)

    logger.info("Serial ports detected: " + str(res))

    return res

# --- Interface class --- #

class SerialCom:
    def __init__(self, dev_id):
        self.ser = None
        self.send_delay = 0.001
        self.connected = False
        self.dev_id = dev_id
        self.busy = False
        self.mutex = Lock()

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

                    self.ser = Serial(port, 115200, timeout=1,
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
                        logger.info("Arduino device with ID: %s found on port: %s." % (self.dev_id, port))
                        logger.info("Serial port opened & started confirmed.")
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
                self.mutex.acquire()
                logger.debug(cmd)
                self.ser.write(cmd.encode('utf-8'))
            except Exception as e:
                logger.error("Failed to send command! " + str(e))
                response = ''
            else:
                time.sleep(self.send_delay)
                response = self.ser.readline().decode()
                logger.debug(response)
            finally:
                self.mutex.release()
                return response


    def isBusy(self):
        return self.mutex.locked()

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
        lightCmd = DIO_CMD + "0" + str(light)  + str(enb) + cmds['trl']
        ret = self.sendCmd(lightCmd)
        if not self.verifyResponse(ret):
            logger.info("Setting up light "  + str(light) + " failed.")
            return False

        logger.info("Light "  + str(light) + " status " + str(enb) + " updated.")
        return True




