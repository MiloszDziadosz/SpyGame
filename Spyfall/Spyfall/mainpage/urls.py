from django.conf.urls import url
from . import views

urlpatterns = [
    # /mainpage/
    url(r'^$', views.index, name='index'),

    # /mainpage/
    url(r'^(?P<temp_id>[0-9]+)/$', views.templist, name='templist'),
]