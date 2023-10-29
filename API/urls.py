from django.urls import path,include
from Applications.UserManage import views as user_views
from Applications.TruckManage import views as truck_views
from Applications.SemitruckManage import views as semitrailer_views
from Applications.ReceivmentManage import views as receivment_views
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'trucks', truck_views.TruckViewSet, basename='trucks')
router.register(r'semitrailers', semitrailer_views.SemiTruckViewSet, basename='semitrailers')
router.register(r'receivments', receivment_views.ReceivmentModelViewSet, basename='receivments')

urlpatterns = [
    path('login/token', user_views.LoginTokenView.as_view(), name='token'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('validate-token/', jwt_views.TokenVerifyView.as_view(),
         name='validate-token'),
    # path('', views.LoginTokenView.as_view(), name='token_refresh'),
    path('home/token', user_views.HomeTokenView.as_view(),
         name='home_token'),
    path('detail-user/', user_views.SingleUserDetail.as_view(),
         name='details-user'),
    path('logout-token/', user_views.LogoutTokenView.as_view(),
         name='logout-token'),
    ####################
    path('all-users/', user_views.UserAllView.as_view(),
         name='all-users'),
    path('register/token', user_views.RegisterUserView.as_view(),
         name='register-users'),
    path('user/<int:pk>', user_views.PkUserDetailView.as_view(),
         name='user-detail'),
    path('user-permissions/', user_views.UserPermissionView.as_view(),
         name='user-permissions'),
    path('semitrailereqipment-create/',
         semitrailer_views.SemiTruckEquipmentCreate.as_view(),
         name='semitrailerequipment-create'),
    path('semitrailereqipment/<int:pk>/',
         semitrailer_views.SemiTruckEquipmentDetail.as_view(),
         name='semitrailerequipment-detail'),
    path('semitrailereqipments/',
         semitrailer_views.SemiTrailerEquipmentList.as_view(),
         name='semitrailerequipment-detail'),
    path('truck-equipment-create/',
         truck_views.TruckEquipmentCreateView.as_view(),
         name='truckequipment-create'),
    path('receivment-create/',
         receivment_views.ReceivmentCreateView.as_view(),
         name='receivments'),
    path('active-receivment/',
         receivment_views.ActiveUserReceivment.as_view(),
         name='active-receivment'
         ),
    # path('semitrailer-all/',
    #      semitrailer_views.SemiTrailerList.as_view(),
    #      name='semitrailer-list'),
    path('', include(router.urls)),
]