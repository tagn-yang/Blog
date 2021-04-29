from django.db import models

from blog_app.models import Post


class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, 'normal'),
        (STATUS_DELETE, 'delete'),
    )
    target = models.CharField(max_length=100, verbose_name="comment target")
    content = models.CharField(max_length=2000, verbose_name="content")
    nickname = models.CharField(max_length=50, verbose_name="nickname")
    website = models.URLField(verbose_name="website")
    email = models.EmailField(verbose_name="email")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="status")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="created_time")

    class Meta:
        verbose_name = verbose_name_plural = 'comment'

    def __str__(self):
        return self.target
    # @classmethod
    # def get_by_target(cls, target):
    #     return cls.objects.filter(target=target, status=cls.STATUS_NORMAL)

    @classmethod
    def get_by_target(cls, target):
        return cls.objects.filter(target=target, status=cls.STATUS_NORMAL)