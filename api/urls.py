from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('register/', views.apiRegistration, name='api-registration'),
    path('api-token-auth/', obtain_auth_token),
    path('task-list/', views.taskList, name='task-list'),
    path('task-detail/<str:pk>/', views.detailList, name='task-detail'),
    path('task-create/', views.createList, name='task-create'),
    path('task-update/<str:pk>/', views.updateList, name='task-update'),
    path('task-delete/<str:pk>/', views.deleteList, name='task-delete')
]