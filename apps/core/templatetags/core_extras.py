from django import template

register = template.Library()


@register.filter
def split(value, delimiter=","):
    return value.split(delimiter)

@register.filter
def required_marker(field):
    """Returns ' *' if the field is required, else empty string — for consistent form labels."""
    return " *" if field.field.required else ""

@register.inclusion_tag("core/partials/field_errors.html")
def field_errors(field):
    return {"errors": field.errors}