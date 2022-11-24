from cart.views import add_to_cart, cart, cart_check_out, hx_menu_cart, update_cart, hx_cart_total, success
from django.urls import path

urlpatterns = [
    path("add_to_cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("", cart, name="cart"),
    path("checkout/", cart_check_out, name="checkout"),
    path("hx_menu_cart/", hx_menu_cart, name="hx_menu_cart"),
    path("hx_cart_total/", hx_cart_total, name="hx_cart_total"),

    path("update_cart/<int:product_id>/<str:action>/",
         update_cart, name="update_cart"),
    path("success/", success, name="success")

]
