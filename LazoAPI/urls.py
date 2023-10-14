from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products", views.get_products, name="products"),
    path("brand", views.get_brand, name="brand"),
    path("products/detail", views.get_product_detail, name="Product Detail"),
    path("reviews/general", views.get_reviews_general, name="Reviews General"),
    path("reviews", views.get_reviews, name="Reviews General")
]