from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('multi/<int:game_id>', views.multiplayer, name='chess-multi'),
    path('creategame/', views.create.as_view(), name='create'),
    path('ongoing/', views.ongoing, name="ongoing"),
]
