from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///test.db" #CONFIGURATION KEY UPDATE [use /// 3 slashes]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
app.app_context().push() #to solve app.app_context() problem 
#to create test.db write in terminal 
#python then write 
#from app (app is your py file name) import db then #this will create instance folder 
#db.create_all() to create test database
class test(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(200),nullable=False)
    desc=db.Column(db.Integer, nullable=False)

    date_Created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self)->str:
        return f"{self.sno}-{self.title}"

@app.route("/",methods=['GET','POST']) #to accept the request wether its get or post we have to mention USE CAPITAL GET AND POST
def hello_world():
    if request.method =='POST': #here we checking if request is post or not 
        # print("its POST method") 
        title=request.form['title'] #retriving form data and adding into variables
        desc=request.form['desc']
        # print("post")
        testx = test(title=title,desc=desc) #creating instance of database and passing the form title and description into testx variable instance
        db.session.add(testx) #performing add operation
        db.session.commit() #commiting the changes
    data = test.query.all() #to display the data into terminal page
    # print(data)
    return render_template('index.html',data=data) #redering index.html content data=data here we passing the data into data variable

@app.route("/show")
def production():
    data = test.query.all() #to display the data into terminal page
    print(data)
    return "this is product page"


@app.route("/update/<int:sno>",methods=['GET','POST']) #passing argument in route
def update(sno):
    if request.method=="POST":
        title=request.form['title'] #retriving form data and adding into variables
        desc=request.form['desc']
        data = test.query.filter_by(sno=sno).first()
        data.title = title
        data.desc = desc
        db.session.add(data) #performing add operation
        db.session.commit()
        return redirect("/")
    data = test.query.filter_by(sno=sno).first() #to display the data into terminal page
    return render_template('update.html',data=data)
    


    
@app.route("/delete/<int:sno>")
def delete(sno):
    data = test.query.filter_by(sno=sno).first() #test is our database name query . filter_by use to apply filter on sno which is in database first() method use to apply only single values
    # print(data)
    db.session.delete(data) #here deleting the data
    db.session.commit() #commiting the changes
    return redirect("/") #redirect to defult page

if __name__ == "__main__":
    app.run(debug=True)