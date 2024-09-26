from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

#initialize Flask
app = Flask(__name__)

#Database configuration

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin123@localhost/student'
app.config['SQLALCHMEY_TRACK_MODIFICATIONS'] = False

#Initialize the database
db =  SQLAlchemy(app)

#Define student module
class student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    course = db.Column(db.String(100), nullable=False)

    def _repr_(self):
        return f"student('{self.name}', '{self.age}', '{self.course}')"

    


#Define routrs
@app.route('/')
def home():
    std =student.query.all()
    return render_template('index.html', students=std)

@app.route('/add',methods=['POST'])
def add():
         forName=request.form['name']
         forAge=request.form['age']
         forCourse=request.form['course']


         #create new Student record
         newStudent=student(name=forName,age=forAge,course=forCourse)
         db.session.add(newStudent)
         db.session.commit()
         return redirect(url_for('home'))

@app.route('/edit/<int:id>',methods=['POST','GET'])
def edit_student(id):
     std = student.query.get_or_404(id)  #get the student by id
     if request.method == 'POST':
          std.name = request.form['name']
          std.age = request.form['age']
          std.course = request.form['course']
          db.session.commit()
          return redirect(url_for('home'))


     return render_template('edit.html', student = std)

@app.route('/delete/<int:id>',methods=['POST'])
def delete_student(id):
     std = student.query.get_or_404(id)  #get the student by id
     db.session.delete(std)
     db.session.commit()
     return redirect(url_for('home'))

    

if __name__=='__main__':
   app.run(debug=True)
