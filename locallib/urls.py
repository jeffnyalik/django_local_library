from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    
    path('', include('catalog.urls')),
    path('catalog/', include('catalog.urls'), name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
