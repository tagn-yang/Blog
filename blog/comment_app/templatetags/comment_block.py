from django import template

from comment_app.forms import CommentForm
from comment_app.models import Comment

register = template.Library()


@register.inclusion_tag('comment/block.html')
def comment_block(target):
    return {
        'target': target,
        'comment_form': CommentForm(),
        'comment_list': Comment.get_by_target(target),
    }
