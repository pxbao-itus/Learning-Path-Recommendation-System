from django.contrib import admin
from django.urls import path, include
from . import career_apis, learning_object_apis, views, user_apis, course_apis

urlpatterns = [
    # Path for Career
    path('career/', career_apis.get_all_career),
    path('career/one', career_apis.get_career_by_id),
    # path('career/language', learning_object_apis.get_language_by_career),
    path('career/lo', career_apis.get_lo_need),

    # Path for Learning Object
    path('lo/language/', learning_object_apis.get_all_programing_language),
    path('lo/knowledge', learning_object_apis.get_all_knowledge),
    path('lo/tool', learning_object_apis.get_all_tool),
    path('lo/platform', learning_object_apis.get_all_platform),
    path('lo/framework', learning_object_apis.get_all_framework),

    # Path for Course
    path('course/need/lo', course_apis.get_lo_provided_by_course),
    path('course/require/lo', course_apis.get_lo_required_by_course),
    path('course', course_apis.get_info_course),

    # Path for user
    path('user/need', user_apis.get_lo_need_by_user),
    # url: http://localhost:8000/apis/user/create
    # method: POST
    # body_example: {
    #     "username": "Bob123",
    #     "password": "123123",
    #     "name": "Bob"
    # }
    # response: {
    #      "status": "success" | "fail"
    # }
    path('user/create', user_apis.create_user),

    # url: http://localhost:8000/apis/user/info?id=4684
    # method: GET
    # response: {
    #     "id": 4684,
    #     "username": "Bob123",
    #     "name": "Bob"
    # }
    path('user/info/', user_apis.get_user_info),

    # url: http://localhost:8000/apis/user/objective
    # method: POST
    # body_example: {
    #     "user_id": 4686,
    #     "career_id": 35
    # }
    # response: {
    #      "status": "success" | "fail"
    # }
    path('user/objective', user_apis.create_objective_career),

    # url: http://localhost:8000/apis/user/has
    # method: POST
    # body_example: {
    #     "user_id": 4684,
    #     "list_lo": [
    #         {
    #             "id": 22,
    #             "type": "tool",
    #             "level": 1
    #         },
    #         {
    #             "id": 16,
    #             "type": "knowledge",
    #             "level": 1
    #         },
    #         {
    #             "id": 27,
    #             "type": "platform",
    #             "level": 1
    #         },
    #         {
    #             "id": 91,
    #             "type": "framework",
    #             "level": 1
    #         }
    #     ]
    # }
    # response: {
    #      "status": "success" | "fail"
    # }
    path('user/has', user_apis.create_user_has_lo),

    # url: http://localhost:8000/apis/user/learning-path?id=4685
    # method: GET
    # response: [
    # [
    #     2081,
    #     867,
    #     3269,
    #     1905,
    #     4404,
    #     2153,
    #     4415,
    #     4417,
    #     3161
    # ]
    # ]
    path('user/learning-path', user_apis.get_learning_path)
]
