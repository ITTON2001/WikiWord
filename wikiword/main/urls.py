from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.tittle, name='tittle'),
    path('maingame/', views.main, name='main'),
]