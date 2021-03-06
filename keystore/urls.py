from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'interface.views.content.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^list/', 'keys.views.keypair_list', {}, 'list'),

    url(r'^api/keypair/(?P<id>\d+)$', 'keys.views.keypair_api_specific'),
    url(r'^api/keypair/', 'keys.views.keypair_api_general'),

    # url(r'^login/', 'django.contrib.auth.views.login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^login-error/', 'interface.views.users.error'),

    url(r'', include('social_auth.urls')),
)
