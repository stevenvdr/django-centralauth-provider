from django.conf.urls.defaults import *

urlpatterns = patterns('centralauth_provider.views',
	url(r'^authenticate/$', 'authenticate', name='registration'),
)

