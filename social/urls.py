from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'social'

urlpatterns=[
    path('', views.profile, name='profile'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('user/edit', views.edit_user, name='edit_user'),

]