from flask import Flask ,render_template ,flash, session  #flask-framework ,#Flask-python class

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/?' #creating a encryption. this is called a salt,

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
#login route

@app.route('/login' , methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        con = pymysql.connect("localhost", "root", "", "grace_db")
        cursor = con.cursor()
        sql = "SELECT * FROM `registration_tbl` where `email`=%s and `password`=%s"

        #execute sql using the cursor object
        cursor.execute(sql,(email,password))
        #check if a match was found or not
        if cursor.rowcount==0:
            return render_template("login.html" , msg1="No match .Wrong input")
        elif cursor.rowcount==1:
            # create a session for the user
            #we store username in session variable, you dont store password in session
            row = cursor.fetchone()

            session['userkey'] = row[1]




            return redirect('/blogging')
        elif cursor.rowcount >1:
            return render_template('login.html', msg1="try again later")
        else:
            return render_template('login.html', msg1="contact admin")

    else:
        #shows login page, after the route is visited
        return render_template('login.html')

#logout

@app.route('/logout')
def logout():
    session.pop('userkey',None)
    return redirect('login')



#pulling records of comments posted .
@app.route("/blogging")
def blogging():
    if 'userkey' in session:
        #get the key value and show
        email = session['userkey']

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
    elif 'userkey' not in session:
        return redirect('/login')
    else:redirect('/login')




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


con = pymysql.connect("localhost", "root", "", "grace_db")
cursor = con.cursor()
@app.route('/customers' , methods=['POST','GET'])
def customers():
    if request.method=='POST':

        State=request.form['State']
        Coverage= request.form['Coverage']


        sql= "SELECT * FROM `customers` WHERE `State`=%s  AND `Coverage` =%s ORDER BY  `EffectiveDate` DESC "
        cursor.execute(sql,(State ,Coverage))

        #check if cursor has zero rows
        if cursor.rowcount==0:
            return render_template('customers.html',msg="no messages")
        else:
            rows=cursor.fetchall()
            return render_template('customers.html',rows=rows)
    else:
        sql= "SELECT * FROM `customers`ORDER BY  `EffectiveDate` DESC "

        cursor.execute(sql)
        rows=cursor.fetchall()
        return render_template('customers.html' , rows=rows)

#deleting a blog:this route receives a message id to specify the blog to be deleted
from flask import redirect
@app.route('/deleteblog/<msg_id>' )
def deleteblog(msg_id):
    #we now delete the massage with that ID
    con = pymysql.connect("localhost", "root", "", "grace_db")
    cursor = con.cursor()
    sql="Delete from messages_tbl where message_id=%s "
    #execute sql, provide msg_id that we received.


    try:
        cursor.execute(sql, (msg_id))
        con.commit()
        return redirect('/blogging')# reloads the page
    except:
        con.rollback()
        return redirect('/blogging')
@app.route('/deleteCustomer/<nameid>' )
def deleteCustomer(nameid):
    #we now delete the massage with that ID
    con = pymysql.connect("localhost", "root", "", "grace_db")
    cursor = con.cursor()
    sql="Delete from customers where `name`= %s "
    #execute sql, provide msg_id that we received.


    try:
        cursor.execute(sql,(nameid))
        con.commit()
        sql = "SELECT * FROM `customers`ORDER BY  `EffectiveDate` DESC "

        cursor.execute(sql)
        rows = cursor.fetchall()

        return render_template('customers.html', msg2= nameid+" ,deleted" , rows=rows)

    except:
        con.rollback()
        return redirect('/customers')




#data science
import pandas
import matplotlib.pyplot as plt
@app.route('/analysis')
def analysis():
    #libraries used for data analysis:
    #1.pandas -basic anaylsis, data structuring
    #2.visualization: for plotting graphs like matplotlib,seaborn,plotly
    con=pymysql.connect("localhost" ,"root", "","grace_db")
    dataframe = pandas.read_sql("select MonthlyPremium ,LastClaim, TotalClaim from customers", con)
    #print(dataframe['Coverage'])
    #print(dataframe.describe())

    years =[2010,2012,2014,2016,2018,2020]
    budget=[20000,15000,52222,78000,56712,89000]

    #plotting
    plt.bar(years,budget)
    plt.xlabel="years"
    plt.ylabel="expense in KES"
    plt.title="school budget distribution / yearly"

    plt.savefig("static/bar.png")
    #plt.show() -displays the graph on the console

    plt.scatter(years, budget)
    plt.xlabel = "years"
    plt.ylabel = "expense in KES"
    plt.title = "school budget distribution / yearly"

    plt.savefig("static/scatter1.png")


    return render_template('analysis.html')

@app.route('/sales')
def sales():
    con=pymysql.connect("localhost","root","","grace_db")
    #dataframe=pandas.read_sql("select * from sales2",con)
    #print(dataframe.head()) #.head() prints the first 5, .tail()-prints the last 5
    #print(dataframe.describe()) #describes the integers in the table eg:price,quantity. it shows basic statistics

    #narrowing  down data
    sales = pandas.read_sql("select * from sales2", con)
    customers = sales[['name','ext price','date']]
    #print(customers.head())

    customer_group= customers.groupby('name') #group customers by name .
    print(customer_group.size()) #gives us the number of times the customers appear on the table

    sales_totals= customer_group.sum() #sums up  'ext price' per group
    print(sales_totals)

    #plot
    sales_totals.plot(kind='bar')
    #plt.show()
    plt.savefig("static/sales.png")
@app.route('/sales2')
def sales2():
    con=pymysql.connect("localhost","root","","grace_db")

    sales = pandas.read_sql("select * from sales2", con)
    customers = sales[['name','category','ext price','date']]

    customer_group= customers.groupby(['name','category']).sum() #group customers by name .


    customer_group.unstack().plot(kind="bar", stacked=True,title="total sales by customers")
    plt.show()



if __name__ == '__main__':
    app.run()
