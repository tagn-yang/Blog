from django.contrib import admin

from blog.custom_site import custom_site
from .models import Link, Sidebar
from blog.base_admin import BaseOwnerAdmin


@admin.register(Link, site=custom_site)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'weight', 'status', 'created_time')
    fields = ('title', 'href', 'status', 'weight')


@admin.register(Sidebar, site=custom_site)
class SidebarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SidebarAdmin, self).save_model(request, obj, form, change)
