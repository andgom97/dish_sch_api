import flask
from flask import request, jsonify
import json
from file import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True

dishes = read_dishes()

def get_dish(name):
    for dish in dishes:
        if dish['name']==name:
            return dish
    return None

def update_dish(old_dish,new_dish):
    keys = old_dish.keys()
    print(keys)
    for key in keys:
        old_dish[key]=new_dish[key]

@app.route('/api/v1', methods=['GET'])
def home():
    html ='''<h1>Dish scheduler API 1.0</h1>
            <p>Backend API for dish scheduler home application.</p>'''
    return html

# Page not found
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

# Bad request
@app.errorhandler(400)
def bad_request(e):
    return "<h1>400</h1><p>Your request is missing parameters.</p>", 400

# Resource already exist
@app.errorhandler(409)
def already_exist(e):
    return "<h1>409</h1><p>The resource already exists.</p>", 409

# Function to filter dishes by name or tag
@app.route('/api/v1/resources/dishes', methods=['GET'])
def filter_dish():
    query_parameters = request.args
    
    name = query_parameters.get('name')
    moment = query_parameters.get('moment')
    tag = query_parameters.get('tag')

    filter_result= dishes
    
    if name:
        filter_result = list(filter(lambda dish: dish['name'].startswith(name),filter_result))
    if moment:
        filter_result = list(filter(lambda dish: dish['moment'] == int(moment) or dish['moment'] == 2,filter_result))
    if tag:
        filter_result = list(filter(lambda dish: dish['tag'] == int(tag),filter_result))
    return jsonify({"dishes":filter_result})

# Function to filter dishes by name or tag
@app.route('/api/v1/resources/dishes/<name>', methods=['GET'])
def get_one_dish(name):
    dish = get_dish(name)
    if dish:
        return jsonify(dish)
    return page_not_found(404)

# Function to post a new dish
@app.route('/api/v1/resources/dishes', methods=['POST'])
def post_dish():
    try:
        dish = {
            'name':request.json['name'],
            'moment':request.json['moment'],
            'ingredients':request.json['ingredients'],
            'tag':request.json['tag']
        }
        if get_dish(dish['name'])==None:
            dishes.append(dish)
            write_dishes({'dishes':dishes})
            return jsonify(dish), 201
        return already_exist(409)
    except TypeError:
        return bad_request(400)
    except KeyError:
        return bad_request(400)

# Function to edit an existing dish
@app.route('/api/v1/resources/dishes/<name>', methods=['PUT'])
def put_dish(name):
    try:
        new_dish = {
            'name':request.json['name'],
            'moment':request.json['moment'],
            'ingredients':request.json['ingredients'],
            'tag':request.json['tag']
        }
        old_dish = get_dish(name)
        update_dish(old_dish,new_dish)
        write_dishes({"dishes":dishes})
        return jsonify(new_dish), 202
    except ValueError:
        return page_not_found(404)
    except AttributeError:
        return page_not_found(404)    
    except TypeError:
        return bad_request(400)
    except KeyError:
        return bad_request(400)

# Function to delete a dish
@app.route('/api/v1/resources/dishes/<name>', methods=['DELETE'])
def delete_dish(name):
    try:
        dish = get_dish(name)
        dishes.remove(dish)
        write_dishes({"dishes":dishes})
        return '<h1>202</h1><p>Accepted.</p>', 202
    except ValueError:
        return page_not_found(404)
