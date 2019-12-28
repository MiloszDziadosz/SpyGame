from django.conf.urls import url
#from django.urls import path, include
from . import views


app_name = 'mainpage'

urlpatterns = [
    # /mainpage/
    url(r'^$', views.index, name='index'),

    # /mainpage/1/
    url(r'^(?P<temp_id>[0-9]+)/$', views.templist, name='templist'),
    #path('')

    # /mainpage/create_game/
    url(r'^(create_game)/$', views.create_game, name='create_game'),
    #path('create_game/', views.new_game),
    # /mainpage/create_game/
    url(r'^(join_game)/$', views.join_game, name='join_game'),

    url(r'^fast_join/(?P<liczba>[0-9]+)$', views.fast_join, name='fast_join'),

    url(r'^game/$', views.game, name='game'),

    url(r'^vote_wait/$', views.vote_wait, name='vote_wait'),

    url(r'^vote/$', views.vote, name='vote'),

    url(r'^count_votes/$', views.count_votes, name='count_votes'),

    url(r'^losowanie/$', views.roles, name='losowanie'),
]




















