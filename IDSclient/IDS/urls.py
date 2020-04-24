from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update_logs/', views.upd_logs, name='upd_logs'),
]