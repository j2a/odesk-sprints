from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django import http
from django.core.urlresolvers import reverse
from basetrack.track import models

@login_required
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

@login_required
def task_details(request, task_id):
    task = models.Task.objects.get(pk=task_id)
    if task.owner != request.user:
        # XXX: Better to handle it through django-permissions
        raise http.Http404
    slug = slugify(task.title)
    return http.HttpResponseRedirect(
        reverse('task_details_slug', args=[task_id, slug]))

@login_required
def task_details_slug(request, task_id, slug):
    task = models.Task.objects.get(pk=task_id)
    if task.owner != request.user:
        raise http.Http404

    task_slug = slugify(task.title)
    if task_slug != slug and request.method == 'GET':
        return http.HttpResponseRedirect(
            reverse('task_details_slug', args=[task_id, task_slug]))

    error = None
    if request.method == 'POST' and 'transition' in request.POST:
        try:
            transition = int(request.POST['transition'][0])
        except (TypeError, IndexError, KeyError):
            error = "Wrong transition parameter"
        try:
            task.do_transition(transition)
        except ValueError, e:
            error = "Transition failed: %s" % e
        else:
            return http.HttpResponseRedirect(
                reverse('track_tasks_list'))
    return render_to_response(
        'track/task_details.html',
        {'task': task, 'error': error},
        context_instance=RequestContext(request))
