from django.contrib import admin
from .models import Subject, StudyTask, StudySession, StudySchedule

admin.site.register(Subject)
admin.site.register(StudyTask)
admin.site.register(StudySession)
admin.site.register(StudySchedule)