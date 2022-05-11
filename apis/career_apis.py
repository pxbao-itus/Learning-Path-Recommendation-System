import json

from django.http import HttpResponse, JsonResponse, HttpRequest

# Create your views here.
from rest_framework.viewsets import ViewSet

from neo4j_connection.models import Career
from services import career_service


def get_all_career(request):
    return JsonResponse(career_service.get_all_career(), safe=False)

def get_career_by_id(request):
    id = int(request.GET.get("id"))
    return JsonResponse(career_service.get_career_by_id(id), safe=False)
