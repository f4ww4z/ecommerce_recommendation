from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import UserList

schema_view = get_schema_view(
    openapi.Info(
        title="Recommendation-based E-Commerce app",
        default_version='v1',
        description='A sample e-commerce web app backend',
        contact=openapi.Contact(email='faww4zintelgent4@gmail.com'),
        license=openapi.License(name='MIT License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger.json', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('docs', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('users', UserList.as_view(), name='users-list'),
]
