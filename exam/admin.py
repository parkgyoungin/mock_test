from django.contrib import admin
from .models import Certificate, Test, Question, Choice, Subject

admin.site.register(Certificate)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Subject)

