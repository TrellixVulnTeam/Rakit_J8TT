"""jobs_site URL Configuration

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
from django.conf.urls import url, handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', include('Our_Vision.urls')),
    url(r'Contact/', include('contact.urls')),
    url(r'Stocks/', include('jobs_app.urls')),
    url(r'Terms_of_Use/', include('Terms_of_Use.urls')),
    url(r'Home/', include('Our_Vision.urls'))
]

handler404 = 'jobs_app.views.error_404'
handler500 = 'jobs_app.views.error_404'
