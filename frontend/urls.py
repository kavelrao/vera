from django.urls import path
from frontend import views


urlpatterns = [
    path('identify_plant/', views.identify_plant_frontend, name='identify_plant'),
    path('display_info/', views.display_info, name='display_info'),
]
