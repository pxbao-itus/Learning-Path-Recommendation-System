import json
from django.http import JsonResponse

from services import user_service
from algorithm_implementation import build_learning_path_step4


def create_user(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user = {
        'username': body['username'],
        'password': body['password'],
        'name': body['name']
    }
    user_service.create_user(user)
    return JsonResponse(user)


def get_user_info(request):
    return JsonResponse(user_service.get_user_info(int(request.GET.get("id"))), safe=False)


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
    user_id = int(request.GET.get("id"))
    user_service.create_user_need_lo(user_id)
    lb = build_learning_path_step4.finding_set_of_LP(user_id)
    user_service.delete_user_need_lo(user_id)
    return JsonResponse(lb, safe=False)
