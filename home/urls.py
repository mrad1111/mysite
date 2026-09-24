from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path(
        "product/<int:product_id>/",
        views.product_detail,
        name="product_detail",
    ),

    path(
        "add-to-cart/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart",
    ),

    path(
        "order-now/<int:product_id>/",
        views.order_now,
        name="order_now",
    ),

    path(
        "cart/",
        views.cart,
        name="cart",
    ),

    path(
        "checkout/",
        views.checkout,
        name="checkout",
    ),

    path(
        "orders/",
        views.orders,
        name="orders",
    ),

    path(
        "profile/",
        views.profile,
        name="profile",
    ),

    path(
        "category/<int:category_id>/",
        views.category_products,
        name="category_products",
    ),

    path(
        "register/",
        views.register,
        name="register",
    ),

    path(
        "about/",
        views.about,
        name="about",
    ),
    path(
        "contact/",
        views.contact,
        name="contact",
    ),

  path(
    "logout/",
    views.user_logout,
    name="logout",
),
    path(
    "remove-from-cart/<int:product_id>/",
    views.remove_from_cart,
    name="remove_from_cart",
),
    path(
    "increase-quantity/<int:product_id>/",
    views.increase_quantity,
    name="increase_quantity",
),
    path(
    "decrease-quantity/<int:product_id>/",
    views.decrease_quantity,
    name="decrease_quantity",
),
    path(
    "wishlist/add/<int:product_id>/",
    views.add_to_wishlist,
    name="add_to_wishlist",
),
    path(
    "wishlist/",
    views.wishlist,
    name="wishlist",
),
]