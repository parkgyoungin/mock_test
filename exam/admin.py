from django.contrib import admin
from .models import *

admin.site.register(Certificate)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Subject)
admin.site.register(Report)
admin.site.register(SubmitQuestion)

