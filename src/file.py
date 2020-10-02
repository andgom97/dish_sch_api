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
        dishes_file.write(json.dumps(new_dishes,indent=4))
        prGreen('Data saved')
    except Exception as e:
        prLightOrange(e)