import markdown2
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def render_markdown(text):
    """
    Renders article content written in Markdown as safe HTML.
    Lets content authors (via Django admin) use **bold**, # headers,
    - lists, and [links](url) without needing a rich-text editor.
    """
    html = markdown2.markdown(
        text,
        extras=["fenced-code-blocks", "tables", "break-on-newline"],
    )
    return mark_safe(html)