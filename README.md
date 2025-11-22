# Inventory Management System (Python)

A modular and fully validated inventory management system built across three development stages (M1S1, M1S2, M1S3).  
The final system supports product registration, menu-driven CRUD operations, inventory statistics, and CSV persistence with robust validation and error handling.

---

# Project Structure

  historia_usuario_M1/
  │── app.py # Main application and user menu
  │── models.py # Product builder (factory)
  │── utils.py # Validations, recalculations, search utilities
  │── data.py # CSV import/export (persistence)
  │── inventory.csv # Default CSV file (optional)


## Features

### CRUD Operations
- Add product
- Show inventory
- Search product
- Update product
- Delete product

### Inventory Statistics
- Total units
- Total inventory value
- Most expensive product
- Product with highest stock

### Validated Input
- Product name normalization
- Non-negative numeric price
- Integer quantity greater than zero

### CSV Persistence
- Export to CSV
- Import with validation
- Skip invalid rows
- Error handling for missing or corrupted files

### Modular Design
Clean separation across multiple modules.

## Module Documentation

### app.py (Main Application)
Contains:
- Global `inventory` list
- Menu loop (`run()`)
- User input collector (`collect_data()`)

Menu options (1–9):
1. Add product  
2. Show inventory  
3. Search product  
4. Update product  
5. Delete product  
6. Show statistics  
7. Export CSV  
8. Import CSV  
9. Exit  

---

### models.py
`build_product(name, quantity, price)`  
Creates a standardized product dictionary:

```python
{
  "name": name,
  "quantity": quantity,
  "price": price,
  "total_cost": price * quantity
} ```

### utils.py

Contains:

- Input validation functions
- Product search functionality
- Total cost recalculation
- Utility functions for inventory operations

Main functions:

- `validate_product_name()`
- `validate_price()`
- `validate_quantity()`
- `get_product_by_name()`
- `recalc_total_cost()`
- `recalc_total_cost_for_inventory()`
- `print_product()`
- `ensure_inventory_not_empty()`

---

### data.py

Handles CSV persistence for saving and loading the inventory.

Functions:

- `export_to_csv(inventory, path)`
- `import_from_csv(path)`

Features:

- Validates CSV header format
- Ensures each row has three valid fields
- Converts data types to proper formats
- Skips invalid rows and counts omissions
- Handles common file errors (missing files, decoding issues, malformed data)
- Returns a list of valid product dictionaries

---

## Inventory Statistics

The system calculates the following metrics:

- Total units: sum of all product quantities  
- Total inventory value: price × quantity for each product, summed across the inventory  
- Most expensive product by unit price  
- Product with the highest stock  

All results are displayed clearly in console output.

---

## Running the Program

Run the program from the project directory using:

```bash
python app.py
