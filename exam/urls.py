from django.urls import path
from .views import *

app_name = 'exam'

urlpatterns = [
    path('', show_certificates, name='certificates'),
    path('certificate=<int:id>/', show_tests, name='tests'),
    path('test=<int:id>/', show_detail, name='detail'),
    path('report=<int:id>/', show_report, name='report')
]