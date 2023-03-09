from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductView.as_view()),
    path("<id>/", views.ProductDetailView.as_view()),
    path("<deletePatch_id>/", views.ProductDetailUpdateDestroyView.as_view()),
]
