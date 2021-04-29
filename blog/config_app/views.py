from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from blog_app.views import CommentViewMixin
from .models import Link


def links(request):
    return HttpResponse('links')


class LinkListView(CommentViewMixin, ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = '/config/links.html'
    context_object_name = 'link_list'
