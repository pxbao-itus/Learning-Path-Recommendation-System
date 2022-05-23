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

