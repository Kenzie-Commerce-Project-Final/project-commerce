from carts.models import Cart, CartProduct


def sum_total_price(cart: Cart) -> int:
    all_products = CartProduct.objects.filter(cart=cart)
    return sum([product.amount * product.product.price for product in all_products])
