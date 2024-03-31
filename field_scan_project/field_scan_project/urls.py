from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('model/', include('ml_model_app.urls')),
    path('auth/', include('authentication.urls')),
    path('', include('field_scan_app.urls')),
    path('admin/', admin.site.urls),
]
