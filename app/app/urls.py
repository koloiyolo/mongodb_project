from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout', views.user_logout, name='logout'),
    path('register', views.user_register, name='register'),
    path('edit', views.edit, name='edit'),
    path('user/edit/<int:pk>', views.user_edit, name='user_edit'),
    path('user/remove/<int:pk>', views.user_remove, name='user_remove'),
    path('users', views.user_list, name='user_list'),

    # films
    path('film/list', views.film_list, name='film_list'),
    path('film/add', views.film_add, name='film_add'),
    path('film/edit/<int:pk>', views.film_edit, name='film_edit'),
    path('film/remove/<int:pk>', views.film_remove, name='film_remove'),

    # rentals
    path('rental/list', views.rental_list, name='rental_list'),
    path('film/rent/<int:pk>', views.film_rent, name='film_rent'),
    path('film/rent/<int:film>/<int:user>', views.film_rent_as, name='film_rent_as'),
    path('film/return/<int:pk>', views.film_return, name='film_return'),
    path('rental/user/list<int:pk>', views.rental_list_user, name='rental_list_user'),
]