import json

from django.http import JsonResponse

# Create your views here.

from services import learning_object_service


# API for Learning Object for user
def get_all_programing_language(request):
    return JsonResponse(learning_object_service.get_all_programing_language(), safe=False)


def get_all_knowledge(request):
    return JsonResponse(learning_object_service.get_all_knowledge(), safe=False)


def get_all_tool(request):
    return JsonResponse(learning_object_service.get_all_tool(), safe=False)


def get_all_platform(request):
    return JsonResponse(learning_object_service.get_all_platform(), safe=False)


def get_all_framework(request):
    return JsonResponse(learning_object_service.get_all_framework(), safe=False)


def get_all_lo(request):
    return JsonResponse(learning_object_service.get_all_lo(), safe=False)


def get_search_lo(request):
    return JsonResponse(learning_object_service.get_lo_search(request.GET.get('value')), safe=False)


def get_lo_has(request):
    return JsonResponse(learning_object_service.get_lo_has(request.GET.get('id')), safe=False)


def delete_lo_has(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    learning_object_service.delete_lo_has(body['user'], body['lo'])
    return JsonResponse(data={"msg": "success"}, safe=False)


def create_lo_has(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    learning_object_service.delete_lo_has(body['user'], body['lo'])
    result = learning_object_service.create_lo_has(body['user'], body['lo'], body['level'])
    return JsonResponse(result, safe=False)