import select
import time
import socket
import json
import os

from constants import *
from mgr_serial import *

_socket = None

def _handleCommand(cmd_str):
    response = ""
    command = ""
    print(cmd_str)            
    try:
        command = json.loads(cmd_str)
        cmd_name = command['cmd']          
        cmd_value = command['value']          
        sendData(command['cmd'])
        sendData(command['value'])
        print(cmd_name)
        print(cmd_value)        
        response = '{"status":"Ok"}'
        #response = ktm_callCommand(cmd_name, command)                        
    except Exception as e:
        response = '{"status":"Error: %s"}' % e

    return response

def mgrSocketOpen():
    try:
        os.unlink(SOCKET_FILE_MGR)
    except OSError as e:
        if os.path.exists(SOCKET_FILE_MGR):
            raise

    global _socket
    _socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    _socket.bind(SOCKET_FILE_MGR)

    # queue up as many as 1 connect request
    _socket.listen(1)
    os.chmod(SOCKET_FILE_MGR, 0o777)
    print("Mgr socket opened.")

def mgrSocketService(deadline):
    read_list = [_socket]

    while True:
        time_left = deadline - time.time()

        if time_left <= 0.0:
            if len(read_list) == 1:
                # No time left and read list empty, stop looping
                break;
            time_left = 0.0

        # The select() function will block until one of the socket states has changed or the timeout_in_seconds expiers
        readable, writable, errored = select.select(read_list, [], [], time_left)
        # The server socket will be readable when a new client is waiting
        for s in readable:
            if s is _socket:
                client_socket, address = _socket.accept()
                read_list.append(client_socket)
            else:
                try:
                    data = s.recv(1024)
                    # Decode the data to a string
                    data = data.decode('utf-8')
                except Exception as e:
                    data = None

                if data:
                    try:
                        response = _handleCommand(data)
                        # Encode the data to utf-8
                        s.sendall(response.encode('utf-8'))
                    except Exception as e:
                        response = '{"status":"Command failed"}';
                else:
                    #l.debug("kt_mgr received no data from socket")
                    s.close()
                    read_list.remove(s)
