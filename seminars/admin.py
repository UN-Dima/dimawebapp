from django.contrib import admin
from .models import Seminars


@admin.register(Seminars)
class SeminarsAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'leader', 'faculty', 'departament')
    list_filter = ('founded', 'faculty', 'departament', 'knowledge_area')
    list_display_links = ['code', "leader"]


