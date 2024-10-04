from django.contrib import admin
from .models import Course, Subject, Institute, Discussion

admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Institute)
admin.site.register(Discussion)
