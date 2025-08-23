from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('archived', 'Archived'),
]

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_pinned = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_pinned', '-publish_date']

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    venue = models.CharField(max_length=255, blank=True)
    organizer_contact = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class TimetableEntry(models.Model):
    level = models.CharField(max_length=50)
    semester = models.CharField(max_length=50)
    course_code = models.CharField(max_length=50)
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.course_code} — {self.day} {self.start_time}'

class Result(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='results/', null=True, blank=True)
    level = models.CharField(max_length=50)
    session = models.CharField(max_length=50)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
