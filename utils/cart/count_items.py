from carts.models import Cart, CartProduct


def count_items(cart: Cart) -> int:
    all_products = CartProduct.objects.filter(cart=cart)
    return sum([product.amount for product in all_products])
