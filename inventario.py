''' WEEK 1 INVENTORY PROGRAM '''

# Function to request the required data with their respective validations
inventory = []

def collect_data():
    collecting_data = True
    while collecting_data:
        try:
            name = str(input("Please enter the product name: ").strip()).capitalize()
            if not name:
                print("Product name can’t be empty. Please enter it to continue")
                continue
            elif not all(c.isalpha() or c.isspace() for c in name):
                print("Error. The product name must contain only letters and spaces. Please try again.")
                continue
            collecting_data = False
        except KeyboardInterrupt:
            print("Error. The value entered is not valid. Please check and try again")
        
    while True:
        try: 
            price = float(input("Enter the product price: "))
            if not price:
                print("The price cannot be empty")
                continue
            break
        except (ValueError, KeyboardInterrupt):
            print("Invalid value. Please enter a numeric value.") 
             
    while True:
        try:
            quantity = int(input("Enter the product quantity: "))
            if not quantity:
                print("The quantity field cannot be empty.")
            break
        except (ValueError, KeyboardInterrupt):
            print("Invalid value. Please enter a non-decimal number.") 

    return name, quantity, price


# Function for the total stock price per product 
def stock_price(quantity, price):
    total_cost = (price * quantity)
    return total_cost


# Function to display product-related information in an organized way
def display_result(name, quantity, price, total_cost):
    product_info = (f"\nName: {name} | Unit Price: {price} | Stock Quantity: {quantity} | Total Stock Value: {total_cost}")
    return product_info
    

'''WEEK 1 DOCUMENTATION: This inventory program allows you to register the basic information of a product.
First, it asks the user for the product name (text), the unit price (which can be an integer or decimal number), and the available quantity (integer).
With this data, the program automatically calculates the total inventory value for that product, meaning the total price of all available units.
Finally, it displays a summary of all entered information and the result of the calculation on the screen.'''


'''WEEK 2'''
def validate_option(menu, message, menu_started=True, minimum=None, maximum=None):
    while menu_started:
        try:
            print(menu)
            option = int(input(message))
            if option in [1, 2, 3, 4]:
                return option
                menu_started = False
            else:
                print("Invalid option. Please select an option between 1 and 4.")
        except ValueError:
                print("Invalid input. Please enter a number between 1 and 4.")
                return option
    

def menu():
    menu_text = (
        "\n---- Options Menu ----\n"
        "1. Add Product\n"
        "2. Show Inventory\n"
        "3. Calculate Statistics\n"
        "4. Save inventory to CSV\n"
        "5. Load inventory from CSV\n"
        "6. Exit\n"
    )
    option = validate_option(menu_text, "Select an option (1-4): ", menu_started=True, minimum=1, maximum=4)
    return option


def main():
    print("Welcome to the Product Inventory Management System!")
    menu_started = True
    while menu_started:
        option = menu()
        if option == 1:
            name, quantity, price = collect_data()
            total_cost = stock_price(quantity, price)
            add_product(name, quantity, price, total_cost)
            continue
        elif option == 2:
            show_inventory()
            continue
        elif option == 3:
            total_value, total_quantity = calculate_statistics()
            show_statistics(total_value, total_quantity)
            continue
        elif option == 4:
            menu_started = False
            print("Exiting the menu. See you later!")
            

def add_product(name, quantity, price, total_cost):
    product = {
        'name': name,
        'quantity': quantity,
        'price': price,
        'total_cost': total_cost
    }
    inventory.append(product)
    print(f"\n{quantity} units of the product {name} added to the inventory.\n")
    

def show_inventory():
    print("\n--- Product Inventory ---\n")
    if not inventory:
        print("Inventory is empty.\nPlease add products to view the inventory.")
        print(inventory)
    else:
        for product in inventory: 
            print(f"\nProduct {inventory.index(product)+1}:{display_result(product['name'], product['quantity'], product['price'], product['total_cost'])}")
        
        

    
def calculate_statistics():
    total_inventory_value = sum(product['total_cost'] for product in inventory)
    total_products = sum(product['quantity'] for product in inventory)
    return total_inventory_value, total_products

def show_statistics(total_inventory_value, total_products):
    print("\n --- Inventory Statistics ---\n"
          f"Total Inventory Value: {total_inventory_value}\n"
          f"Total Number of Products Registered: {total_products}\n")

'''WEEK 2 DOCUMENTATION: This program has been enhanced with a menu that gives the user four options:
1. Add Product: Allows the user to input product details and adds them to the inventory.
2. Show Inventory: Displays all products currently in the inventory with their details.
3. Calculate Statistics: Computes and shows the total inventory value and the total number of products registered.
4. Exit: Closes the menu and ends the program.
The menu continues to display until the user chooses to exit, allowing multiple operations in one session.''' 

def export_to_csv():
    pass

def import_from_csv():
    
    pass 
main()
