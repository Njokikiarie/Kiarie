from flask import Flask ,render_template   #flask-framework ,#Flask-python class

app = Flask(__name__)

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

def index():
   return render_template('index.html')

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

        #save the three fields to the database
        #establish db connection
         con=pymysql.connect("localhost","root", "","grace_db")

         #execute sql -create a cursor object to execute sql.
         cursor =con.cursor()
         sql= "INSERT INTO `messages_tbl`(`name`,`email`,`message`) VALUES (%s,%s,%s)"  # %s protects data .
         cursor.execute(sql,(name,email,message))
         con.commit() #commits the changes to the db
         return render_template('blog.html')
     else:
         return render_template('blog.html')



if __name__ == '__main__':
    app.run()
