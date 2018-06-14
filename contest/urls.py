from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    #path('1/', views.register, name='register'),
]
