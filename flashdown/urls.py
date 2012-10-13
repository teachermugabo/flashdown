from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/?$', 'flashdown.views.home', name='home'),
    url(r'^decks/', include('decks.urls')),
)

# admin documentation:
# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

# admin:
# url(r'^admin/', include(admin.site.urls)),
