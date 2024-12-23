from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from passlib.hash import sha256_crypt

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key_here'

# MongoDB connection setup
client = MongoClient("127.0.0.1:27017")  # Use your MongoDB URI
db = client['products']  # Database name
users_collection = db['user']  # Collection for user data
details_collection = db['product_details'] 
# Home route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/loginpage')
def loginpage():
    return render_template('login.html')

@app.route('/signuppage')
def signuppage():
    return render_template('signup.html')

@app.route('/addproductpage')
def addproductpage():
    return render_template('addproduct.html')

@app.route('/dashboardpage')
def dashboardpage():
    return render_template('dashboard.html')

# Register route (for simplicity)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        # Hash the password
        hashed_password = sha256_crypt.hash(password)

        # Store user in MongoDB
        users_collection.insert_one({'first_name':first_name ,'last_name':last_name ,'email': email, 'password': hashed_password})

        flash("Registration Successful!", "success")
        return redirect(url_for('loginpage'))

    return render_template('signup.html')  
@app.route('/login', methods=['GET','POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Check if user exists
    email= users_collection.find_one({'email': email})
    
    if email and sha256_crypt.verify(password, email['password']):
        flash("Login Successful!", "success")
        return redirect(url_for('dashboard'))
    else:
        flash("Invalid Username or Password!", "danger")
        return redirect(url_for('home'))
    
    
@app.route('/addproduct', methods=['POST'])
def addproduct():
    if request.method == 'POST':
        product_name=request.form['product_name']
        category=request.form['category']
        quantity = request.form['quantity']
        price = request.form['price']

        details_collection.insert_one({'product_name':product_name ,'category':category ,'quantity':quantity, 'price': price})

        
        return redirect(url_for('dashboard'))

    return render_template('register.html')
@app.route('/dashboard')
def dashboard():
    products = details_collection.find()
    products_list = list(products)

    return render_template('dashboard.html', products=products_list)

@app.route('/productdetails')
def productdetails():
    product_name=request.args.get("product_name")
    return product_name
if __name__== '__main__':
    app.run(debug=True)