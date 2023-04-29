from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import user
from flask import Flask,flash, redirect, session
import re

#program will compare email address to this pattern
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class user:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.confirm_pwd = data['confirm_pwd']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

@classmethod
def get_all(cls):
	query = "SELECT * FROM users"
	users_from_db = connectToMySQL('recipe_share').query_db(query)
	users = []
	for user in users_from_db:
		users.append(cls(user))
	return users

@classmethod
def save(cls,data):
	query = "Insert INTO users (first_name,last_name,email,password,created_at,updated_at) \
VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());"
	user_id = connectToMySQL('recipe_share').query_db(query,data)
	return user_id

#Joins both user and recipe tables
@classmethod
def get_users_with_recipes( cls , data ):
    query = "SELECT * FROM users LEFT JOIN recipes ON recipes.user_id = users.id WHERE users.id = %(id)s;"
    recipe_results = connectToMySQL('recipe_share').query_db( query , data )
    recipe = cls( recipe_results[0] )
    for row in recipe_results:
        recipe_data = {
            "id" : row["recipe.id"],
            "name" : row["recipe.name"],
            "instructions" : row["recipe.instructions"],
            "under_30min" : row["recipe.under_30min"],
            "date_made" : row["recipe.date_made"],
            "created_at" : row["recipe.created_at"],
            "updated_at" : row["recipe.updated_at"]
        }
        user.recipes.append( recipe.Recipe( recipe_data ) )
    return recipe
#Searchs for first and last names of the user
@classmethod
def get_one_by_name(cls, firstName,lastName):
    data = {
        "first_name" : firstName,
        "last_name" : lastName
    }
    query = "SELECT * FROM userss \
            WHERE (first_name = %(firstName)s \
            AND last_name = %(lastName)s);"
    name_results = connectToMySQL('recipe_share').query_db(query,data)
    if not name_results:

        #return blank list if no such name is found
        return []
    return cls(name_results[0])

#Searches for a particular email address of a user
@classmethod
def get_one_email(cls, email):
    data = {
        "email" : email
    }
    query = "SELECT * FROM users \
            WHERE email = %(email)s;"
    email_results = connectToMySQL('recipe_share').query_db(query,data)
    if not email_results:

        #returns blank list if no such email is found
        return []
    return cls(email_results[0])  

#Searches for a particular password and returns empty list if none
@classmethod
def get_one_by_pwd(cls, pwd):
    data = {
            "pwd" : pwd
        }
    query = "SELECT * FROM users \
            WHERE password = %(pwd)s;"
    pwd_results = connectToMySQL('recipe_share').query_db(query,data)
    if not pwd_results:
        return []
    return cls(pwd_results[0])

#validates new registers
@staticmethod
def validate(user):
    is_valid = True

    #first two checks if first and last names are only letters
    #and are more than two letters long
    if (len(user['first_name']) < 2) \
        or (not user['first_name'].isalpha()):
        flash("First name must be more than two letters!")
        is_valid = False
    if (len(user['last_name']) < 2)\
        or(not user['last_name'].isalpha()):
        flash("Last name must be more than two letters!")
        is_valid = False

    #checks to see if email is in valid pattern
    if not EMAIL_REGEX.match(user['email']): 
        flash("Invalid email address!")
        is_valid = False

    #checks to see if password is longer than 8 letters
    if len(user['password']) < 8:
        flash("Password needs to be at least 8 characters.")
        is_valid=False
        
    #checks to see if same password is entered both times
    if not user['confirm_password'] != user['password']:
        flash("Password did not match.")
        is_valid=False

    #Checks if user is already in system
    elif user.get_one_by_name(
        user['first_name'],
        user['last_name']):
        flash("Name is already in the system")
        is_valid=False
    elif user.get_one__email(
        user['email']):
        flash("Email is already in the system.")
        is_valid=False
    elif user.get_one_by_pwd(
        user['password']):
        flash("Sorry, password is taken.  Try again.") 
        is_valid=False
    return is_valid
    
#Validates returning users login
def validate_login(user):
    is_valid = True

    #If the email is not in the system or entered correctly
    if (len(user['email']) < 1) or not \
        user.get_one_email(user['email']):
        flash("Invalid email address. Try again")
        is_valid=False
    elif not EMAIL_REGEX.match(user['email']):
        flash("Invalid email format.  Try again.")
        is_valid = False

    #If the password is not correct
    if (len(user['password']) < 1) or not \
        user.get_one_by_pwd(user['password']):
        flash("Invalid password.  Try again.")
        is_valid=False
    return is_valid

#Logging out clears the session and destorying login session
@app.route('/logout')
def logout():
    session.pop()
    session.clear()
    return redirect('/')

