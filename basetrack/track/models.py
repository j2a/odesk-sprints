from django.db import models
from django_odesk.task import abstract


class Task(abstract.BaseTask):

    description = models.TextField(null=True)

    @models.permalink
    def get_absolute_url(self):
        return 'track_task_details', [self.pk]
