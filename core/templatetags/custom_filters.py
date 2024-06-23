from django import template

register = template.Library()

@register.filter
def simplify_distance_unit(distance_km):
    """
    Convert distance to meters if less than 1 km, otherwise return km.
    """
    if distance_km < 1:
        return f"{distance_km * 1000:.2f} m"
    else:
        return f"{distance_km:.2f} km"