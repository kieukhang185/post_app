from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://mongo:27017/mydatabase"
mongo = PyMongo(app)

# Home route
@app.route('/')
def index():
    if 'username' in session:
        items = mongo.db.items.find()
        return render_template('dashboard.html', items=items, username=session['username'])
    return redirect(url_for('login'))

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})

        if existing_user is None:
            hashpass = generate_password_hash(request.form['password'])
            users.insert_one({'username': request.form['username'], 'password': hashpass, 'role': 'user'})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        user = users.find_one({'username': request.form['username']})

        if user and check_password_hash(user['password'], request.form['password']):
            session['username'] = request.form['username']
            session['role'] = user['role']
            return redirect(url_for('index'))
        return 'Invalid username/password'

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Create Item
@app.route('/add', methods=['POST'])
def add_item():
    mongo.db.items.insert_one({'name': request.form['name'], 'description': request.form['description']})
    return redirect(url_for('index'))

# Update Item
@app.route('/edit/<item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = mongo.db.items.find_one({'_id': ObjectId(item_id)})
    if request.method == 'POST':
        mongo.db.items.update_one({'_id': ObjectId(item_id)}, {'$set': {'name': request.form['name'], 'description': request.form['description']}})
        return redirect(url_for('index'))
    return render_template('edit.html', item=item)

# Delete Item
@app.route('/delete/<item_id>')
def delete_item(item_id):
    mongo.db.items.delete_one({'_id': ObjectId(item_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  
