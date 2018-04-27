from flask import Flask
from blueprints.api import api
import logging
import sys


from werkzeug.local import LocalProxy
from flask import current_app

#from flask_mysqldb import MySQL

import pymysql.cursors
import os

app = Flask(__name__)

#from extensions import mysql
#from flask.extensions import MySQL

#app.config['MYSQL_DATABASE_USER'] = 'cvservice'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'cvservice'
#app.config['MYSQL_DATABASE_DB'] = 'CVSERVICE'
#app.config['MYSQL_DATABASE_HOST'] = 'cvservice-mysql:5001'
#mysql = MySQL()
#mysql.init_app(app



from blueprints.api import api



def get_mysql_connection():
    connection = pymysql.connect(host='cv-service-mysql',
                                 user='root',
                                 password='my-secret-pw',
                                 db='CVSERVICE',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)
    return connection
    
    
    


schema_sql = ""
with open('/schema/schema.sql', 'r') as myfile:
    schema_sql=myfile.readlines()

schema_sql_array = [x.strip() for x in schema_sql] 

example_sql=""
if os.stat('/schema/example.sql'):
    with open('/schema/example.sql', 'r') as myfile:
        example_sql=myfile.readlines()

    example_sql_array = [x.strip() for x in example_sql] 

connection = get_mysql_connection()

try:

    #https://pypi.org/project/PyMySQL/

    with connection.cursor() as cursor:
        #sql = '''SELECT name FROM terms;'''
        
        for line in schema_sql_array:
            if line != "":
                print("line: " +line)
                cursor.execute(line)
        
        
    if  example_sql != "":
          with connection.cursor() as cursor:
              #sql = '''SELECT name FROM terms;'''
              for line in example_sql_array:
                  if line != "":
                      print("line: " +line)
                      cursor.execute(line)
              
              
        
finally:
    connection.close()
       






app.register_blueprint(api, url_prefix='/api')




#@app.after_request
#def add_header(response):
#    response.cache_control.max_age = 30
#    return response

#app.logger.addHandler(logging.StreamHandler(sys.stdout))
#app.logger.setLevel(logging.DEBUG)

#app.logger.debug("Hello World")


#logger = LocalProxy(lambda: current_app.logger)

@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

