import os
import requests
import json


PLANT_ID_URL = 'https://plant.id/api/v2'
PLANT_ID_KEY = os.getenv('PLANT_ID_KEY')


def identify_plant(image, latitude=None, longitude=None, live=False):
    if not live:
        with open('api/static/dummy_plant_info.json') as f:
            information = json.load(f)
        return information

    payload = {
        'images': [image],
        'plant_details': ['common_names', 'taxonomy', 'wiki_description', 'wiki_image']
    }
    if latitude:
        payload['latitude'] = latitude
    if longitude:
        payload['longitude'] = longitude
    
    headers = {'Content-Type': 'application/json', 'Api-Key': PLANT_ID_KEY}
    
    result = requests.post(f'{PLANT_ID_URL}/identify', headers=headers, json=payload)
    result = result.json()
    information = result['suggestions'][0]
    for suggestion in result['suggestions']:
        if suggestion['probability'] > information['probability']:
            information = suggestion

    with open('api/static/dummy_plant_info.json', 'w') as f:
        json.dump(information, f)

    return information