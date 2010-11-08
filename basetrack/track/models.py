from django.db import models
from django_odesk.task import abstract
from workflows import utils


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
    workflow = models.ForeignKey('workflows.Workflow')

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
