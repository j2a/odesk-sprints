from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django import http
from django.core.urlresolvers import reverse
from basetrack.track import models


def tasks_list(request):
    task_list = models.Task.objects.filter(owner=request.user)
    states = set()
    grouped = {}
    for task in task_list:
        states = states.union(set(task.workflow.states.all()))
        grouped[task.state] = grouped.get(task.state, []) + [task]
    grouped_list = [{'title': s.name, 'task_list': grouped.get(s, [])}
                    for s in states]
    return render_to_response(
        'track/tasks_list.html',
        {'grouped_task_list': grouped_list},
        context_instance=RequestContext(request))


def task_details(request, task_id):
    task = models.Task.objects.get(pk=task_id)
    slug = slugify(task.title)
    return http.HttpResponseRedirect(
        reverse('task_details_slug', args=[task_id, slug]))


def task_details_slug(request, task_id, slug):
    task = models.Task.objects.get(pk=task_id)
    task_slug = slugify(task.title)
    if task_slug != slug:
        return http.HttpResponseRedirect(
            reverse('task_details_slug', args=[task_id, task_slug]))
    return render_to_response(
        'track/task_details.html',
        {'task': task},
        context_instance=RequestContext(request))
