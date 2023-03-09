from carts.models import Cart


def sum_total_price(cart: Cart) -> int:
    all_products = cart.cartproduct_set.all()
    return sum([product.amount * product.product.price for product in all_products])
