from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^$', 'config.views.index', name='config_index'),

    url(r'^generateCA/$', 'config.views.generateCA', name='config_generateCA'),

#    url(r'^monitor/$', 'mdm.views.index'),
#    url(r'^monitor/detail/(?P<udid>[a-zA-Z0-9\-]+)/$', 'mdm.views.detail'),
#    url(r'^monitor/detail/(?P<udid>[a-zA-Z0-9\-]+)/api$', 'mdm.views.monitor_detail_api'),
#    url(r'^monitor/detail/(?P<udid>[a-zA-Z0-9\-]+)/profile/$', 'mdm.views.install_profile'),
#    url(r'^monitor/detail/(?P<udid>[a-zA-Z0-9\-]+)/push/$', 'mdm.views.send_push'),
)
