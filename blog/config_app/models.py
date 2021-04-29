from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string


class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, 'normal'),
        (STATUS_DELETE, 'delete'),
    )

    title = models.CharField(max_length=50, verbose_name='title')
    href = models.URLField(verbose_name='link')  # default_length=200
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name='status')
    weight = models.PositiveIntegerField(default=1, choices=zip(range(1, 6),
                                                                range(1, 6)), verbose_name='weight',
                                         help_text='weight is bigger, order forward')

    owner = models.ForeignKey(User, verbose_name='author', on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='created_time')

    class Meta:
        verbose_name = verbose_name_plural = 'link'

    def __str__(self):
        return self.title


class SideBar(models.Model):
    DISPLAY_HTML = 1
    DISPLAY_LATEST = 2
    DISPLAY_HOT = 3
    DISPLAY_COMMENT = 4
    SIDE_TYPE = (
        (DISPLAY_HTML, 'HTML'),
        (DISPLAY_LATEST, 'latest articles'),
        (DISPLAY_HOT, 'hot articles'),
        (DISPLAY_COMMENT, 'recent articles'),
    )
    # objects = None
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_SHOW, 'show'),
        (STATUS_HIDE, 'hide'),
    )

    # SIDE_TYPE = (
    #     (1, 'HTML'),
    #     (2, 'latest articles'),
    #     (3, 'hot articles'),
    #     (4, 'recent articles'),
    # )
    title = models.CharField(max_length=50, verbose_name='title')
    display_type = models.PositiveIntegerField(default=1, choices=SIDE_TYPE,
                                               verbose_name='show type')
    content = models.CharField(max_length=500, blank=True, verbose_name='content',
                               help_text='if setting is not HTML type, it can be NULL')
    status = models.PositiveIntegerField(default=STATUS_SHOW,
                                         choices=STATUS_ITEMS, verbose_name='status')
    weight = models.PositiveIntegerField(default=1, choices=zip(range(1, 6),
                                                                range(1, 6)), verbose_name='weight',
                                         help_text='weight is bigger, order forward')

    owner = models.ForeignKey(User, verbose_name='author', on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='created_time')

    class Meta:
        verbose_name = verbose_name_plural = 'sidebar'

    def __str__(self):
        return self.title

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_SHOW)

    @property
    def content_html(self):
        """direct rendering of templates"""
        from blog.blog_app.models import Post
        from blog.comment_app.models import Comment

        result = ''
        if self.display_type == self.DISPLAY_HTML:
            result = self.content
        elif self.display_type == self.DISPLAY_LATEST:
            context = {
                'posts': Post.latest_posts()
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_HOT:
            context = {
                'posts': Post.hot_posts()
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_COMMENT:
            context = {
                'posts': Comment.objects.filter(status=Comment.STATUS_NORMAL)
            }
            result = render_to_string('config/blocks/sidebar_comments.html', context)

        return result
