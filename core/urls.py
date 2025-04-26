from django.contrib import admin
from django.urls import path, include, re_path

# Static settings
from django.conf import settings
from django.conf.urls.static import static

# Swagger UI
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Apply API",
      default_version='v1',
      description="Apply API",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# Admin custom
admin.site.site_title = "Admin"
admin.site.site_header = "Qabul Admin"
admin.site.index_title = "Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),

    # Djoser
    # re_path(r'^auth/', include('djoser.urls')),
   #  re_path(r'^auth/', include('djoser.urls.jwt')),
   # Accounts APP
   path('api/v1/auth/', include('accounts.urls')),
   path('api/v1/application/', include('applications.urls')),

    # Swagger UI
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
