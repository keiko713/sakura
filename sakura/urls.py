from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'tweets.views.index'),
    url(r'^api/add_blacklist$', 'tweets.views.add_blacklist'),
    url(r'^page/(?P<page_id>\d+)/$', 'tweets.views.get_page'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
