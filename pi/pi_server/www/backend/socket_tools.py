import os
import stat
import socket
import time
import json

SOCKET_RCV_BUF_SIZE = 1024

# ---------- Global Vars -----------

def isSocket(path):
    # https://stackoverflow.com/questions/17877296/checking-if-path-is-a-socket-in-python-2-7
    result = False

    try:
        mode = os.stat(path).st_mode
        result = stat.S_ISSOCK(mode)
    except:
        pass

    return result

def unixDatagramSend(socket_file, msg):
    # http://www.velvetcache.org/2010/06/14/python-unix-sockets

    # send msg
    client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    client.connect(socket_file)
    client.sendall(msg.encode('utf-8'))
    client.close()

def unixStreamingSendReceiveJson(socket_file, send, timeout = 5):
    if(isSocket(socket_file)):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(socket_file)
        sock.sendall(send.encode())
        response = unixStreamingRecvJson(sock, SOCKET_RCV_BUF_SIZE, timeout)
        sock.close()
    else:
        response = None

    # Return response
    return response

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

def unixStreamingRecvJson(sock, rcv_buff_size, timeout):
    data = ''
    deadline = time.time() + timeout
    sock.setblocking(0)
    while True:
        timeleft = deadline - time.time()
        if timeleft < 0.0:
            # print("Socket timed out! got: " + str(data))
            data = None
            break;
        try:
            package = None
            package = sock.recv(rcv_buff_size)
            package = package.decode('utf-8')
        except socket.error as socket_error:
            # print("Socket errored: %d timeleft %f" % (socket_error.errno, timeleft))
            if len(data) > 0 and is_json(data):
                break
            else:
                time.sleep(0.001)

        if package:
            # print("Got %d bytes" % len(package))
            data += package

    return data


# ----------- TEST ------------
if __name__ == "__main__":
    import unittest
    import subprocess

    class TestSocketTools1(unittest.TestCase):
        def test_isSocket_on_non_sockets(self):
            # isSocket must return false without crash on missing files, dirs, block devices
            self.assertFalse(isSocket("/tmp"))
            self.assertFalse(isSocket("/dev/sda"))
            os.system("touch /tmp/normalfile")
            self.assertFalse(isSocket("/tmp/normalfile"))
            os.system("rm /tmp/normalfile")
            self.assertFalse(isSocket("/tmp/normalfile"))


    class TestSocketTools2(unittest.TestCase):
        def setUp(self):
            # For this test, we will setup a unix datagram receive socket
            os.system("rm -f /tmp/testsocket /tmp/testout")

            self.sp = subprocess.Popen("socat UNIX-RECVFROM:/tmp/testsocket,fork OPEN:/tmp/testout,create &", shell=True)
            time.sleep(0.5)

        def tearDown(self):
            try:
                self.sp.terminate()
                self.sp.wait()
            except:
                pass

            os.system("rm -f /tmp/testsocket /tmp/sockout")

        def test_isSocket_unixDatagramSend(self):
            self.assertTrue(isSocket("/tmp/testsocket"))

            unixDatagramSend("/tmp/testsocket", "test message")
            time.sleep(0.5)

            with open("/tmp/testout") as f:
                self.assertEqual(f.read(), "test message")


    unittest.main()
