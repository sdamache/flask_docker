from logging import debug
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import psycopg2
from psycopg2 import pool
# from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple


app = Flask(__name__)

POSTGRES_USER='postgres'
POSTGRES_PW='root@1234'
POSTGRES_HOST="0.0.0.0:5432"
POSTGRES_DB="postgres"

try:
    db_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PW'), host=os.environ.get('POSTGRES_HOST'), database=os.environ.get('POSTGRES_DB'))
    if not db_pool:
        print("Not able to establish connection with db")
except Exception as e:
    print("Exception while trying to create connection pool %s" % str(e))

@app.route('/')
def hello_world():
    return render_template('employee.html')

@app.route("/employee", methods=["GET"])
def employee():
    select_query = '''SELECT * FROM employee;'''    
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    cursor.execute(select_query)
    lst = cursor.fetchall()
    print("Table content is: ")
    print(lst)
    data = []
    db_conn.close()
    for row in lst:
        print(row)
        data.append(row[1])
    return jsonify(data)

@app.route('/employeeDetails', methods=['GET'])
def employeeDetails():
    # Using Dummy data here. Make a call to db and retrieve all fields of that employee and send it the way I'm sending
    print(request.args.get('id'))
    print(type(request.args.get('id')))

    select_query = "select * from employee where id = "+request.args.get('id')+";"
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    cursor.execute(select_query)
    lst = cursor.fetchall()
    print(lst)
    print(type(lst))
    if lst:
        data = {'Name': lst[0][1], 'Age':lst[0][2], 'Role': 'SD', 'Team': 'Swaas'} 
    else:
        data = {'Name': 'dummy', 'Age':0, 'Role': 'SD', 'Team': 'Swaas'} 
    return jsonify(data)
 
################### MONITORING ###############################################
# provide app's version and deploy environment/config name to set a gauge metric
# register_metrics(app, app_version="v0.1", app_config="staging")


# # Plug metrics WSGI app to your main app with dispatcher
# dispatcher = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})

# run_simple(hostname="0.0.0.0", port=9094, application=dispatcher)
################### MONITORING ###############################################

if __name__ == '__main__':
   app.run(debug=True,host='0.0.0.0',port=5000)

