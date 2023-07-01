from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.title, name='title'),
    path('maingame/', views.main, name='main'),
]