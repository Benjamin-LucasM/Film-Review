from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movie_list, name='list'),
    path('movie/<int:pk>/', views.movie_detail, name='detail'),
    path('signup/', views.signup, name='signup'),
    path('add/', views.add_movie, name='add_movie'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),
]