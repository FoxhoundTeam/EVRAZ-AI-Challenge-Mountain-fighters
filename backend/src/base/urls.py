from django.conf.urls import url, include
from rest_auth.views import LoginView, UserDetailsView, LogoutView
from rest_framework import routers
from src.base.views import (
    EmployeeViewSet,
    CameraViewSet,
    ViolationViewSet,
    FrameViewSet
)

rest_auth_urls = [
    url(r'^login/$', LoginView.as_view(), name='rest_login'),
    url(r'^logout/$', LogoutView.as_view(), name='rest_logout'),
    url(r'^user/$', UserDetailsView.as_view(), name='user'),
]

router = routers.DefaultRouter()
router.register(r'employee', EmployeeViewSet, basename='Employee')
router.register(r'camera', CameraViewSet, basename='Camera')
router.register(r'violation', ViolationViewSet, basename='Violation')
router.register(r'frame', FrameViewSet, basename='Frame')


urlpatterns = [
    url(r'^auth/', include((rest_auth_urls, 'auth'), namespace='auth')),
    url(r'^', include(router.urls)),
]
