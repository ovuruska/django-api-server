from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Quicker API",
      default_version='v1',
      description="Quicker Pet Grooming Scheduling API",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="ege.bagirsakci@makequicker.com"),
      license=openapi.License(name="Your License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('scheduling.urls')),
    path('api/auth/', include('authorization.urls')),
    path('api/', include('transactions.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('graphql/', include('graph.urls')),
    path('api/search/', include('search.urls')),
    path('api/capacity/', include('capacity.urls')),
    path('api/available/', include('available.urls')),
    path('api/customer/', include('customer.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
	path('payment/', include('payment.urls')),
]
