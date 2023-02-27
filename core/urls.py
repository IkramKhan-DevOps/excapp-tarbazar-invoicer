"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the admin() function: from django.urls import admin, path
    2. Add a URL to urlpatterns:  path('blog/', admin('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve

from core.settings import ENVIRONMENT, MEDIA_ROOT, STATIC_ROOT


def home_view(request):
    return redirect("accounts:cross-auth")


def handler404(request, *args, **kwargs):
    return render(request, "404.html")


def handler500(request, *args, **kwargs):
    return render(request, "500.html")


# EXTERNAL APPS URLS
urlpatterns = [

    # DJANGO URLS > remove in extreme security
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),

    # API URLS
    path('accounts/', include('allauth.urls')),
]

# universal urls
urlpatterns += [
    path('under-construction/', TemplateView.as_view(template_name='under-construction.html')),
]

# your apps urls
urlpatterns += [
    path('accounts/', include('src.accounts.urls', namespace='accounts')),
    path('admins/', include('src.administration.admins.urls', namespace='admins')),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]