from flask import Flask ,render_template ,flash  #flask-framework ,#Flask-python class

app = Flask(__name__)
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#in flask we attach every function to a route so we use the route.

@app.route('/home')
def home():
    #we need to create a html page in the templates folder.
    return render_template('home.html')


#static folder  stores images,stylesheets





@app.route('/services')
def services():
    #we need to create a html page in the templates folder.
    return render_template('services.html')

@app.route('/products')

def products():
    return render_template('products.html')



@app.route('/contact')

def contact():
   return render_template('contact.html')

@app.route('/about')

def about():
   return render_template('about.html')


@app.route('/')

def index3():
   return render_template('index3.html')

@app.route('/index2')

def index2():
   return render_template('index2.html')

#the application layer (business logic layer)

import pymysql    #import pymsql to install on the current project
from flask import request
@app.route('/blog', methods=['POST','GET'])
def blog():#logic goes her
    #handle form data
     if request.method=='POST': #check if user posted something
         email=request.form['email']
         name=request.form['name']
         message=request.form['message']

         #validation
         if email=="":
             return render_template('blog.html', msg1="email field is empty")
             #flash("email field is empty")

         if name=="":
             #flash("name field is empty")
             return render_template('blog.html', msg2="name field is empty")
         if message=="":
             #flash("name field is empty")

             return render_template('blog.html', msg3="message field is empty")
         if len(message)<10:
             #flash("message is too short")
             return render_template('blog.html', msg4="message is too short")
         else:
             #save the three ``fields to the database
             #establish db connection
             con=pymysql.connect("localhost","root", "","grace_db")

             #execute sql -create a cursor object to execute sql.
             cursor =con.cursor()
             sql= "INSERT INTO `messages_tbl`(`name`,`email`,`message`) VALUES (%s,%s,%s)"  # %s protects data .
             try:


                cursor.execute(sql,(name,email,message))
                con.commit() #commits the changes to the db
                return render_template('blog.html',msg="uploaded!")
             except:
               con.rollback()
     else:
         return render_template('blog.html')


import pymysql    #import pymsql to install on the current project
from flask import request
@app.route('/registration' , methods=['POST','GET'])
def registration():
    if request.method=='POST':
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        password=request.form['password']

        con1 = pymysql.connect("localhost", "root", "", "grace_db")
        cursor=con1.cursor()
        sql1="INSERT INTO `registration_tbl`(`firstname`,`lastname`,`email`,`password`) VALUES (%s,%s,%s,%s)"
        try:
            cursor.execute(sql1,(firstname,lastname,email,password))
            con1.commit()
            return render_template('index3.html', message="registration successful")
        except:
            con1.rollback()
    else:
        return render_template('registration.html' )

#pulling records of comments posted .
@app.route("/blogging")
def blogging():
    con=pymysql.connect("localhost", "root", "","grace_db")
    cursor=con.cursor()

    sql= "SELECT * FROM `messages_tbl` ORDER BY `message_time` DESC"
    #EXECUTE SQL
    cursor.execute(sql)

    #count the returned rows
    if cursor.rowcount < 1:
        return render_template('blogging.html', msg= " no messages found")
    else:
        rows =cursor.fetchall()
        #send the rows to the presentation layer,your html
        return render_template('blogging.html', rows= rows)


#searching from the database
@app.route('/search' , methods=['POST','GET'])
def search():
    if request.method=='POST':

        name=request.form['name']
        con = pymysql.connect("localhost", "root", "", "grace_db")
        cursor = con.cursor()

        sql= "SELECT * FROM `messages_tbl` WHERE `name`=%s ORDER BY  `message_time` DESC "
        cursor.execute(sql,(name))

        #check if cursor has zero rows
        if cursor.rowcount==0:
            return render_template('search.html',msg="no messages")
        else:
            rows=cursor.fetchall()
            return render_template('search.html',rows=rows)
    else:return render_template('search.html')

#the above function receives a name from the form and returns rows based on that name if they exist






if __name__ == '__main__':
    app.run()
