from django.urls import path 
from . import views

# define the urls
urlpatterns = [
    path('tasks/', views.tasks),
    path('tasks/<int:id>/', views.task_detail),
]