import grpc

# import the generated classes
from protos import greet_pb2
from protos import greet_pb2_grpc

import os
import logging
import flask
from flask import request, jsonify
from flask import json
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)

app = flask.Flask(__name__)
CORS(app)

# initialize the gRPC channel
addr = os.getenv('GRPC_SERVER_ADDRESS', 'localhost:50051')
creds = grpc.ssl_channel_credentials()
channel = grpc.secure_channel(addr, creds)
greeter = greet_pb2_grpc.GreeterStub(channel)

@app.route('/hello', methods=['GET'])
def getHello():
    req = 100
    for x in range(req):
      myhost = os.uname()[1]
      helloRequest = greet_pb2.HelloRequest(name='%s' % myhost) 
      response = greeter.SayHello(helloRequest, timeout=25)
      return response.message

app.run(host='0.0.0.0', port=os.getenv('PORT', '8050'))