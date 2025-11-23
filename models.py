def build_product(name, quantity, price):
    """ Builds a product dictionary with total_cost.
    Parameters:
    - name: str, product name
    - quantity: int, product quantity
    - price: float, product price
    Returns:
     A dictionary with keys: name, quantity, price, total_cost
    """
    return {
        'name': name,
        'quantity': quantity,
        'price': price,
        'total_cost': price * quantity
    }
