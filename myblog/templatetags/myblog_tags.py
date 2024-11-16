from django import template

from myblog.models import Post


register = template.Library()


@register.inclusion_tag("myblog/tags/recent_posts.html")
def get_recent_posts():
    recent_posts = Post.objects.order_by("-id")[:5]
    return {"recent_posts": recent_posts}
