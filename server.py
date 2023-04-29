from flask_app import app
from flask import Flask, redirect,render_template,request,session
from flask_app.models import Recipe,User
#Returns the home page
@app.route('/')
def index():
    return render_template('index.html')

#Displays form for new recipe
@app.route('/recipes/new')
def add_recipe():
    return render_template('create_recipe.html')

#Displays specific recipe
@app.route('/recipes/<int:x>')
def show_recipe():
    return render_template('show_recipe.html', x = session['recipe_id'], \
                        recipe_info= Recipe.getOne(session['recipe_id']),
                        user_info = User.get_user_with_recipes())

@app.route('/recipes/edit/<int:x>', methods=['POST'])
def edit_recipe(id):
    if id not in session or (not Recipe.validate(request.form)):
        return redirect('/')
    return render_template('edit_recipe.html',x=session['id'], \
                        get_recipe=Recipe.get_one(session['id']))

if __name__ == "__main__":
    app.run(debug=True)
