from django.urls import path
from Applications.UserManage import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('register', views.Register.as_view(), name='register'),
    path('user', views.UserDetail.as_view(), name='user'),
    path('allusers', views.AllUsers.as_view(), name='all_users'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login/token', views.LoginTokenView.as_view(), name='token_refresh'),
    path('home/token', views.HomeTokenView.as_view(), name='home_token'),
    path('detail-user/', views.UserDetailToken.as_view(), name='details-user'),
    path('validate-token/', views.ValidateToken.as_view(), name='validate-token'),
    path('logout-token/', views.LogoutTokenView.as_view(), name='validate-token')
]