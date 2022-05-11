from django.contrib import admin
from django.urls import path, include
from . import career_apis, learning_object_apis, views

urlpatterns = [
    # Path for Career
    path('career/', career_apis.get_all_career),
    path('career/id', career_apis.get_career_by_id),
    path('career/language', learning_object_apis.get_language_by_career),

    # Path for Learning Object
    path('lo/language/', learning_object_apis.get_all_programing_language),



    path('lo/knowledge', learning_object_apis.get_all_knowledge),
    path('lo/tool', learning_object_apis.get_all_tool),
    path('lo/platform', learning_object_apis.get_all_platform),
    path('lo/framework', learning_object_apis.get_all_framework),

]
