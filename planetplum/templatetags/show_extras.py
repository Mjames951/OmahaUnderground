from django import template

register = template.Library()

def show_price_pwyc(show):
    """
    return price summary
    """
    price_str = "FREE" if not show.price or show.price == 0 else f"${show.price}"
    pwyc_str = "(PWYC)" if show.pwyc else ""
    return f"{price_str} {pwyc_str}"

@register.simple_tag
def show_price(show):
    return show_price_pwyc(show)
