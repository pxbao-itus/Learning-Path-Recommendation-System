from django.http import JsonResponse

from services import course_service


def get_lo_provided_by_course(request):
    return JsonResponse(status=200, data=course_service.get_lo_provided_by_course(int(request.GET.get('id'))),
                        safe=False)


def get_lo_required_by_course(request):
    return JsonResponse(status=200, data=course_service.get_lo_required_by_course(int(request.GET.get('id'))),
                        safe=False)


def get_info_course(request):
    return JsonResponse(status=200, data=course_service.get_info_course(int(request.GET.get('id'))), safe=False)
