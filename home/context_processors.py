from .models import Category


def cart_data(request):

    cart = request.session.get("cart", {})

    cart_count = sum(cart.values())

    try:
        categories = Category.objects.prefetch_related("subcategories").all()
    except Exception:
        categories = []

    return {
        "cart_count": cart_count,
        "categories": categories,
    }