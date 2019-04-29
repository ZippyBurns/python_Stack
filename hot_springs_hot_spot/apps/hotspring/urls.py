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
    url(r'^view/(?P<my_val>\d+)$', views.view),
    url(r'^edit/(?P<my_val>\d+)$', views.edit),
    url(r'^delete/(?P<my_val>\d+)$', views.delete),
    url(r'^send_message$', views.send_message),
    url(r'^send_comment$', views.send_comment),
    url(r'^delete_message/(?P<my_val>\d+)$', views.delete_message),
    url(r'^delete_comment/(?P<my_val>\d+)$', views.delete_comment),
]