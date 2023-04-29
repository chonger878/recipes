from flask_app.models.recipe import Recipe
from flask_app import app
from flask_app.models.user import User
from flask import Flask, render_template,request,redirect,session

#Displays user's dashboard
@app.route('/recipes')
def dashboard():
    return render_template('dashboard.html', all_users = User.get_all(), list=User.get_users_with_recipes())

#Creating a new recipe
@app.route('/recipe/create',methods=['POST'])
def create_recipe():
    if not Recipe.validate(request.form):
        return redirect('/')
    data = {
        "name" : request.form['name'],
        "description" : request.form['description'],
        "instructions" : request.form['instructions'],
        "under_30min" : request.form['under_30min'],
        "date_made" : request.form['date_made'],
        "created_at" : request.form['created_at'],
        "updated_at" : request.form['updated_at']
    }
    id = Recipe.save(data)
    session['id'] = id
    return redirect('/recipes')
        