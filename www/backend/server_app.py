from flask import Flask
from flask import request
from flask import Response

application = Flask(__name__) #Create FLask appplication

@application.route("/backend/test")
def hello():
    status = '{"status":"Ok"}'   
    return status
    
