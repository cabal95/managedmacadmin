from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='monitor/')),

    url(r'^checkin$', 'mdm.views.checkin'),
    url(r'^enroll$', 'mdm.views.enroll'),

    url(r'^monitor/$', 'mdm.views.index'),
    url(r'^monitor/detail/(?P<udid>[a-zA-Z0-9\-]+)/$', 'mdm.views.detail', name='device_detail'),
    url(r'^monitor/detail/(?P<udid>[a-zA-Z0-9\-]+)/api$', 'mdm.views.monitor_detail_api'),
    url(r'^monitor/detail/(?P<udid>[a-zA-Z0-9\-]+)/profile/$', 'mdm.views.install_profile'),
    url(r'^monitor/detail/(?P<udid>[a-zA-Z0-9\-]+)/push/$', 'mdm.views.send_push'),
    url(r'^monitor/detail/(?P<udid>[a-zA-Z0-9\-]+)/info/$', 'mdm.views.device_information'),
    url(r'^monitor/detail/(?P<udid>[a-zA-Z0-9\-]+)/profiles/$', 'mdm.views.profile_list'),
    url(r'^monitor/detail/(?P<udid>[a-zA-Z0-9\-]+)/apps/$', 'mdm.views.application_list'),
    url(r'^monitor/detail/(?P<udid>[a-zA-Z0-9\-]+)/preference/(?P<ident>[a-zA-Z0-9\-\._]+)/$', 'mdm.preferences_views.device', name='device_preference_edit'),

    url(r'^groups/$', 'mdm.groups_views.index', name='groups_index'),
    url(r'^groups/(?P<id>[a-zA-Z0-9\-]+)/$', 'mdm.groups_views.detail', name='devicegroup_detail'),
    url(r'^groups/(?P<id>[a-zA-Z0-9\-]+)/api/$', 'mdm.groups_views.api'),
    url(r'^groups/(?P<id>[a-zA-Z0-9\-]+)/preference/(?P<ident>[a-zA-Z0-9\-\._]+)/$', 'mdm.preferences_views.devicegroup', name='devicegroup_preference_edit'),
)
