from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from users import views as users_views

urlpatterns = [
    path("", users_views.UserView().as_view()),
    path("login/", jwt_views.TokenObtainPairView.as_view()),
    path("<str:pk>/", users_views.UserDetailView.as_view()),
    path("<str:pk>/products/", users_views.SellerProductsView().as_view()),
    path("<str:pk>/purchase_history/", users_views.PurchaseHistoryView().as_view()),
]
