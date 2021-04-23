from django.contrib.auth.models import User
from django.db import models


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

    owner = models.ForeignKey(User, verbose_name='author')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='created_time')

    class Meta:
        verbose_name = verbose_name_plural = 'link'


class Sidebar(models.Model):
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_SHOW, 'show'),
        (STATUS_HIDE, 'hide'),
    )

    SIDE_TYPE = (
        (1, 'HTML'),
        (2, 'latest articles'),
        (3, 'hot articles'),
        (4, 'recent articles'),
    )

    title = models.CharField(max_length=50, verbose_name='title')
    display_type = models.PositiveIntegerField(default=1, choices=SIDE_TYPE,
                                               verbose_name='show type')
    content = models.CharField(max_length=500, blank=True, verbose_name='content',
                               help_text='if setting is not HTML, it can be NULL')
    status = models.PositiveIntegerField(default=STATUS_SHOW,
                                         choices=STATUS_ITEMS, verbose_name='status')
    weight = models.PositiveIntegerField(default=1, choices=zip(range(1, 6),
                                                                range(1, 6)), verbose_name='weight',
                                         help_text='weight is bigger, order forward')

    owner = models.ForeignKey(User, verbose_name='author')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='created_time')

    class Meta:
        verbose_name = verbose_name_plural = 'sidebar'
