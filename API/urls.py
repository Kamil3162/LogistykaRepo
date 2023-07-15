from django.urls import path
from Applications.UserManage import views

urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('register', views.Register.as_view(), name='register'),
    path('user', views.UserDetail.as_view(), name='user'),
    path('allusers', views.AllUsers.as_view(), name='all_users')
]