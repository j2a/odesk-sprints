from basetrack.track import models as track
from django.contrib import admin

class TaskAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'owner', 'state')

    def state(self, obj):
        return obj.state.name

admin.site.register(track.Task, TaskAdmin)
