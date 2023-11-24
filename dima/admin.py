from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.conf import settings
from admin_interface.models import Theme
from .models import Newsletter, Broadcast, Team, Content, Attachment_Content, UpdateFiles

admin.site.unregister(Group)
# admin.site.unregister(User)

if not settings.DEBUG:
    admin.site.unregister(Theme)


class Attachment_ContentAdmin(admin.StackedInline):
    model = Attachment_Content
    extra = 1


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('upload', 'file')
    exclude = ('thumbnail',)
    list_display_links = ['upload']


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ('upload', 'expiration', 'title', 'link', 'active')
    list_display_links = ['upload']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('area',)
    list_display_links = ['area']


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('label', 'content',)
    list_display_links = ['label']
    inlines = [Attachment_ContentAdmin,
               ]

@admin.register(UpdateFiles)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('table_to_update', 'file', 'upload_date')
    list_display_links = ['table_to_update']

# @admin.register(Content)
# class ContentAdmin(SummernoteModelAdmin):
    # list_display = ('label', 'content',)
    # list_display_links = ['label']
    # summernote_fields = ('content',)
