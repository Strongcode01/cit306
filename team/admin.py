from django.contrib import admin
from .models import TeamMember

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'matric_number', 'project_role')
    search_fields = ('full_name', 'matric_number', 'project_role')
