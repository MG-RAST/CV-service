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



#from flaskext.mysql import MySQL  
#from flask_mysqldb import MySQL
import pymysql.cursors





#logger = logging.getLogger(__name__)
#logger.debug('logged from thread --------------------------------------- ')

api = Blueprint('api', __name__, template_folder='templates')

#from current_app import mysql
#mysql = MySQL()

#logger = logging.getLogger(__name__)

port = 80
#api_url_internal = 'http://localhost'
#api_url = 'http://submission-api'

# modify /etc/hosts/: 127.0.0.1    localhost submission-api
STATUS_Bad_Request = 400  # A client error
STATUS_Unauthorized = 401
STATUS_Not_Found = 404
STATUS_Server_Error = 500


def get_mysql_connection():
    connection = pymysql.connect(host='cv-service-mysql',
                                 user='cvservice',
                                 password='cvservice',
                                 db='CVSERVICE',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)
    return connection

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
        #if status_code and status_code==STATUS_Server_Error:
        #    logger.warning(message)
        #else:
        #    logger.debug(message)
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

@api.route('/term', methods=['GET', 'POST'])
def api_term_root():
    #current_app.logger.info('submit ---------------------------------------')
    logger=current_app.logger
    result =None
    connection = get_mysql_connection()
    
    
    if request.method == 'GET':
    
        try:
       
            #https://pypi.org/project/PyMySQL/
        
        
            with connection.cursor() as cursor:
                sql = '''SELECT name FROM terms;'''
                cursor.execute(sql, ())
                result = cursor.fetchall()
                print(result)
        finally:
            connection.close()
        
        
        result_array = []
        for obj in result:
            result_array.append(obj['name'])
   
    
        return jsonify(
                result_array
        )
        
    elif request.method == 'POST':
        
        input_data = request.get_json()
        #input_data = request.form[0]
        
        new_name = input_data['name']
        synonyms  = None
        
        if "synonyms" in input_data:
            synonyms = input_data["synonyms"]
        
        # check if exists
        try:
       
            #https://pypi.org/project/PyMySQL/
        
        
            with connection.cursor() as cursor:
                # Read a single record
                #sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = '''SELECT `name`,`id` from `terms` WHERE name=%s'''
                cursor.execute(sql, (new_name))
                result = cursor.fetchone()
                print(result)
        
        finally:
            pass
        
        if result != None:
            if len(result) > 0:
                connection.close()
                
                raise InvalidUsage('Entry already exists', status_code=409)
                
        
        # insert term
        try:
       
            #https://pypi.org/project/PyMySQL/
        
        
            with connection.cursor() as cursor:
                
                sql = '''INSERT INTO `terms` (`name`) VALUES (%s)'''
                print(sql)
                cursor.execute(sql, (new_name,))
                result = cursor.fetchone()
                print(result)
                
                cursor.execute(sql, (new_name,))
                
        finally:
            connection.commit()
        
        
        try:
       
            #https://pypi.org/project/PyMySQL/
            with connection.cursor() as cursor:
                
                sql = '''SELECT `id` FROM `terms` WHERE `name`=%s'''
                print(sql)
                cursor.execute(sql, (new_name,))
                result = cursor.fetchone()
                print(result)
        finally:
            pass
            
        
        if not 'id' in result:
            raise InvalidUsage('field id not in result', status_code=400)
            
            
            
        new_id = result['id']
        if new_id == None:
            raise InvalidUsage('id is empty', status_code=400)
        
        # insert synonyms
        if synonyms != None:
            
            for synonym in synonyms:
                try:
                    #https://pypi.org/project/PyMySQL/
                    with connection.cursor() as cursor:
                
                       sql = '''INSERT INTO `synonyms` (`id`, `synonym`) VALUES (%s, %s);'''
                       print(sql)
                       cursor.execute(sql, (new_id, synonym,))
                       result = cursor.fetchone()
                       print(result)
                
                       
                finally:
                    pass
        
            
        
        
        api_result = get_object(connection, str(new_id))
        
        connection.close()
        
        
        
        
        return jsonify(
                api_result
        )
        
    
    
    raise MyException("not supported")
        



def get_object(connection, id_str):
    print("id_str: "+id_str)
    print("id_str type: "+str(type(id_str)))
    try:
       
        #https://pypi.org/project/PyMySQL/
        
        with connection.cursor() as cursor:
           
            sql = '''SELECT t.id, t.name, s.synonym FROM terms t, synonyms s  WHERE t.id = s.id AND t.id = %s;'''
            print("B id_str: "+id_str)
            print(sql)
            cursor.execute(sql, (id_str))
            result_array = cursor.fetchall()
            print("get_object got:"+str(result_array))
    except Exception as e:
        raise InvalidUsage("(get_object) "+str(e), status_code=400)
        
    api_result = {
       'id' : result_array[0]['id'],
       'name' : result_array[0]['name']
    }
       
    synonyms_array = []
   
    for obj in result_array:
        synonyms_array.append(obj['synonym'])
   
    api_result['synonyms'] = synonyms_array
    
    return api_result
        


@api.route('/id/<id_str>')
def api_id(id_str):
    #current_app.logger.info('submit ---------------------------------------')
    logger=current_app.logger
    result =None
    connection = get_mysql_connection()
    
      
    api_result = get_object(connection, str(id_str))
    
    connection.close()
    
    return jsonify(
           api_result
    )
   


@api.route('/term/<term>')
def api_term(term):
    #current_app.logger.info('submit ---------------------------------------')
    logger=current_app.logger
    result =None
    connection = get_mysql_connection()
    try:
       
        #https://pypi.org/project/PyMySQL/
        
        
        with connection.cursor() as cursor:
            # Read a single record
            #sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            #sql = '''SELECT t.id, t.name, GROUP_CONCAT(s.synonym) FROM terms t, synonyms s  WHERE t.id = s.id AND t.id = %s GROUP BY t.id;'''
            sql = '''SELECT t.id, t.name, s.synonym FROM terms t, synonyms s  WHERE t.id = s.id AND t.name = %s;'''
            cursor.execute(sql, (term))
            result = cursor.fetchall()
            print(result)
    finally:
        connection.close()
        
    
    api_result = {
        'id' : result[0]['id'],
        'name' : result[0]['name']
    }
        
    synonyms_array = []
    
    for obj in result:
        synonyms_array.append(obj['synonym'])
    
    api_result['synonyms'] = synonyms_array
  
    return jsonify(
            api_result
    )


@api.route('/testing')
def api_testing():
    return 'this is a test'


@api.route('/')
def api_root():
    return 'This is the CV server.\n'

