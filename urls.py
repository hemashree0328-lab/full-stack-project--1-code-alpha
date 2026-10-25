
from django.urls import path
from . import views
from . import views

urlpatterns = [
    # Homepage and products
    path("", views.product_list, name="product_list"),
    path("products/", views.product_list, name="product_list"),
    path(
        "products/<int:product_id>/",
        views.product_detail,
        name="product_detail",
    ),

    # Shopping cart
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path(
        "cart/increase/<int:product_id>/",
        views.increase_quantity,
        name="increase_quantity",
    ),
    path(
        "cart/decrease/<int:product_id>/",
        views.decrease_quantity,
        name="decrease_quantity",
    ),
    path(
        "cart/remove/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),

    # Account
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Checkout and orders
    path("checkout/", views.checkout, name="checkout"),
    path(
        "order-success/<int:order_id>/",
        views.order_success,
        name="order_success",
    ),
    path("my-orders/", views.my_orders, name="my_orders"),
    path(
        "orders/<int:order_id>/track/",
        views.track_order,
        name="track_order",
    ),
    path(
        "orders/<int:order_id>/cancel/",
        views.cancel_order,
        name="cancel_order",
    ),

    # Product reviews
    path(
        "products/<int:product_id>/review/",
        views.add_review,
        name="add_review",
    ),
    path("my-admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
