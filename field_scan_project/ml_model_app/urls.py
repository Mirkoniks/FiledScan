from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from ml_model_app.views import *

urlpatterns = [
    path('image-model', image_model, name='image model'),
]
