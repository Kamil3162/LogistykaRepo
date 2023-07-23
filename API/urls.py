from django.urls import path
from Applications.UserManage import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('login/token', jwt_views.TokenObtainPairView.as_view(), name='token'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('validate-token/', jwt_views.TokenVerifyView.as_view(),
         name='validate-token'),
    # path('', views.LoginTokenView.as_view(), name='token_refresh'),
    path('home/token', views.HomeTokenView.as_view(), name='home_token'),
    path('detail-user/', views.SingleUserDetail.as_view(), name='details-user'),
    path('logout-token/', views.LogoutTokenView.as_view(), name='logout-token'),
    ####################
    path('all-users/', views.UserAllView.as_view(), name='all-users'),
    path('register/token', views.RegisterUserView.as_view(), name='register-users'),
    path('user/<int:pk>', views.PkUserDetailView.as_view(), name='user-detail'),

]