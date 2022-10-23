from django.shortcuts import render, redirect
from django.urls import reverse
from frontend.forms import IdentifyForm
from api.util import identify_plant

import requests
import base64
import os


GEO_URL = 'https://api.ipgeolocation.io/ipgeo'
GEO_KEY = os.getenv('GEO_KEY')
MAPBOX_TOKEN = os.getenv('MAPBOX_TOKEN')

def identify_plant_frontend(request):
    if request.method == 'POST':
        form = IdentifyForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            img = base64.b64encode(data['image'].read()).decode('utf-8')
            request.session['image'] = img
            return redirect(reverse('display_info'))

    else:
        form = IdentifyForm()

    return render(request, 'identify_plant.html', {'form': form})


def display_info(request):
    image = request.session['image']
    information = identify_plant(image, live=False)
    if not information['is_plant']:
        return redirect(reverse('no_plant'))

    if information['plant_details'].get('wiki_image') and information['plant_details']['wiki_image'].get('value'):
        image = information['plant_details']['wiki_image']['value']
        image_url = True
    else:
        image_url = False

    if os.getenv('LONGITUDE') and os.getenv('LATITUDE'):
        geo_response = {
            'longitude': float(os.getenv('LONGITUDE')),
            'latitude': float(os.getenv('LATITUDE'))
        }
    else:
        geo_response = requests.get(GEO_URL, params={'apiKey': GEO_KEY}).json()

    context = {
        'plant_name': information['plant_name'],
        'common_names': information['plant_details']['common_names'],
        'image': image,
        'image_url': image_url,
        'plant_description': information['plant_details']['wiki_description']['value'],
        'taxonomy': information['plant_details']['taxonomy'],
        'longitude': geo_response['longitude'],
        'latitude': geo_response['latitude'],
        'mapbox_token': MAPBOX_TOKEN
    }
    return render(request, 'display_info.html', context)

def no_plant(request):
    return render(request, 'no_plant.html', {'retry_url': reverse('identify_plant')})
