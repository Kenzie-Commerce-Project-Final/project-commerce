from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("", views.ProductView.as_view()),
    path("<id>/", views.ProductDetailView.as_view()),
]
