"""
URL configuration for unidoc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="UniDoc API",
        default_version='v1',
        description="API для системы управления документами UniDoc",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@unidoc.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# API URLs
api_urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('core.urls')),
]

# Web URLs
web_urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('projects/', TemplateView.as_view(template_name='projects.html'), name='projects'),
    path('tasks/', TemplateView.as_view(template_name='tasks.html'), name='tasks'),
    path('documents/', TemplateView.as_view(template_name='documents.html'), name='documents'),
]

urlpatterns = [
    path('api/', include(api_urlpatterns)),
    path('web/', include(web_urlpatterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
