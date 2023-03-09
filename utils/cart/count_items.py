from carts.models import Cart


def count_items(cart: Cart) -> int:
    all_products = cart.cartproduct_set.all()
    return sum([product.amount for product in all_products])
