from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.conf import settings
# from admin_interface.models import Theme

# admin.site.unregister(Group)
# admin.site.unregister(User)

# if not settings.DEBUG:
#     admin.site.unregister(Theme)


# class Data_ContentAdmin(admin.StackedInline):
#     model = Attachment_Content
#     extra = 1


# @admin.register(Content)
# class ContentAdmin(SummernoteModelAdmin):
    # list_display = ('label', 'content',)
    # list_display_links = ['label']
    # summernote_fields = ('content',)
