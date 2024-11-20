from django.urls import path
from .views import home, colleague_tasks

urlpatterns = [
    path('', home, name='home'),
    path('tasks/<str:colleague_name>/', colleague_tasks, name='colleague_tasks'),
]