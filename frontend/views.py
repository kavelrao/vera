from django.shortcuts import render, redirect
from django.urls import reverse
from frontend.forms import IdentifyForm
from api.util import identify_plant

import base64


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
    if information['plant_details'].get('wiki_image') and information['plant_details']['wiki_image'].get('value'):
        image = information['plant_details']['wiki_image']['value']
        image_url = True
    else:
        image_url = False
    context = {
        'plant_name': information['plant_name'],
        'common_names': information['plant_details']['common_names'],
        'image': image,
        'image_url': image_url,
        'plant_description': information['plant_details']['wiki_description']['value'],
        'taxonomy': information['plant_details']['taxonomy'],
    }
    return render(request, 'display_info.html', context)
