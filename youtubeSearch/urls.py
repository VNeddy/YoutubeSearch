from django.conf.urls import url
from django.urls import path
from django.views.generic.base import RedirectView
from . import search, views

urlpatterns = [
    url(r'^$', views.index, name='search'),
    url(r'^result$', search.search_post),
    url(r'^download/(?P<file_path>.*)/$', views.download, name='download'),
    path('favicon.ico', RedirectView.as_view(url='static/images/favicon.ico')),
]
