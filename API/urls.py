from django.urls import path,include
from Applications.UserManage import views
from Applications.TruckManage import views as truck_views
from Applications.SemitruckManage import views as semitrailer_views
from Applications.ReceivmentManage import views as receivment_views
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'trucks', truck_views.TruckViewSet, basename='trucks')
router.register(r'semitrailers', semitrailer_views.SemiTruckViewSet, basename='semitrailers')
router.register('receivments', receivment_views.ReceivmentViewSet, basename='receivments')

urlpatterns = [
    path('login/token', jwt_views.TokenObtainPairView.as_view(), name='token'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('validate-token/', jwt_views.TokenVerifyView.as_view(),
         name='validate-token'),
    # path('', views.LoginTokenView.as_view(), name='token_refresh'),
    path('home/token', views.HomeTokenView.as_view(),
         name='home_token'),
    path('detail-user/', views.SingleUserDetail.as_view(),
         name='details-user'),
    path('logout-token/', views.LogoutTokenView.as_view(),
         name='logout-token'),
    ####################
    path('all-users/', views.UserAllView.as_view(),
         name='all-users'),
    path('register/token', views.RegisterUserView.as_view(),
         name='register-users'),
    path('user/<int:pk>', views.PkUserDetailView.as_view(),
         name='user-detail'),
    path('user-permissions/', views.UserPermissionView.as_view(),
         name='user-permissions'),
    path('semitrailereqipment-create/',
         semitrailer_views.SemiTruckEquipmentCreate.as_view(),
         name='semitrailerequipment-create'),
    path('semitrailereqipment/<int:pk>/',
         semitrailer_views.SemiTruckEquipmentDetail.as_view(),
         name='semitrailerequipment-detail'),
    # path('semitrailer-all/',
    #      semitrailer_views.SemiTrailerList.as_view(),
    #      name='semitrailer-list'),
    path('', include(router.urls)),
]