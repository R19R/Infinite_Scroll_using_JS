from flask import Flask, json, request, redirect, render_template, jsonify
import csv
from models import Employee, db
import sqlite3


app=Flask(__name__)
app.secret_key = 'somethingmeanttobesecret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
@app.before_first_request
def create_table():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")



@app.route("/list", methods=['GET'])
def list():
    '''API to read details from csv file'''
    det = []
    with open('mock.csv', 'r') as rfile:
        reader = csv.DictReader(rfile)
        for row in reader:
            detail = dict(row)
            det.append(detail)
        return jsonify(det)


@app.route("/employee", methods=['POST'])
def employee():
    '''API to post details read from csv file into Database'''
    if request.method == 'POST':
        res = request.get_json(force=True)
        id = res.get('id')
        fname = res.get('firstName')
        lname = res.get("lastName")
        dept = res.get("department")
        emp_details = Employee(
            employee_id = id,
            first_name = fname,
            last_name = lname,
            department = dept)
        db.session.add(emp_details)
        db.session.commit()
        return "Details added"
    return "Method is GET"


@app.route("/showdetails", methods=['GET'])
def details():
    '''Reading data from Database'''
    det = []
    cursor_value = request.args.get('cursor')

    connect = sqlite3.connect('employee.db')
    connect.row_factory = sqlite3.Row
    cur = connect.cursor()
    cur.execute("select * from employee")

    if cursor_value == None:
        rows = cur.fetchmany(10) 
        for row in rows:
            det.append({
                'id':row['employee_id'],
                'fname': row['first_name'],
                'lname': row['last_name'],
                'dept': row['department']
            })
        return jsonify({'details_list': det, "cursor":1})
    
@app.route("/otherdetails", methods=['GET'])
def other():
    det = []
    limit = 10
    offset = 10
    
    cursor_value = request.args.get('cursor')
    offset_value = request.args.get('offset')

    connect = sqlite3.connect('employee.db')
    connect.row_factory = sqlite3.Row
    cur = connect.cursor()
    
    if cursor_value == "1":
        if offset_value == 'null':
            cur.execute("select * from employee limit {0} offset {1}".format(limit, offset))
            offset += limit
        else:
            cur.execute("select * from employee limit {0} offset {1}".format(limit, offset_value))
            offset = int(offset_value) + limit
        
        rows = cur.fetchall() 
        if rows == []:
            return jsonify({'info': "No More entries"})
        for row in rows:
            det.append({
                'id':row['employee_id'],
                'fname': row['first_name'],
                'lname': row['last_name'],
                'dept': row['department']
            })
        return jsonify({'details_list': det, "cursor":1, "offset": offset })        


if __name__ == '__main__':
    app.run(debug=True)


