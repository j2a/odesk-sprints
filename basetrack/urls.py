from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()


def root(request):
    from django.http import HttpResponseRedirect
    from django.core.urlresolvers import reverse

    if request.user.is_authenticated():
        return HttpResponseRedirect(
            reverse('index'))
    else:
        return HttpResponseRedirect(
            reverse('django_odesk.auth.views.authenticate'))


urlpatterns = patterns(
    '',
    url(r'^$', root, name='root'),
    url(r'^odesk-auth/', include('django_odesk.auth.urls')),
    url(r'^manage/', include(admin.site.urls)),
)
