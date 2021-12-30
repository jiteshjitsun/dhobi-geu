from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/',views.signin,name='signin'),
    path('signup/',views.signup, name='signup'),
    path('contact/',views.contactForm, name='contact'),
    path('userprofile/',views.userprofile, name='profile'),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name='checkout'),
    path('update_item/', views.updateItem, name="update_item"),
]