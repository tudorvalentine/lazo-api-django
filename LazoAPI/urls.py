from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products", views.get_products, name="products"),
    path("brand", views.get_brand, name="brand"),
    path("products/detail", views.get_product_detail, name="Product Detail"),
    path("reviews/general", views.get_reviews_general, name="Reviews General"),
    path("reviews", views.get_reviews, name="Reviews General"),
    path("reviews/add", views.add_review, name="Add Review"),
    path('password/forgot', views.forgot_password, name="Forgot Password"),
    path('password/forgot/code', views.forgot_password_verify_code, name="Forgot Password Code"),


    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout, name='token_logout'),
]