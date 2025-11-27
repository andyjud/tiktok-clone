from django import template
from ..models import Follow

register = template.Library()

@register.filter
def is_following(user, this_user):
    is_following = Follow.objects.filter(follower=user, following=this_user).exists()
    return is_following