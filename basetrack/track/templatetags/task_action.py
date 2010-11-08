from django.template import Library
from workflows import utils
from basetrack.track import models as track

register = Library()



@register.inclusion_tag('track/tags/task_action.html', takes_context=True)
def task_action(context, task):
    user = context['user']
    transitions = utils.get_allowed_transitions(task, user)
    next_transition = None
    if len(transitions) == 1:
        next_transition = transitions[0]
    return {'transitions': transitions, 'next_transition': next_transition}
