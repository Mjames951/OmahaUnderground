from django import template

register = template.Library()

def show_price_pwyc(show):
    """
    return price summary
    """
    if show.price == 0:
        price_str = "FREE"
    elif show.price is None:
        price_str = ""
    else:
        price_str = f"${show.price}"
        
    pwyc_str = "(PWYC)" if show.pwyc else ""

    return f"{price_str} {pwyc_str}"

@register.simple_tag
def show_price(show):
    return show_price_pwyc(show)