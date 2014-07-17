from django.contrib import admin
from .models import Page

class PageAdmin(admin.ModelAdmin):
    search_fields = ['name', 'slug']
    list_display = ['name', 'slug']

admin.site.register(Page, PageAdmin)
