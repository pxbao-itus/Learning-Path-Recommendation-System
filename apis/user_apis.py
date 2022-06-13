import json
from django.http import JsonResponse

import algorithm_implementation
from services import user_service
from algorithm_implementation import build_learning_path_step4, evaluate_set_courses_step3
from models.user import User


def create_user(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user = {
        'name': body['name'],
        'email': body['email'],
        'cost': body['cost'],
        'time': body['time']
    }
    result = user_service.create_user(user)
    if result.__len__() > 0:
        return JsonResponse(result[0])
    else:
        return JsonResponse.status_code(400)


def get_user_info(request):
    result = user_service.get_user_info(int(request.GET.get("id")))
    if isinstance(result, User):
        return JsonResponse(result.get_user(), safe=False)
    else:
        return JsonResponse.status_code(400)


def create_objective_career(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    result = user_service.create_objective_career(body['user_id'], body['career_id'])
    if result > 0:
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "fail"})


def create_user_has_lo(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user_service.create_user_has_lo(body["user_id"], body["list_lo"])
    return JsonResponse({"status": "success"})


def get_learning_path(request):
    lb = user_service.get_learning_path(int(request.GET.get("id")))
    return JsonResponse(lb, safe=False)
