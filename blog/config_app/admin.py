from django.contrib import admin

from blog.custom_site import custom_site
from .models import Link, SideBar
from blog.base_admin import BaseOwnerAdmin


@admin.register(Link, site=custom_site)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'weight', 'status', 'created_time')
    fields = ('title', 'href', 'status', 'weight')


@admin.register(SideBar, site=custom_site)
class SidebarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')

