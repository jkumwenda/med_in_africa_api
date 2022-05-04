from django import urls
from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="DRF BASE API",
      default_version='v1',
      description="DRF Base API documentation",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router  = DefaultRouter()

router.register('users', views.UserViewSet, basename = 'Users')
router.register('register', views.UserRegistrationViewSet, basename = 'User Register')
router.register('reset_password', views.PasswordResetViewSet, basename = 'Password ')
router.register('groups', views.GroupViewSet, basename = 'Groups')
router.register('permissions', views.PermissionViewSet, basename = 'Permissions')
router.register('user_logs', views.UserLogsViewSet, basename = 'User Logs')

urlpatterns = [
    path('', include(router.urls)),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]