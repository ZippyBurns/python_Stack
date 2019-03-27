from django.conf.urls import url
from . import views 

urlpatterns=[
    url(r'^$', views.index),
    url(r'^home$', views.homepage),
    url(r'^login$', views.login),
    url(r'logout$', views.logout),
    url(r'^username$', views.username),
    url(r'^home$', views.home),
    url(r'^find$', views.find),
    url(r'^community$', views.community),
    url(r'^news$', views.news),
    url(r'^about_me$', views.about_me),
]