from django.urls import path
from .views import (
    IndexView, AboutView, ContactView, 
    ServicesView, ProductsView, BlogView, FAQView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('services/', ServicesView.as_view(), name='services'),
    path('products/', ProductsView.as_view(), name='products'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('faq/', FAQView.as_view(), name='faq'),
]
