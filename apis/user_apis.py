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
        'name': "anonymous",
        'email': "anonymous",
        'cost': int(body['cost']) | 0,
        'time': int(body['time']) | 0
    }
    result = user_service.create_user(user, body['id'])
    if result.__len__() > 0:
        return JsonResponse(status=200, data=result[0])
    else:
        return JsonResponse(status=400, data={"message": "failed"})


def register(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    result = user_service.register(body['name'], body['email'])
    if result.__len__() > 0:
        return JsonResponse(status=200, data=result[0])
    else:
        return JsonResponse(status=400, data={"message": "failed"})


def update(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user_service.update(body['user'], body['career'])
    return JsonResponse(status=200, data={"msg": "success"})


def login(request):
    user_id = user_service.login(request.GET.get("email"))
    return JsonResponse(user_id, safe=False)


def get_user_info(request):
    result = user_service.get_user_info(int(request.GET.get("id")))
    if isinstance(result, User):
        return JsonResponse(result.get_user(), safe=False)
    else:
        return JsonResponse(status=400, data={"message": "failed"})


def create_objective_career(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    result = user_service.create_objective_career(body['user_id'], body['career_id'])
    if result > 0:
        return JsonResponse({"id": result})
    else:
        return JsonResponse(status=400, data={"message": "failed"})


def create_user_has_lo(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user_service.create_user_has_lo(body["user_id"], body["list_lo"])
    return JsonResponse(status=200, data={"message": "succeed"})


def get_lo_need_by_user(request):
    return JsonResponse(status=200, data=user_service.get_lo_need_by_user(int(request.GET.get('id'))), safe=False)


def get_learning_path(request):
    lb = user_service.get_learning_path_v2(int(request.GET.get("id")))
    return JsonResponse(lb, safe=False)


def get_lp_info(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    return JsonResponse(user_service.get_info_lp(body['courses'], body['user']), safe=False)