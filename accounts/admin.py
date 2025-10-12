from django.contrib import admin
from .models import AllowedMatric, Profile

@admin.register(AllowedMatric)
class AllowedMatricAdmin(admin.ModelAdmin):
    list_display = ("matric_number", "used", "created_at", "updated_at")
    search_fields = ("matric_number",)
    list_filter = ("used",)
    ordering = ("matric_number",)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "matric_number", "department", "is_team_member")
    list_filter = ("is_team_member", "department")
    search_fields = ("user__username", "matric_number", "user__first_name", "user__last_name")
