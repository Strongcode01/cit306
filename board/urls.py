from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('announcements/', views.announcements_list, name='announcements'),
    path('announcement/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('events/', views.events_list, name='events'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('timetable/', views.timetable, name='timetable'),
    path('results/', views.results, name='results'),
    path('archive/', views.archive, name='archive'),
    path('search/', views.search, name='search'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
