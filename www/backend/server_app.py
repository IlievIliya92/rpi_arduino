from flask import Flask
from flask import request
from flask import Response

application = Flask(__name__) #Create FLask appplication

application.config['PROPAGATE_EXCEPTIONS'] = True

def resp_js(s):
    return Response(s, mimetype="application/json")

@application.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@application.route("/backend/test")
def hello():
    status = '{"status":"Ok"}'   
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
    
