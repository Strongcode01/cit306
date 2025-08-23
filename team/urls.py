from django.urls import path
from . import views

app_name = 'team'

urlpatterns = [
    path('credentials/', views.credentials, name='credentials'),
]
