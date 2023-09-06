from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

class Department(db.Model):
    dno = db.Column(db.Integer, primary_key=True)
    dname = db.Column(db.String(255))

    def to_dict(self):
        return {
            'dno': self.dno,
            'dname': self.dname
        }
    
class Employee(db.Model):
    eno = db.Column(db.Integer, primary_key=True)
    ename = db.Column(db.String(255))
    dno = db.Column(db.Integer, db.ForeignKey('department.dno'), nullable=False)
    salary = db.Column(db.Integer)

    def to_dict(self):
        return {
            'eno': self.eno,
            'ename': self.ename,
            'dno': self.dno,
            'salary': self.salary
        }

db.create_all()

@app.route('/addEmployee', methods=['POST'])
def add_todo():
    data = request.json
    employee = Employee(ename=data['ename'], dno=data['dno'], salary=data['salary'])
    db.session.add(employee)
    db.session.commit()
    return {'eno': employee.eno}

@app.route('/addDepartment', methods=['POST'])
def add_department():  
    data = request.json
    department = Department(dname=data['dname'])
    db.session.add(department)
    db.session.commit()
    return {'dno': department.dno}

@app.route('/allDepartments')
def get_alldept():
    depts = Department.query.all()
    return {'Department': [dept.to_dict() for dept in depts]}

@app.route('/allEmployees')
def get_allemp():
    emps = Employee.query.all()
    return {'Employee': [emp.to_dict() for emp in emps]}

@app.route('/api')
def get_employee():
    eno = request.args.get('ENO')
    if eno is not None:
        employee = Employee.query.filter_by(eno=eno).first()
        if employee is not None:
            return jsonify(employee.to_dict())
        else:
            return jsonify({'message': 'Employee not found'})

    else:
        dname = request.args.get('DNAME')
        if dname is not None:
            employees = db.session.execute(f"SELECT * FROM employee WHERE dno = (SELECT dno FROM department WHERE dname = :dname)", {"dname": dname})
            return jsonify([dict(row) for row in employees])
        else:
            return jsonify({'message': 'Please specify ENO or DNAME'})

if __name__ == '__main__':
    app.run(port=9000)
