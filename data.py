# files.py
import csv

DEFAULT_PATH = "inventory.csv"


# Save inventory to CSV file
def export_to_csv(inventory, path=DEFAULT_PATH, include_header=True):
    """
    Saves the inventory to a CSV file.
    Format: name,price,quantity
    """
    try:
        if not inventory:
            print("The inventory is empty. There is no data to save.")
            return

        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if include_header:
                # Header as specified
                writer.writerow(["name", "price", "quantity"])

            for product in inventory:
                writer.writerow(
                    [
                        product.get("name"),
                        product.get("price"),
                        product.get("quantity"),
                    ]
                )

        print(f"Inventory saved to: {path}")

    except PermissionError:
        print("The file could not be saved due to permission issues.")
    except Exception as e:
        print(f"An error occurred while saving the CSV: {e}")




# Load CSV file and merge or overwrite inventory
def import_from_csv(current_inventory, path=DEFAULT_PATH):
    """
    Loads products from a CSV file and replaces or merges with the current inventory.

    Rules:
    - Required header: name,price,quantity
    - Each row: exactly 3 columns
    - price -> float >= 0
    - quantity -> int >= 0
    - Invalid rows are skipped and counted
    """
    loaded_inventory = []
    invalid_rows = 0

    try:
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader, None)

            if header is None:
                print("The CSV file is empty.")
                return current_inventory

            expected_header = ["name", "price", "quantity"]
            normalized_header = [col.strip().lower() for col in header]

           
            if normalized_header != expected_header:
                print("Invalid header. Expected: name,price,quantity.")
                return current_inventory

            for row in reader:
                
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

                    loaded_inventory.append(
                        {
                            "name": name,
                            "price": price,
                            "quantity": quantity,
                        }
                    )

                except ValueError:
                    invalid_rows += 1

        if not loaded_inventory:
            print("No valid products were found in the file.")
            return current_inventory

       
        while True:
            choice = input(
                "Overwrite current inventory? (Y/N): "
            ).strip().upper()
            if choice in ("Y", "N"):
                break
            print("Invalid option. Please answer Y or N.")

        if choice == "Y":
            action = "overwrite"
            final_inventory = loaded_inventory
        else:
            action = "merge"
            final_inventory = current_inventory.copy()

            for new_product in loaded_inventory:
                existing = next(
                    (p for p in final_inventory if p["name"] == new_product["name"]),
                    None,
                )

                if existing:
                    
                    existing["quantity"] += new_product["quantity"]
                    if existing["price"] != new_product["price"]:
                        existing["price"] = new_product["price"]
                else:
                    final_inventory.append(new_product)

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



