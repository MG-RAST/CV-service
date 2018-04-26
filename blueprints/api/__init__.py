from flask import Blueprint
from flask import Response
from flask import request
from flask import jsonify
#from flask import stream_with_context
import uuid
import logging
import re
import sys
import os
import time
import subprocess
import psutil
import json

from flask import current_app

from subprocess import Popen, PIPE, STDOUT
sys.path.append("../..")
#import export
sys.path.pop()
sys.path.append("..")





#logger = logging.getLogger(__name__)
#logger.debug('logged from thread --------------------------------------- ')

api = Blueprint('api', __name__, template_folder='templates')

#logger = logging.getLogger(__name__)

port = 80
#api_url_internal = 'http://localhost'
#api_url = 'http://submission-api'

# modify /etc/hosts/: 127.0.0.1    localhost submission-api
STATUS_Bad_Request = 400  # A client error
STATUS_Unauthorized = 401
STATUS_Not_Found = 404
STATUS_Server_Error = 500


def execute_command(command, env):
    #global args
    
    print("execute command")
    
    if env:
        for key in env:
            #print("key: %s" % (key))
            search_string = "${"+key+"}"
            #if args.debug:
            #    print("search_string: %s" % (search_string))
            value = env[key]
            command = command.replace(search_string, value)
        
        #if args.debug:
        #   print("exec: %s" % (command), flush=True)
            
        process = subprocess.Popen(command, shell=True,  stdout=PIPE, stderr=STDOUT, close_fds=True, executable='/bin/bash', env=env)
    else:
        #if args.debug:
        print("exec: %s" % (command), flush=True)
        #print("no special environment")
        process = subprocess.Popen(command, shell=True,  stdout=PIPE, stderr=STDOUT, close_fds=True, executable='/bin/bash')
  
    last_line = ''
    while True:
        #print('loop')
        output = process.stdout.readline()
        rc = process.poll()
        if output == '' and process.poll() is not None:
            #print("Cond 1")
            break
        
        if output:
            last_line = output.decode("utf-8").rstrip()
            print(last_line)
        if rc==0:
            #print("Cond 2")
            break
       
    
    #if args.debug:
        #print(last_line)
        
    if process.returncode:
        raise MyException("Command failed (return code %d, command: %s): %s" % (process.returncode, command, last_line[0:500]))    
        
    return last_line


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code and status_code==STATUS_Server_Error:
            logger.warning(message)
        else:
            logger.debug(message)
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@api.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# id, term, synonyms


@api.route('/id/<id_str>')
def api_submit(node_id):
    #current_app.logger.info('submit ---------------------------------------')
    logger=current_app.logger
    #status : submitted | error | complete ,
    #result : null |error-text |  status-id
    logger.info("__ api_submit()  id_str = {}".format(id_str))
    
    node_id = node_id.lower()
    
    result = id_str
    
  
    
    # metadata goes into headers
    
    return jsonify({
            result
    })




@api.route('/testing')
def api_testing():
    return 'this is a test'


@api.route('/')
def api_root():
    return 'This is the CV server.\n'

