from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = "shop"
urlpatterns = [
    path("", views.index, name="index"),
    path("product/search", views.product_search, name="product_search"),
    path("product/detail/<int:product_id>", views.product_detail, name="product_detail"),
    path("cart", views.cart, name="cart"),
    path("cart/add/<int:product_id>", views.add_cart, name="add_cart"),
    path("cart/update/<int:product_id>", views.update_cart, name="update_cart"),
    path("cart/delete/<int:product_id>", views.delete_cart, name="delete_cart"),
    path("order", views.order, name="order"),
    path("order/complete", views.order_complete, name="order_complete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
