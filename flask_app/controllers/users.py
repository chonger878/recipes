from flask_app import app
from flask_app.models.user import User
from flask import Flask, flash, redirect, request,session
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/user/create',methods=['POST'])
def create_user():
    if not User.validate(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    confirm_pw_hash = bcrypt.generate_password_hash(request.form['confirm_pwd'])
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash,
        "confirm_pwd" : confirm_pw_hash,
        "created_at" : request.form['created_at'],
        "updated_at" : request.form['updated_at']          
    }
	
    #Saves new user id 
    uId = User.save(data)
    session['uId'] = uId

    session['first_name'] = data['first_name']
    return redirect('/recipes')

#Login for returning user
app.route('/login', methods=['POST'])
def login():
    if User.validate_login(request.form):
        return redirect('/')
    data = {
        "email" : request.form['email']
    }
    #Checks if email is already in system
    check_email = User.get_one_email(data)
    if not check_email:
        flash('Invalid email not in the system')
        return redirect('/')
    if not bcrypt.check_password_hash(check_email.password, \
                                request.form['password']):
        flash('Invalid login.  Try again')
        return redirect('/')
    
    #saves and prints user registration as visit
    session['user_id'] = check_email.id
    #saves user's first name for greeting
    session['first_name'] = check_email.first_name
    return redirect('/recipes')