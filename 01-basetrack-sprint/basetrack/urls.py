from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()


def root(request):
    from django.http import HttpResponseRedirect
    from django.core.urlresolvers import reverse

    if request.user.is_authenticated():
        return HttpResponseRedirect(
            reverse('track_tasks_list'))
    else:
        return HttpResponseRedirect(
            reverse('django_odesk.auth.views.authenticate'))


urlpatterns = patterns(
    '',
    url(r'^$', root, name='root'),
    url(r'^track/', include('basetrack.track.urls')),
    url(r'^odesk-auth/', include('django_odesk.auth.urls')),
    url(r'^manage/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^assets/(.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
