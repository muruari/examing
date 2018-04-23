from django.conf.urls import url
from . import views

urlpatterns = [
   
    url(r'^$', views.registration),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^add_friend/(?P<id>\d+)$', views.add_friend),
    url(r'^remove_friend/(?P<id>\d+)$', views.remove_friend),
    url(r'^user/(?P<id>\d+)$', views.user_page)
       
]