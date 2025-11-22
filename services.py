def build_product(name, quantity, price):
    return {
        'name': name,
        'quantity': quantity,
        'price': price,
        'total_cost': price * quantity
    }
