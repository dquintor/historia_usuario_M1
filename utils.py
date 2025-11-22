def get_product_by_name(inventory, name):
    """Return the product dict with the given name, or None if not found."""
    normalized_name = name.strip().capitalize()
    return next((p for p in inventory if p["name"] == normalized_name), None)

def recalc_total_cost(product):
    """Ensure product has a correct total_cost field."""
    price = product.get("price", 0)
    quantity = product.get("quantity", 0)
    product["total_cost"] = price * quantity
    return product["total_cost"]

def recalc_total_cost_for_inventory(inventory):
    for product in inventory:
        recalc_total_cost(product)
def display_result(name, quantity, price, total_cost=None):
    """
    Returns a formatted string with product info.
    If total_cost is not provided, it is calculated as price * quantity.
    """
    if total_cost is None:
        total_cost = price * quantity

    product_info = (
        f"\nName: {name} | Unit Price: {price} | "
        f"Stock Quantity: {quantity} | Total Stock Value: {total_cost}"
    )
    return product_info

def print_product(product, index=None):
    """
    Print a single product nicely formatted.
    If index is provided, show 'Product {index}:' before details.
    """
    total_cost = product.get("total_cost")
    header = f"\nProduct {index}:" if index is not None else "\nProduct:"
    print(header + display_result(
        product["name"],
        product["quantity"],
        product["price"],
        total_cost
    ))

def ensure_inventory_not_empty(inventory, action_description="perform this action"):
    """
    Returns True if inventory is NOT empty.
    If empty, prints a message and returns False.
    """
    if not inventory:
        print(f"Inventory is empty. Please add products before trying to {action_description}.")
        return False
    return True
