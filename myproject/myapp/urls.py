from . import views
from django.urls import path
from .views import *

# path('url', view_function, name="urlname")
# Dynamic Routing: We pass values through routing. For example, if we want to pass a username to a view function, we can do it like this:
# path('user/<str:username>/', user_profile, name="user_profile")
# Except values from route -> recieve in view function as parameters. For example, if we want to pass a username to a view function, we can do it like this:
# def user_profile(request, username):
urlpatterns = [
    path('', index, name="home"),
    path('shop/', shop, name="shop"),
    path('search/', search, name="search"),
    path('category/<slug:slug>/', category_view, name="category"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),
    path('cart/', cart, name="cart"),
    path('add_to_cart/<int:product_id>/', add_to_cart, name="add_to_cart"),
    path('toggle_wishlist/<int:product_id>/', toggle_wishlist, name='toggle_wishlist'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name="remove_from_cart"),
    path('clear_cart/', clear_cart, name="clear_cart"),
    path('checkout/', checkout, name="checkout"),
    path('payment_success/', payment_success, name="payment_success"),
    path('login/', login_view, name="login"),
    path('register/', register_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('account/', account_view, name="account"),
    path('orders/', orders_view, name="orders"),
    path('rate/<int:product_id>/', rate_product, name="rate_product"),
    path('reviews/<int:product_id>/', product_reviews, name="product_reviews"),
    path('api/ai-stylist/', views.ai_stylist_chat, name='ai_stylist_chat'),
    path('api/add-bundle/', views.add_bundle_to_cart, name='add_bundle_to_cart'),
]