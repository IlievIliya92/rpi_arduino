import json

from flask import Flask
from flask import request
from flask import Response

from socket_tools import *

application = Flask(__name__) #Create FLask appplication
application.config['PROPAGATE_EXCEPTIONS'] = True

SOCKET_FILE_MGR = "/run/mgr.socket"

def resp_js(s):
    return Response(s, mimetype="application/json")

@application.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@application.route("/backend/test")
def test():
    err = ""
    cmd = ""
    
    # Get all of the arguments from the URL
    args = request.args.to_dict()
    
    for i in sorted(args.keys()):
        cmd += args[i] + " "
    
    if ( len(cmd) == 0 ):
        err = "Failed to get cmd arguments!"
    if len(err) == 0:
        status = run_socket(cmd, SOCKET_FILE_MGR)
    else:
        status = '{"status":"Error: %s"}' % err
  
    return resp_js(status)
    
@application.route("/backend/cmd")
def cmd():
    # Parse the URL arguments
    cmd = request.args.get('cmd')
    value = request.args.get('value')
    
    package = {"cmd":cmd,
               "value":value}
               
    status = run_socket(json.dumps(package), SOCKET_FILE_MGR)
    
    return resp_js(status)
# ---- Utility functions


def run_socket(arg, server_address):
      if arg[-1] != '\n':
          arg += '\n'
      try:
          response = unixStreamingSendReceiveJson(server_address, arg)
      except Exception as e:
          response = '{"status":"Error: %s"}' % repr(e)
      
      if response is None:
          response = '{"status":"Error: Socket didn\'t respond"}'
      return response

def socket_recv(sock, rcv_buff_size, timeout = 1):
  data = b''
  deadline = time.time() + timeout

  while True:
    try:
      time.time() >= deadline
      sock.settimeout(deadline - time.time())
      package = sock.recv(rcv_buff_size)
      data += package
      if len(package) < rcv_buff_size:
          # either 0 or end of data
        break
    except:
      return "Socket timed out!"

  return data    
    
