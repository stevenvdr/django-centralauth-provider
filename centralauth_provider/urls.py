from django.conf.urls.defaults import *

urlpatterns = patterns('centralauth_provider.views',
    url(r'^authenticate/$', 'authenticate', name='authenticate'),
    url(r'^get_attributes/$', 'get_attributes', name='get_attributes'),
)

