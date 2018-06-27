from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^registration$', views.registration),
    url(r'^admin$', views.admin),
    url(r'^admin_process$', views.admin_process),
    url(r'^exchange$', views.exchange),
    url(r'^upload$', views.upload),
    url(r'^upload_process$', views.upload_process),
    url(r'^sampler$', views.sampler),
    url(r'^sampler_process$', views.sampler_process),
    url(r'^cart$', views.cart),
    url(r'^payment$', views.payment),
    url(r'^review$', views.review),
    url(r'^edit$', views.edit),
    url(r'^edit_process$', views.edit_process),   # This line has changed! Notice that urlpatterns is a list, the comma is in
]      