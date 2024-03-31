from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from field_scan_app.views import *

urlpatterns = [
    path('', index, name='main index'),
    path('dashboard', dashboard, name='dashboard'),
    path('signals', signals, name='signals'),
    path('upload-image', upload_image, name='upload image'),
]
    
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
