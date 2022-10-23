from django.urls import path
from api import views


urlpatterns = [
    path('identify_plant/', views.identify_plant_view, name='identify_plant')
]
