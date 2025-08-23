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
    list_display = ("user", "matric_number", "serial_number", "department", "newsletter")
    search_fields = ("user__username", "matric_number", "serial_number")
    list_filter = ("newsletter",)
