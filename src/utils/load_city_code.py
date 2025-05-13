import json

def load_city_code():
    with open('config/city_code.json', 'r', encoding='utf-8') as f:
        return json.load(f)
