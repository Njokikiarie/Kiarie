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
#static folder  stores images,stylesheets
if __name__ == '__main__':
    app.run()
