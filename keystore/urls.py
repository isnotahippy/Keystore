from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'keystore.views.home', name='home'),
    # url(r'^keystore/', include('keystore.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^list/', 'keys.views.keypair_list', {}, 'list'),
    url(r'^add/', 'keys.views.keypair_edit', {}, 'keypair_add'),
    url(r'^edit/(?P<keyid>\d+)/$', 'keys.views.keypair_edit', {}, 'keypair_edit')
)
