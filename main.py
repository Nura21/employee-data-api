import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
import requests

@app.route('/employees-create', methods=['POST'])
def createEmployee():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        _json = request.json
        _name = _json['name']
        _first_name = _json['first_name']
        _last_name = _json['last_name']
        _fullname = _json['fullname']
        _company = _json['company']

        if _name and _company and request.method == 'POST':
            sqlQuery = "INSERT INTO employee_name_lists(name) VALUES(%s)"
            bindData = (_fullname)
            cursor.execute(sqlQuery, bindData)

            sqlQuery2 = "INSERT INTO employee_detail_lists(name, first_name, last_name, fullname, company) VALUES(%s, %s, %s, %s, %s)"
            bindData2 = (_name, _first_name,_last_name, _fullname, _company)
            cursor.execute(sqlQuery2, bindData2)
            
            conn.commit()

            response = jsonify('Employee added successfully!')
            response.status_code = 200
            
            print(response)

            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/employees')
def employees():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("SELECT employee_detail_lists.fullname, employee_detail_lists.company, company_detail_lists.domain FROM employee_detail_lists LEFT JOIN company_detail_lists ON employee_detail_lists.company = company_detail_lists.name ORDER BY company_detail_lists.domain")
        employeeRows = cursor.fetchall()
        
        response = jsonify(sorted(employeeRows, key=lambda x: (x["fullname"], x["company"], x["domain"])))
        response.status_code = 200
        
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/employees-works')
def employeeWorks():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("SELECT company_detail_lists.name AS company, employee_detail_lists.fullname AS employees FROM company_detail_lists LEFT JOIN employee_detail_lists ON company_detail_lists.name = employee_detail_lists.company ORDER BY company_detail_lists.name")
        employeeWorkRows = cursor.fetchall()

        company_dict = {}
        for item in employeeWorkRows:
            company = item["company"]
            employee = item["employees"]

            if company not in company_dict:
                company_dict[company] = []
            
            if employee is not None:
                company_dict[company].append(employee)

        result = []
        for company, employees in company_dict.items():
            result.append({
                "company": company,
                "employees": employees
            })

        response = jsonify(sorted(result, key=lambda x: (x["company"], x["employees"])))
        response.status_code = 200
        
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
# @app.route('/todo/<int:todo_id>')
# def todo_details(todo_id):
#     try:
#         conn = mysql.connect()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
        
#         cursor.execute("SELECT * FROM todos WHERE id =%s", todo_id)
#         todoRow = cursor.fetchone()
        
#         response = jsonify(todoRow)
#         response.status_code = 200

#         return response
#     except Exception as e:
#         print(e)
#     finally:
#         cursor.close()
#         conn.close()

@app.route('/employees-update', methods=['PUT'])
def updateEmployee():
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        _first_name = _json['first_name']
        _last_name = _json['last_name']
        _fullname = _json['fullname']
        _company = _json['company']

        if _name and request.method == 'PUT':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            sqlQuery = "UPDATE employee_name_lists SET name=%s WHERE id=%s"
            bindData = (_fullname, _id)
            cursor.execute(sqlQuery, bindData)

            sqlQuery2 = "UPDATE employee_detail_lists SET name=%s, first_name=%s, last_name=%s, fullname=%s, company=%s WHERE id=%s"
            bindData2 = (_name, _first_name,_last_name, _fullname, _company, _id)
            cursor.execute(sqlQuery2, bindData2)
            
            conn.commit()



            response = jsonify('Employee updated sucessfully!')
            response.status_code = 200

            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/employee-delete/<int:id>', methods=['DELETE'])
def deleteEmployee(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM employee_detail_lists WHERE id=",(id, ))
        employeeName = cursor.fetchall()

        print(employeeName)

        # raise ValueError("Cannot divide by zero")
        
        # cursor.execute("DELETE FROM employee_detail_lists WHERE name =EMP", (id,))
        conn.commit()

        response = jsonify('Todo deleted successfully!')
        response.status_code = 200

        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status' : 404,
        'message' : 'Record not found: ' + request.url,
    }

    response = jsonify(message)
    response.status_code = 404

    return response

if __name__ == "__main__":
    app.run()