"""build_interface URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.urls import re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('build/', include('build.urls'), name='build'),
    re_path('release/', include('ocp_build_data.urls'), name="release"),
    #url('health/', include('build_health.urls'), name='build_health'),
    re_path('autocomplete/', include('autocomplete.urls'), name='autocomplete'),
    re_path('errata/', include('errata.urls'), name='errata'),
    re_path('incident/', include('incident_reports.urls'), name='incident'),
    re_path('api/v1/', include('api.urls')),
]
