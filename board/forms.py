from django import forms
from .models import Announcement, Event, TimetableEntry, Result

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'body', 'expiry_date', 'status', 'is_pinned']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_datetime', 'end_datetime', 'venue', 'organizer_contact']

class TimetableEntryForm(forms.ModelForm):
    class Meta:
        model = TimetableEntry
        fields = '__all__'

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['title', 'file', 'level', 'session']
