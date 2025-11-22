# files.py
import csv

DEFAULT_PATH = "inventory.csv"


# ====== TASK 4: Guardar CSV ======
def export_to_csv(inventory, path=DEFAULT_PATH, include_header=True):
    """
    Guarda el inventario en un archivo CSV.
    Formato: nombre,precio,cantidad
    """
    try:
        if not inventory:
            print("El inventario está vacío. No hay datos para guardar.")
            return

        with open(path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            if include_header:
                # Encabezado según el enunciado
                writer.writerow(['nombre', 'precio', 'cantidad'])

            for product in inventory:
                writer.writerow([
                    product.get('name'),
                    product.get('price'),
                    product.get('quantity')
                ])

        print(f"Inventario guardado en: {path}")

    except PermissionError:
        print("No se pudo guardar el archivo por problemas de permisos.")
    except Exception as e:
        print(f"Ocurrió un error al guardar el CSV: {e}")


# (Opcional) alias con el nombre del enunciado
def guardar_csv(inventario, ruta=DEFAULT_PATH, incluir_header=True):
    export_to_csv(inventario, ruta, incluir_header)


# ====== TASK 5: Cargar CSV ======
def import_from_csv(current_inventory, path=DEFAULT_PATH):
    """
    Carga productos desde un CSV y reemplaza o fusiona el inventario actual.

    Reglas:
    - Encabezado obligatorio: nombre,precio,cantidad
    - Cada fila: 3 columnas
    - precio -> float >= 0
    - cantidad -> int >= 0
    - Filas inválidas se omiten y se cuentan
    """
    loaded_inventory = []
    invalid_rows = 0

    try:
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader, None)

            if header is None:
                print("El archivo CSV está vacío.")
                return current_inventory

            expected_header = ['nombre', 'precio', 'cantidad']
            normalized_header = [col.strip().lower() for col in header]

            # Validar encabezado
            if normalized_header != expected_header:
                print("Encabezado inválido. Se esperaba: nombre,precio,cantidad.")
                return current_inventory

            for row in reader:
                # Saltar líneas totalmente vacías
                if not row or all(col.strip() == "" for col in row):
                    continue

                if len(row) != 3:
                    invalid_rows += 1
                    continue

                try:
                    nombre = row[0].strip()
                    precio = float(row[1])
                    cantidad = int(row[2])

                    if precio < 0 or cantidad < 0:
                        raise ValueError

                    loaded_inventory.append({
                        'name': nombre,
                        'price': precio,
                        'quantity': cantidad
                    })

                except ValueError:
                    invalid_rows += 1

        if not loaded_inventory:
            print("No se encontraron productos válidos en el archivo.")
            return current_inventory

        # Preguntar al usuario si sobrescribe o fusiona
        while True:
            choice = input("¿Sobrescribir inventario actual? (S/N): ").strip().upper()
            if choice in ('S', 'N'):
                break
            print("Opción inválida. Responde S o N.")

        if choice == 'S':
            action = "reemplazo"
            final_inventory = loaded_inventory
        else:
            action = "fusión"
            final_inventory = current_inventory.copy()

            for new_product in loaded_inventory:
                existing = next(
                    (p for p in final_inventory if p['name'] == new_product['name']),
                    None
                )

                if existing:
                    # Política: sumar cantidad y actualizar precio al nuevo si difiere
                    existing['quantity'] += new_product['quantity']
                    if existing['price'] != new_product['price']:
                        existing['price'] = new_product['price']
                else:
                    final_inventory.append(new_product)

        print(f"Inventario cargado desde: {path}")
        print(f"Productos cargados: {len(loaded_inventory)}")
        print(f"Filas inválidas omitidas: {invalid_rows}")
        print(f"Acción realizada: {action}")

        return final_inventory

    except FileNotFoundError:
        print("El archivo especificado no fue encontrado.")
    except UnicodeDecodeError:
        print("Error de codificación. Asegúrate de que sea un archivo CSV válido.")
    except Exception as e:
        print(f"Ocurrió un error inesperado al cargar el archivo: {e}")

    return current_inventory


# (Opcional) alias con el nombre del enunciado
def cargar_csv(ruta=DEFAULT_PATH, inventario_actual=None):
    if inventario_actual is None:
        inventario_actual = []
    return import_from_csv(inventario_actual, ruta)
