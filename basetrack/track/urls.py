from django.conf.urls.defaults import *

urlpatterns = patterns(
    'basetrack.track.views',
    url(r'^list/$',
        'tasks_list', name='track_tasks_list'),
    url(r'^task/(?P<task_id>\d+)/$',
        'task_details', name='track_task_details'),
    url(r'^task/(?P<task_id>\d+)/(?P<slug>[\w\d-]+)/$',
        'task_details_slug', name='task_details_slug')
)
