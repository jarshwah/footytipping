from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

# includes
urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^tipping/', include('tipping.urls', namespace='tipping')),
)

urlpatterns += staticfiles_urlpatterns()

# site urls
urlpatterns += (
    url(r'^index/$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
)
