from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *


app_name = 'store'
urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('detail/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
]
