from django.urls import path

from . import views

urlpatterns = [
    #path('', views.HomeworkCreate.as_view()),
    path('hw/create', views.HomeworkCreate.as_view()),
    path('', views.HomeworkCreate.as_view()),

]


