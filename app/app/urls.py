
#from xml.etree.ElementInclude import include
from drf_spectacular.views import (SpectacularAPIView,SpectacularSwaggerView,)
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

#from core.views import CustomPasswordResetView

urlpatterns = [
    #Enlace de admin
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    ),
    
    path('api/', include('api_forwardingcr.urls')),

]
