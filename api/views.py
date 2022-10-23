from rest_framework.decorators import api_view
from rest_framework.views import Response

from api.util import identify_plant


@api_view(['POST'])
def identify_plant_view(request):
    image = request.data.get('image', None)
    if not image:
        return Response('"image" is required in request payload', status=406)
    information = identify_plant(image, request.data.get('latitude'), request.data.get('longitude'))
    return Response(information)
