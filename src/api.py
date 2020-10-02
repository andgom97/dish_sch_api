import flask
from flask import request, jsonify
import json
from file import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True

dishes = read_dishes()

def dish_exist(name):
    for dish in dishes:
        if name==dish['name']:
            return True
    return False

@app.route('/api/v1', methods=['GET'])
def home():
    html ='''<h1>Dish scheduler API 1.0</h1>
            <p>Backend API for dish scheduler home application.</p>'''
    return html

# Page not found
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

# Error function
@app.errorhandler(400)
def bad_request(e):
    return "<h1>400</h1><p>Your request is missing parameters.</p>", 400

# Function to filter dishes by name or tag
@app.route('/api/v1/resources/dishes', methods=['GET'])
def dish_filter():
    query_parameters = request.args
    
    name = query_parameters.get('name')
    moment = query_parameters.get('moment')

    filter_result=[]
    
    if not (name or moment):
        return jsonify({"dishes":dishes})
    
    if name:
        for dish in dishes:
            if name in dish['name']:
                filter_result.append(dish)
        
    if moment:
        for dish in dishes:
            if int(moment)==dish['moment'] or dish['moment']==2:
                filter_result.append(dish)

    return jsonify({"dishes":filter_result})

# Function to post a new dish
@app.route('/api/v1/resources/dishes', methods=['POST'])
def add_dish():
    if not request.json:
        return bad_request(400)
    if not 'name' in request.json:
        return bad_request(400)
    if not 'ingredients' in request.json:
        return bad_request(400)
    if not 'moment' in request.json:
        return bad_request(400)
    if not 'tag' in request.json:
        return bad_request(400)
    if not dish_exist(request.json['name']):
        dish = {
            'name':request.json['name'],
            'moment':request.json['moment'],
            'ingredients':request.json['ingredients'],
            'tag':request.json['tag']
        }
        dishes.append(dish)
        write_dishes({'dishes':dishes})
        return jsonify(dish), 201
    return "<h1>409</h1><p>The resource already exists.</p>", 409

# Function to edit an existing dish
@app.route('/api/v1/resources/dishes', methods=['PUT'])
def update_dish():
    pass

# Function to delete a dish
@app.route('/api/v1/resources/dishes', methods=['DELETE'])
def delete_dish():
    query_parameters = request.args

    name = query_parameters.get('name')

    if name:
        for dish in dishes:
            if name==dish['name']:
                dishes.remove(dish)
                write_dishes({"dishes":dishes})
                return "<h1>202</h1><p>Accepted.</p>", 202
        return page_not_found(404)
        
    if not name:
        return bad_request(400)