from django.db import models
from django_odesk.task import abstract
from workflows import utils, models as workflows


class TaskState(object):

    def __get__(self, instance, cls):
        state = utils.get_state(instance)
        if state is None:
            self.__set__(instance, instance.workflow.initial_state)
            return instance.workflow.initial_state
        return state

    def __set__(self, instance, value):
        utils.set_state(instance, value)


class Task(abstract.BaseTask):

    description = models.TextField(null=True)
    workflow = models.ForeignKey(workflows.Workflow)

    state = TaskState()

    @models.permalink
    def get_absolute_url(self):
        return 'track_task_details', [self.pk]


    def do_transition(self, transition=None, user=None):
        if user is None:
            user = self.owner
        if transition is None:
            possible = self.state.get_allowed_transitions(self, user)
            if len(possible) == 0:
                raise ValueError("There is no any possible transitions "
                                 "for %r" % self)
            elif len(possible) > 1:
                raise ValueError("Transition is not defined and there are "
                                 "many possible transitions for %r" % self)
            transition = possible[0]
        utils.do_transition(self, transition, user)


def update_odesk_task(sender, instance, created, **kwargs):
    state = instance.state
    obj = instance.content
    actions = {
        'Accepted': 'create_odesk_task',
        'Closed': 'delete_odesk_task'}
    # XXX: Weak. We make lock to some DB content: what if
    # we will change Accepted to Assigned?
    # Need to have some "state-related info", like
    # http://bitbucket.org/diefenbach/django-lfc/src/f67eed8ab3f5/lfc/models.py#cl-56
    # and rely on info in WorkflowStatesInformation instance. Like
    # the owner of task, should we create or delete odesk task code, etc.
    if state.name not in actions:
        return
    action_name = actions[state.name]
    if hasattr(obj, action_name):
        getattr(obj, action_name)()

models.signals.post_save.connect(
    update_odesk_task,
    sender=workflows.StateObjectRelation,
    dispatch_uid='basetrack.track.update_odesk_task')
