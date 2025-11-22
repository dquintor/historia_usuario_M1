from models import build_product
from data import export_to_csv, import_from_csv, DEFAULT_PATH
from utils import (get_product_by_name,recalc_total_cost,recalc_total_cost_for_inventory,print_product,ensure_inventory_not_empty,
                   validate_price,validate_quantity, validate_product_name)

CSV_PATH = "inventory.csv"

"""INVENTORY PROGRAM """

# Global inventory list
inventory = []


def collect_data():
    """Collect product data from user input with validation.
    
    This function prompts interactively for product name, price, and quantity,
    ensuring valid inputs before returning them:
    - Product name: string with letters and spaces only, not empty.
    - Product price: floating-point number > 0.
    - Quantity: non-decimal integer > 0.
    
    Returns
    -------
    tuple
        (name: str, quantity: int, price: float)
    """
    
    name = None
    price = None
    quantity = None
    
    # Product name input and validation
    while name is None:
        try:
            user_input = input("Please enter the product name: ")
            name = validate_product_name(user_input)
        except ValueError as e:
            print(e)
        except KeyboardInterrupt:
            print("\nInput interrupted. Please try again.")
    
    # Product price input and validation
    while price is None:
        try:
            user_input = input("Enter the product price: ")
            price = validate_price(user_input)
        except ValueError as e:
            print(e)
        except KeyboardInterrupt:
            print("\nInput interrupted. Please try again.")
    
    # Product quantity input and validation
    while quantity is None:
        try:
            user_input = input("Enter the product quantity: ")
            quantity = validate_quantity(user_input)
        except ValueError as e:
            print(e)
        except KeyboardInterrupt:
            print("\nInput interrupted. Please try again.")
    
    return name, quantity, price


def stock_price(quantity, price):
    """Return total stock value for a product."""
    return price * quantity




def validate_option(menu, message, menu_started=True, minimum=None, maximum=None):
    """Validate user menu option input.
    
    Parameters
    ----------
    menu : str
        The menu text to display.
    message : str
        The prompt message for user input.
        menu_started : bool, optional
        Whether the menu loop is active. Default is True.
        minimum : int, optional
        Minimum valid option value. Default is None.
        maximum : int, optional
        Maximum valid option value. Default is None.
    
    Returns
    -------
    int
        The validated menu option selected by the user.
        """
    while menu_started:
        try:
            print(menu)
            option = int(input(message))
            if minimum is not None and option < minimum:
                print(f"Invalid option. Please select an option between {minimum} and {maximum}.")
                continue
            if maximum is not None and option > maximum:
                print(f"Invalid option. Please select an option between {minimum} and {maximum}.")
                continue
            return option
        except ValueError:
            print("Invalid input. Please enter a number.")


def menu():
    """Display the menu and get a validated user option.
    
    Returns
    -------
    int
        The validated menu option selected by the user."""
    
    menu_text = (
        "\n---- Options Menu ----\n"
        "1. Add Product\n"
        "2. Search Product\n"
        "3. Update Product\n"
        "4. Delete Product\n"
        "5. Show Inventory\n"
        "6. Statistics\n"
        "7. Save inventory to CSV\n"
        "8. Load inventory from CSV\n"
        "9. Exit\n"
    )
    option = validate_option(menu_text, "Select an option (1-9): ", menu_started=True, minimum=1, maximum=9)
    return option

def main():
    """Main function to run the inventory management system.
     Runs an interactive menu loop until the user chooses to exit."""
    
    print("Welcome to the Product Inventory Management System!")
    menu_started = True


    while menu_started:
        option = menu()

        if option == 1:
            # Add product
            name, quantity, price = collect_data()
            add_product(name, quantity, price)
            continue

        elif option == 2:
            # Search product
            search_product(inventory)
            continue

        elif option == 3:
            # Update product
            update_product(inventory)
            continue

        elif option == 4:
            # Delete product
            delete_product(inventory)
            continue

        elif option == 5:
            # Show inventory
            show_inventory(inventory)
            continue

        elif option == 6:
            # Statistics
            total_value, total_quantity, most_expensive_product, most_stocked_product = calculate_statistics(
                inventory
            )
            show_statistics(
                total_value,
                total_quantity,
                most_expensive_product,
                most_stocked_product,
            )
            continue

        elif option == 7:
            # Save to CSV
            export_to_csv(inventory, CSV_PATH)
            continue

        elif option == 8:
            # Load from CSV (overwrite or merge inside import_from_csv)
            new_inventory = import_from_csv(inventory, CSV_PATH)
            if new_inventory is not inventory:
                inventory.clear()
                inventory.extend(new_inventory)

            continue

        elif option == 9:
            # Exit
            menu_started = False
            print("Exiting the menu. See you later!")


