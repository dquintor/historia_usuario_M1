def validate_product_name(user_input):
    """
    Validate and normalize a product name.

    Rules:
    - Not empty after stripping spaces
    - Only letters and spaces
    - Capitalize first letter
    parameters:
    - user_input: str, raw input from user
    returns:
    - normalized name string
    """
    name = user_input.strip().capitalize()

    if not name:
        raise ValueError("Product name can’t be empty. Please enter it to continue.")

    if not all(c.isalpha() or c.isspace() for c in name):
        raise ValueError("The product name must contain only letters and spaces.")

    return name


def validate_price(user_input):
    """
    Validate and convert product price.

    Rules:
    - Not empty
    - Numeric (float)
    - Greater than 0
    parameters:
    - user_input: str, raw input from user
    returns:
    - price as float
    
    """
    text = user_input.strip()

    if not text:
        raise ValueError("The price cannot be empty.")

    price_value = float(text)

    if price_value <= 0:
        raise ValueError("The price must be greater than 0.")

    return price_value


def validate_quantity(user_input):
    """
    Validate and convert product quantity.

    Rules:
    - Not empty
    - Integer (no decimals)
    - Greater than 0
    parameters:
    - user_input: str, raw input from user
    returns:
    - quantity as int
    
    """
    text = user_input.strip()

    if not text:
        raise ValueError("The quantity field cannot be empty.")

    quantity_value = int(text)

    if quantity_value <= 0:
        raise ValueError("The quantity must be greater than 0.")

    return quantity_value



def get_product_by_name(inventory, name):
    """Return the product dict with the given name, or None if not found.
    parameters:
    - inventory: list of product dicts
    - name: str, product name to search for
    returns:
    - product dict if found, else None
    """
    normalized_name = name.strip().capitalize()
    return next((p for p in inventory if p["name"] == normalized_name), None)

def recalc_total_cost(product):
    """Ensure product has a correct total_cost field.
    parameters:
    - product: dict with keys name, price, quantity
    returns:
    - total_cost as float
    """
    price = product.get("price", 0)
    quantity = product.get("quantity", 0)
    product["total_cost"] = price * quantity
    return product["total_cost"]

def recalc_total_cost_for_inventory(inventory):
    """Recalculate total_cost for all products in inventory.
    parameters:
    - inventory: list of product dicts
    returns: None
    """
    for product in inventory:
        recalc_total_cost(product)
def display_result(name, quantity, price, total_cost=None):
    """
    Returns a formatted string with product info.
    If total_cost is not provided, it is calculated as price * quantity.
    parameters:
    - name: str, product name
    - quantity: int, product quantity
    - price: float, product price
    - total_cost: float or None, total cost of the product
    returns:
    - formatted string with product details
    
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
    parameters:
    - product: dict with keys name, quantity, price, total_cost
    - index: int or None, optional product index for display
    returns: None
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
    parameters:
    - inventory: list of product dicts
    - action_description: str, description of the action user wanted to do
    returns:
    - True if inventory not empty, else False
    
    """
    if not inventory:
        print(f"Inventory is empty. Please add products before trying to {action_description}.")
        return False
    return True
