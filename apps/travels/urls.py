from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add$', views.add),
    url(r'^join$', views.join),
    url(r'^addtrip$', views.addtrip),
    url(r'^destination/(?P<id>\d+)$', views.destination)
]