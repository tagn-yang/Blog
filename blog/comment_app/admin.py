from django.contrib import admin

from blog.custom_site import custom_site
from .models import Comment
from blog.base_admin import BaseOwnerAdmin


@admin.register(Comment, site=custom_site)
class CommentAdmin(BaseOwnerAdmin):
    list_display = ('target', 'nickname', 'website', 'content', 'created_time')