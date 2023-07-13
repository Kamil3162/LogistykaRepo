from django.urls import path
from Applications.UserManage import views

urlpatterns = [
    path('login', views.Login),
    path('register', views.Register),
    path('logout', views.),
    path('user'),
]