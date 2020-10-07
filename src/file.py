import json
from prcolors import prLightOrange, prGreen

def read_dishes():
    try:
        dishes_file = open('../data/dishes.json','r')
        dishes = json.load(dishes_file)['dishes']
        return dishes
    except Exception as e:
        prLightOrange(e)
        return None

def write_dishes(new_dishes):
    try:
        dishes_file = open('../data/dishes.json','w')
        dishes_file.write(json.dumps({'dishes':new_dishes},indent=4))
        prGreen('Dishes saved')
    except Exception as e:
        prLightOrange(e)

def read_users():
    try:
        users_file = open('../data/users.json','r')
        users = json.load(users_file)['users']
        return users
    except Exception as e:
        prLightOrange(e)
        return None

def write_users(new_users):
    try:
        users_file = open('../data/users.json','w')
        users_file.write(json.dumps({'users':new_users},indent=4))
        prGreen('Users saved')
    except Exception as e:
        prLightOrange(e)