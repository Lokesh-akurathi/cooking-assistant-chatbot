from django.contrib import admin
from django.urls import path, include
from mainapp import views as mainapp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('mainapp.urls')),
    path('', mainapp_views.index, name='index'),
]