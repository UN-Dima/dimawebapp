from django.contrib import admin
from .models import QuipuProject
# Register your models here.


# class Row_QuipuProjectAdmin(admin.StackedInline):
    # model = Row_QuipuProject
    # extra = 1

# class Recurso_QuipuProjectAdmin(admin.StackedInline):
    # model = Recurso_QuipuProject
    # extra = 1


@admin.register(QuipuProject)
class QuipuProjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'proyecto', 'empresa')
    # list_filter = ('inventors', 'patent_type', 'departament', 'grant', 'filling', 'publication')
    list_display_links = ['code']

    # inlines = [Row_QuipuProjectAdmin,
               # ]
