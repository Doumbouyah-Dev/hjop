from django import template

register = template.Library()


@register.simple_tag
def is_bookmarked(opportunity, user):
    if not user.is_authenticated:
        return False
    return opportunity.bookmarked_by.filter(user=user).exists()