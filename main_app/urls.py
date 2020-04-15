from django.urls import path

from main_app.views.views import login_view, home_view, menus_view, sign_up_view
from main_app.views.dish_views import dish_view
from main_app.views.dining_hall_views import dining_hall_view

urlpatterns = [
    path('', login_view, name='login'),
    path('signup', sign_up_view, name='sign_up'),
    path('home/', home_view, name='home'),
    path('menus/', menus_view, name='menus'),
    path('dish/', dish_view, name='dish'),
    path('dining_hall/', dining_hall_view, name='dining_hall'),
]