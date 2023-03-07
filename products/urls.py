from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductView.as_view()),
    path("<id>/", views.ProductDetailView.as_view()),
    path("<name>/", views.ProductDetailView.as_view()),
    path("categories/<category_id>/", views.ProductDetailView.as_view()),
]
