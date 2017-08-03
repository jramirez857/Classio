"""fake_classio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from polls import views

from django.contrib.auth import views as auth_views

from django.contrib.auth.views import (
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
    # these are the two new imports
    password_change,
    password_change_done,
)


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'$^', 'dashboard.views.index', name='root'),
    url(r'^login/$', 'dashboard.views.login_user'),
    url(r'^new/$', 'chat.views.new_room', name='new_room'),
    url(r'^questions/$', 'chat.views.chat_room', name='chat_room'),
    #url(r'^(?P<label>[\w-]{,50})/$', 'chat.views.chat_room', name='chat_room'),
    url(r'^slides/$', 'dashboard.views.index'),
    url(r'^audio/$', 'dashboard.views.audio', name='audio_stream'),
    url(r'^polls/$', 'polls.views.index', name="polls"),
    url(r'^polls/(?P<poll_id>\d+)/$', 'polls.views.detail', name='detail'),
    url(r'^polls/(?P<poll_id>\d+)/results/$', 'polls.views.results', name='results'),
    url(r'^polls/(?P<poll_id>\d+)/vote/$', 'polls.views.vote', name='vote'),
    url(r'^change-password/', 'django.contrib.auth.views.password_change',
        {'post_change_redirect': '/password-changed/'}),
    url(r'^password-changed/', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^clarity/$', 'dashboard.views.clarity', name='clarity_rating'),

    url(r'^add_poll/$', 'polls.views.add_poll', name='add_poll'),
    url(r'^add_choice/$', 'polls.views.add_choice', name='add_choice'),
    url(r'^delete_poll/(?P<poll_id>\d+)/$', 'polls.views.delete_poll', name='delete_poll'),

    url(r'^startdarkice/$', 'dashboard.views.startDarkIce'),
    url(r'^stopdarkice/$', 'dashboard.views.stopDarkIce'),

    url(r'^startclarity/$', 'dashboard.views.startClarity'),
    url(r'^stopclarity/$', 'dashboard.views.stopClarity'),

    ]