def add_product(name, quantity, price):
    """Create a product and add it to the inventory.
    
    Parameters
    ----------
    name : str
        The product name.
    quantity : int
        The product quantity.
    price : float
        The product price.
        """
    global inventory
    product = build_product(name, quantity, price)  
    recalc_total_cost(product)  
    inventory.append(product)
    print(f"\n{quantity} units of the product {name} added to the inventory.\n")


def show_inventory(inv):
    """Print all products in the inventory.
    
    parameters
    ----------
    inv : list
        The inventory list of products."""
        
    print("\n--- Product Inventory ---\n")
    if not ensure_inventory_not_empty(inv, "view the inventory"):
        print(inv)
        return

    for index, product in enumerate(inv, start=1):
        print_product(product, index)


def calculate_statistics(inv):
    """Calculate basic inventory statistics.
    parameters
    ----------
    inv : list
        The inventory list of products.
        
    Returns
    -------
    tuple
        total_inventory_value : float
        Total value of all products in inventory.
        total_products : int
        Total number of product units in stock.
        most_expensive_product : float or None
        Price of the most expensive product, or None if inventory is empty.
        most_stocked_product : int or None
        Highest stock quantity of any product, or None if inventory is empty.
            """
    if not ensure_inventory_not_empty(inv, "calculate statistics"):
        return 0, 0, None, None

    recalc_total_cost_for_inventory(inv)

    total_inventory_value = sum(p["total_cost"] for p in inv)
    total_products = sum(p.get("quantity", 0) for p in inv)
    most_expensive_price = max(p.get("price", 0) for p in inv)
    most_stocked_quantity = max(p.get("quantity", 0) for p in inv)

    return total_inventory_value, total_products, most_expensive_price, most_stocked_quantity


def show_statistics(total_inventory_value, total_products, most_expensive_product, most_stocked_product):
    """Display inventory statistics.
    parameters
    ----------
    total_inventory_value : float
        Total value of all products in inventory.
    total_products : int
        Total number of product units in stock.
    most_expensive_product : float or None
        Price of the most expensive product, or None if inventory is empty.
    most_stocked_product : int or None
        Highest stock quantity of any product, or None if inventory is empty.
        """
        
    print("\n --- Inventory Statistics ---\n")
    print(f"Total Inventory Value: {total_inventory_value}")
    print(f"Total Number of Units in Stock: {total_products}")

    if most_expensive_product is not None:
        print(f"Most Expensive Product Price: {most_expensive_product}")
    else:
        print("Most Expensive Product Price: N/A")

    if most_stocked_product is not None:
        print(f"Product with Highest Stock Quantity: {most_stocked_product}")
    else:
        print("Product with Highest Stock Quantity: N/A")


""" WEEK 3 """


def search_product(inv):
    """Search for a product by name and show it.
    parameters
    ----------
    inv : list
        The inventory list of products."""
        
    if not ensure_inventory_not_empty(inv, "search products"):
        return None

    search_name = input("Enter the product name to search: ").strip()
    product = get_product_by_name(inv, search_name)

    if product:
        print("Product found:")
        print_product(product)
        return product

    print("Product not found in the inventory.")
    return None


def update_product(inventory):
    """Update a product's price and/or quantity by name.
    parameters
    ----------
    inventory : list
        The inventory list of products.
        """
        
    if not ensure_inventory_not_empty(inventory, "update a product"):
        return

    name = input("Enter the product name to update: ").strip()
    product = get_product_by_name(inventory, name)

    if product is None:
        print(f"Product '{name.capitalize()}' not found in the inventory.")
        return

    print("\nProduct found:")
    print_product(product)

    print("\nLeave any field empty to keep the current value.\n")

    # Update price
    new_price_input = input("Enter new price (or press Enter to keep current): ").strip()
    if new_price_input:
        try:
            new_price = validate_price(new_price_input)
            product["price"] = new_price
        except ValueError as e:
            print(e)

    # Update quantity
    new_quantity_input = input("Enter new quantity (or press Enter to keep current): ").strip()
    if new_quantity_input:
        try:
            new_quantity = validate_quantity(new_quantity_input)
            product["quantity"] = new_quantity
        except ValueError as e:
            print(e)

    recalc_total_cost(product)

    print("\nProduct updated successfully:")
    print_product(product)


def delete_product(inventory):
    """Delete a product from the inventory by name.
    parameters
    ----------
    inventory : list
        The inventory list of products.
        """

    if not ensure_inventory_not_empty(inventory, "delete a product"):
        return

    name = input("Enter the name of the product to delete: ").strip()
    product = get_product_by_name(inventory, name)

    if product is None:
        print(f"Product '{name.capitalize()}' not found in the inventory.")
        return

    print("\nProduct found:")
    print_product(product)

    confirmation = input(
        "Are you sure you want to delete this product? (Y/N): "
    ).strip().upper()

    if confirmation == "Y":
        inventory.remove(product)
        print(f"\nProduct '{product['name']}' has been removed successfully.")
    else:
        print("\nDeletion cancelled.")



if __name__ == "__main__":
    main()
