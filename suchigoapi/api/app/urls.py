"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import (
    RegisterView, CustomAuthToken, HomeView, ProfileView, 
    SettingsView, BillViewSet, PickupViewSet, AddressViewSet
)

router = DefaultRouter()
router.register(r'bills', BillViewSet, basename='bill')
router.register(r'pickups', PickupViewSet, basename='pickup')
router.register(r'addresses', AddressViewSet, basename='address')

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', CustomAuthToken.as_view(), name='login'),
    path('api/home/', HomeView.as_view(), name='home'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
    path('api/settings/', SettingsView.as_view(), name='settings'),
    path('api/', include(router.urls)),
]
