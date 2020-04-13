from django.urls import path

from .views import login_view, home_view, menus_view, sign_up_view

urlpatterns = [
    path('', login_view, name='login'),
    path('', sign_up_view, name='sign_up'),
    path('home/', home_view, name='home'),
    path('menus/', menus_view, name='menus')
]