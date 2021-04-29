from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from blog.custom_site import custom_site
from .models import Category, Post, Tag
from .adminforms import PostAdminForm
from blog.base_admin import BaseOwnerAdmin


class PostLine(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostLine, ]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        """
        count the numbers of articles
        :param obj:
        :return: the numbers of articles
        """
        return obj.post_set.count()

    post_count.short_description = "the numbers of articles"


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """The custom filter only displays the current user category"""

    title = 'category filter'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    forms = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator'
    ]
    # click to access the edit page
    list_display_links = []

    list_filter = [CategoryOwnerFilter, ]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    # edit page
    save_on_top = True
    exclude = ['owner']  # don't show

    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    fieldsets = (
        ('infrastructure configuration', {
            'description': 'infrastructure configuration description',
            'fields': (
                ('title', 'category'),
                'status'
            )
        }),
        ('content', {
            'fields': (
                'desc',
                'content'
            ),
        }),
        ('extra information', {
            'classes': ('collapse',),
            'fields': ('tag',),
        })
    )
    # filter_horizontal = ('tag', )
    filter_vertical = ('tag',)

    class Media:
        css = {
            'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/"
                    "bootstrap.min.css",),
        }
        js = ('https://cdn,bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)

    def operator(self, obj):
        return format_html(
            '<a href="{}">edit</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = 'operate'


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user',
                    'change_message']