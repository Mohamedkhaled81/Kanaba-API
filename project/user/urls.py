from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter




urlpatterns = [
    path('customer/register', views.CustomerRegister.as_view({'post': 'create'}),
        name='customer-register'),
    path('customer/login', views.CustomerLogin.as_view({'post': 'create'}),
        name='customer-login'),
    path('customer/logout', views.CustomerLogout.as_view(),
        name='customer-logout')
]