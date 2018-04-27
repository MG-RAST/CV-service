from flask import Flask
from blueprints.api import api
import logging
import sys


from werkzeug.local import LocalProxy
from flask import current_app

#from flask_mysqldb import MySQL

import pymysql.cursors

app = Flask(__name__)

#from extensions import mysql
#from flask.extensions import MySQL

#app.config['MYSQL_DATABASE_USER'] = 'cvservice'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'cvservice'
#app.config['MYSQL_DATABASE_DB'] = 'CVSERVICE'
#app.config['MYSQL_DATABASE_HOST'] = 'cvservice-mysql:5001'
#mysql = MySQL()
#mysql.init_app(app)








from blueprints.api import api


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

