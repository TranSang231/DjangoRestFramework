from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),         # URL /
    path('about/', views.about, name='about'),   # URL /about/
]