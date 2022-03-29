"""webssh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from LogTool_v3 import settings
from django_webssh import views
from django.conf.urls import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('upload_ssh_key/', views.upload_ssh_key),
    # path('django_webssh/', include('django_webssh.urls')),
    path('webssh/', views.webssh),
    path('is_login', views.is_login),
    path('dele', views.dele),
]
urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
