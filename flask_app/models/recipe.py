from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash

class recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30mins = data['under_30mins']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
@classmethod
def get_all(cls):
	query = "SELECT * FROM recipes"
	recipes_from_db = connectToMySQL('recipe_share').query_db(query)
	recipes = []
	for recipe in recipes_from_db:
		recipes.append(cls(recipe))
	return recipes

def get_one(cls,id):
	query = "SELECT * FROM recipes WHERE recipe_id = %(id)s;"
	getRecipe = connectToMySQL('recipe_share').query_db(query)
	oneRecipe = []
	for component in getRecipe:
		oneRecipe.append(cls(component))
	return oneRecipe

@classmethod
def save(cls,data):
	query = "Insert INTO recipes (name,description,instructions, under_30min, date_made, user_id,created_at,updated_at) \
VALUES(%(name)s,%(description)s,%(instructions)s,%(under_30min)s,%(date_made)s, %(user_id)s,NOW(),NOW());"
	recipe_id = connectToMySQL('recipe_share').query_db(query,data)
	return recipe_id

@classmethod
def validate_recipe(recipe):
    is_valid = True

    #Checks if the entries are valid
    if (len(recipe['name']) < 3) \
        or (not recipe['name'].isalpha()):
        flash("Recipe name cannot be less than 3 letters!")
        is_valid = False
    if (len(recipe['instructions']) < 3) \
        or (not recipe['instructions'].isalpha()):
        flash("Instructions cannot be less than 3 letters!")
        is_valid = False
    if (len(recipe['directions']) < 3) \
        or (not recipe['directions'].isalpha()):
        flash("Directions cannot be less than 3 letters!")
        is_valid = False
    return is_valid

@classmethod
def update(cls,data):
    query = """UPDATE recipes 
            SET name=%(name)s,
            description=%(description)s,instructions=%(instructions)s,
            under_30min = %(under_30min)s, date_made= %(date_made)s
            WHERE id = %(id)s;"""
    return connectToMySQL('recipe_share').query_db(query,data)



