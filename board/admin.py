from django.contrib import admin
from .models import Announcement, Event, TimetableEntry, Result

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date', 'status', 'is_pinned')
    list_filter = ('status', 'is_pinned')
    search_fields = ('title', 'body')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_datetime', 'venue')
    search_fields = ('title', 'description')

@admin.register(TimetableEntry)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'level', 'semester', 'day', 'start_time')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'session', 'uploaded_by', 'upload_date')
