import serial
import time
import glob
import os

cmds = {
        'h': 'S>',
        'start': '01',
        'stop': '05',
        'trl':  '<E*'
        }

pwmCmd = {
          'cmdid': '02',
          'channels':['00', '01'],
          'dcycle':[100, 1300, 50]
          }

dioCmd = {
          'cmdid': '03',
          'dios': 5
          }

adcCmd = {
            'cmdid': '04'
         }

class TestCmd:
    def __init__(self, br = 38400, timeout = 1):
        self.port = self.findPort()
        self.ser = self.openSerial(br, timeout)
        self.sendDelay = 0.2
        self.send_data_len = 10


    def findPort(self):
        ports = glob.glob('/dev/ttyACM[0-9]*')

        res = []
        for p in ports:
            try:
                s = serial.Serial(p)
                s.close()
                res.append(p)
            except:
                pass

        return res[0]

    def openSerial(self, br, tm):
        try:
            ser = serial.Serial(self.port, br, parity = serial.PARITY_NONE,
                                stopbits = serial.STOPBITS_ONE,
                                bytesize = serial.EIGHTBITS,
                                timeout=tm)
            ser.close()
            ser.open()
        except Exception as e:
            print(e)
            os.exit()
        else:
            return ser

    def sendCmd(self, data):
        cmd = cmds['h'] + data + cmds['trl']
        print(cmd)
        try:
            self.ser.write(cmd.encode())
            time.sleep(self.sendDelay)
            response = self.ser.readline().decode()
        except Exception as e:
            print(e)
            pass
        else:
            return self.verifyResponse(response)

    def verifyResponse(self, response):
        print(response)

        if 'Ok' in response:
            return True
        else:
            return False

    def commStart(self, run):
        ret = False

        if run == 'start':
            ret = self.sendCmd(cmds['start'])
            while not ret:
                ret = self.sendCmd(cmds['stop'])
                ret = self.sendCmd(cmds['start'])
        elif run == 'stop':
            ret = self.sendCmd(cmds['stop'])

        return ret

    def pwmTest(self, ch = 0):
        ret = self.commStart('start')

        print(self.pwmTest.__name__)

        if ret:
            for i in range(self.send_data_len):
                cmd = pwmCmd['cmdid'] + pwmCmd['channels'][ch] + str(pwmCmd['dcycle'][0])
                ret = self.sendCmd(cmd)
                if not ret:
                    print("FAILED!")
                    self.commStart('stop')
                    return

        ret = self.commStart('stop')
        return ret

    def dioTest(self, enb = 0):
        ret = self.commStart('start')

        print(self.dioTest.__name__)

        if ret:
            for i in range(dioCmd['dios']):
                cmd = dioCmd['cmdid'] + "0" + str(i)  + str(enb)
                time.sleep(1)
                ret = self.sendCmd(cmd)
                if not ret:
                    print("FAILED!")
                    self.commStart('stop')
                    return

        ret = self.commStart('stop')
        return ret


    def adcTest(self):
        ret = self.commStart('start')

        print(self.adcTest.__name__)

        if ret:
            ret = self.sendCmd(adcCmd['cmdid'])
            if not ret:
                print("FAILED!")
                self.commStart('stop')
                return

        ret = self.commStart('stop')
        return ret


    def close(self):
        self.ser.close()

def main():

    testCmds = TestCmd()

    if testCmds.pwmTest(0):
        print("PWM ch0 test passed")
    else:
        print("PWM ch0 test failed")
    time.sleep(1)

    if testCmds.pwmTest(1):
        print("PWM ch1 test passed")
    else:
        print("PWM ch1 test failed")
    time.sleep(1)

    if testCmds.dioTest(1):
        print("DIO on test passed")
    else:
        print("DIO on test failed")
    time.sleep(1)

    if testCmds.dioTest(0):
        print("DIO off test passed")
    else:
        print("DIO off test failed")
    time.sleep(1)

    if testCmds.adcTest():
        print("Adc test passed")
    else:
        print("Adc test failed")
    time.sleep(1)

    testCmds.close()

if __name__ == "__main__":
    main()
