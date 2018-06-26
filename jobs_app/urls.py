from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^submit', views.Stock_Page.submit),
    url(r'^$', views.index),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


