from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products", views.products, name="products"),
    path("brand", views.brand, name="brand"),
    path("products/detail", views.product_detail, name="Product Detail")
]