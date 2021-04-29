import mistune
from django.contrib.auth.models import User
from django.db import models
from django.utils.functional import cached_property


class Category(models.Model):
    object = None
    objects = None
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, 'normal'),
        (STATUS_DELETE, 'delete'),
    )

    name = models.CharField(max_length=50, verbose_name='category_name')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name='status')

    is_nav = models.BooleanField(default=False, verbose_name='is or not nav')
    owner = models.ForeignKey(User, verbose_name='author', on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='created_time')

    class Meta:
        verbose_name = verbose_name_plural = 'category'

    def __str__(self):
        return self.name

    # @classmethod
    # def get_navs(cls):
    """
        two database requests generated, 2 i/o
    """
    #     categories = cls.objects.filter(status=cls.STATUS_NORMAL)
    #     nav_categories = categories.filter(is_nav=True)
    #     normal_categories = categories.filter(is_nav=False)
    #
    #     return {
    #         'navs': nav_categories,
    #         'categories': normal_categories,
    #     }

    @classmethod
    def get_navs(cls):
        """
        reconsitution get_navs, two database requests generated, 2 i/o
        :return: nav_categories, normal_categories
        """
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)

        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }


class Tag(models.Model):
    objects = None
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, 'normal'),
        (STATUS_DELETE, 'delete'),
    )

    name = models.CharField(max_length=10, verbose_name='tag_name')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name='status')
    owner = models.ForeignKey(User, verbose_name='author', on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='created_time')

    class Meta:
        verbose_name = verbose_name_plural = 'tag'

    def __str__(self):
        return self.name


class Post(models.Model):
    objects = None
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, 'normal'),
        (STATUS_DELETE, 'delete'),
        (STATUS_DRAFT, 'draft'),
    )

    title = models.CharField(max_length=225, verbose_name='title')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='summary')
    content = models.TextField(verbose_name='main body', help_text='main body must be MarkDown format')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name='status')
    category = models.ForeignKey(Category, verbose_name='category', on_delete=models.DO_NOTHING)
    tag = models.ManyToManyField(Tag, verbose_name='tag')
    owner = models.ForeignKey(User, verbose_name='author', on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='created_time')
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)
    content_html = models.TextField(verbose_name='Text html code', blank=True, editable=False)

    class Meta:
        verbose_name = verbose_name_plural = 'article'
        ordering = ['-id']  # order by desc

    def __str__(self):
        return self.title

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.object.get(id=tag_id)
        except Tag.DoseNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')

        return post_list, tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.object.get(id=category_id)
        except Category.DoseNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Category.STATUS_NORMAL).select_related('owner', 'category')

        return post_list, category

    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        return queryset

    @classmethod
    def host_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')

    def save(self, *args, **kwargs):
        self.content_html = mistune.Markdown(self.content)
        super().save(*args, **kwargs)

    @cached_property
    def tags(self):
        return ','.join(self.tag.values_list('name', flat=True))