from django.contrib import admin
from projects.models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('hermes_cod', 'project_name', 'first_name', 'last_name',)
    list_filter = ('project_state', 'call_type', 'faculty', 'departament',)

