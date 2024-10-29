import json

def load_data():
    with open('./data/products.json', 'r') as file:
        data = json.load(file)
    return data
