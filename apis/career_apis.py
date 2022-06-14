from django.http import JsonResponse

# Create your views here.

from services import career_service


def get_all_career(request):
    return JsonResponse(career_service.get_all_career(), safe=False)


def get_career_by_id(request):
    id = int(request.GET.get("id"))
    return JsonResponse(career_service.get_career_by_id(id), safe=False)


def get_lo_need(request):
    return JsonResponse(status=200, data=career_service.get_lo_career_need(int(request.GET.get("id"))), safe=False)
