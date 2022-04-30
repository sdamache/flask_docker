from logging import debug
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import psycopg2
from psycopg2 import pool
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple


app = Flask(__name__)

# POSTGRES_USER='postgres'
# POSTGRES_PW='Define your own password'
# POSTGRES_HOST="localhost:5432"
# POSTGRES_DB="test"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:' + f'{os.getenv("POSTGRES_PW")}@{os.getenv("POSTGRES_HOST")}/{os.getenv("POSTGRES_DB")}'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
def hello_world():
    return render_template('employee.html')

@app.route("/employee", methods=["GET"])
def employee():
    select_query = '''select * from Employee'''    
    db_conn = db.getconn()
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

    select_query = "select * from Employee where id = "+request.args.get('id')+";"
    db_conn = db.getconn()
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
 