from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),         # URL /
    path('about/', views.about, name='about'),   # URL /about/
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('products/', views.products, name='products'),
    path('blog/', views.blog, name='blog'),
    path('faq/', views.faq, name='faq'),
]