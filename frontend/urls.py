from django.urls import path
from frontend import views


urlpatterns = [
    path('identify_plant/', views.identify_plant_frontend, name='identify_plant'),
    path('display_info/', views.display_info, name='display_info'),
    path('no_plant_found/', views.no_plant, name='no_plant'),
]
