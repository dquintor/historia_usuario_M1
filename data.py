# files.py
import csv

DEFAULT_PATH = "inventory.csv"


# Save CSV
def export_to_csv(inventory, path=DEFAULT_PATH, include_header=True):
    """Saves the inventory to a CSV file at the given path.
    If include_header is True, writes the header row.
    
    parameters:
    - inventory: list of product dicts
    - path: file path to save the CSV
    - include_header: whether to write the header row
    
    returns: None"""
    try:
        if not inventory:
            print("Inventory is empty. No data to save.")
            return

        with open(path, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)

            if include_header:
                # Header according to the requirements
                writer.writerow(['name', 'price', 'quantity'])

            for product in inventory:
                writer.writerow([
                    product.get('name'),
                    product.get('price'),
                    product.get('quantity')
                ])

        print(f"Inventory saved to: {path}")

    except PermissionError:
        print("Could not save file due to permission issues.")
    except Exception as e:
        print(f"An error occurred while saving the CSV: {e}")



#Load CSV with overwrite/merge option
def import_from_csv(current_inventory, path=DEFAULT_PATH):
    """
    Loads products from a CSV and either replaces or merges the current inventory.

    Rules:
    - Required header: name,price,quantity
    - Each row must have exactly 3 columns
    - price -> float >= 0
    - quantity -> int >= 0
    - Invalid rows are skipped and counted
    Parameters:
    - current_inventory: list of existing product dicts
    - path: file path to load the CSV from
    Returns:
    - new inventory list if successful, else returns current_inventory
    """
    loaded_inventory = []
    invalid_rows = 0

    try:
        with open(path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader, None)

            if header is None:
                print("The CSV file is empty.")
                return current_inventory

            expected_header = ['name', 'price', 'quantity']
            normalized_header = [col.strip().lower() for col in header]

            # Validate header
            if normalized_header != expected_header:
                print("Invalid header. Expected: name,price,quantity.")
                return current_inventory

            for row in reader:
                # Skip completely empty lines
                if not row or all(col.strip() == "" for col in row):
                    continue

                if len(row) != 3:
                    invalid_rows += 1
                    continue

                try:
                    name = row[0].strip()
                    price = float(row[1])
                    quantity = int(row[2])

                    if price < 0 or quantity < 0:
                        raise ValueError

                    # calculate total_cost for each loaded product
                    total_cost = price * quantity

                    loaded_inventory.append({
                        'name': name,
                        'price': price,
                        'quantity': quantity,
                        'total_cost': total_cost
                    })

                except ValueError:
                    invalid_rows += 1

        if not loaded_inventory:
            print("No valid products found in the CSV file.")
            return current_inventory

        # Ask the user if they want to overwrite or merge the inventory
        while True:
            choice = input("Overwrite current inventory? (Y/N): ").strip().upper()
            if choice in ('Y', 'N'):
                break
            print("Invalid option. Enter Y or N.")

        if choice == 'Y':
            action = "overwrite"
            final_inventory = loaded_inventory
        else:
            action = "merge"
            final_inventory = current_inventory.copy()

            for new_product in loaded_inventory:
                existing = next(
                    (p for p in final_inventory if p['name'] == new_product['name']),
                    None
                )

                if existing:
                    #  add quantity and update price if different
                    existing['quantity'] += new_product['quantity']
                    if existing['price'] != new_product['price']:
                        existing['price'] = new_product['price']
                else:
                    final_inventory.append(new_product)

        # Recalculate total_cost for *all* products in the final inventory
        for product in final_inventory:
            product['total_cost'] = product['price'] * product['quantity']

        print(f"Inventory loaded from: {path}")
        print(f"Products loaded: {len(loaded_inventory)}")
        print(f"Invalid rows skipped: {invalid_rows}")
        print(f"Action performed: {action}")

        return final_inventory

    except FileNotFoundError:
        print("The specified file was not found.")
    except UnicodeDecodeError:
        print("Encoding error. Make sure it is a valid CSV file.")
    except Exception as e:
        print(f"An unexpected error occurred while loading the file: {e}")

    return current_inventory


