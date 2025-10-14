from django.db import models

class TeamMember(models.Model):
    full_name = models.CharField(max_length=200)
    matric_number = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    project_role = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    github = models.URLField(blank=True)
    responsibilities = models.TextField(blank=True)

    def __str__(self):
        return f'{self.full_name} ({self.matric_number})'
