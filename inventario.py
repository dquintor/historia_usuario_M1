#Funcion para solicitar los datos requeridos con sus respectivas validaciones
def solicitar_datos():
    while True:
        try:
            nombre = str(input("Ingrese el nombre del producto:").strip()).capitalize()
            if not nombre:
                print("El nombre del producto no puede estar vacio")
                continue
            elif not all(c.isalpha() or c.isspace() for c in nombre):
                print("Error. El nombre del producto solo puede contener letras y y espacios")
                continue
            break
        except KeyboardInterrupt:
            print("Error. Valor Ingresado no valido")
    
    while True:
        try: 
            precio = float(input("Ingrese el precio del producto: "))
            if not precio:
                print("El precio no puede estar vacio")
                continue
            break
        except (ValueError,KeyboardInterrupt):
            print("Valor invalido. Ingrese un dato numerico.") 
             
    while True:
        try:
            cantidad = int(input("Ingrese la cantidad del producto:"))
            if not cantidad:
                print("El campo cantidad no puede estar vacio.")
            break
        except (ValueError,KeyboardInterrupt):
            print("Valor invalido. Ingrese un dato sin decimales.") 
    return nombre, cantidad, precio

#Funcion para el precio total del stock por producto 
def precio_stock(cantidad, precio):
    costo_total = (cantidad * precio)
    return costo_total

#Funcion para mostrar la información relacionada al producto de manera organizada
def mostrar_resultado(nombre, cantidad, precio,costo_total):
    print(f"\n---Resumen del registro---\nNombre del producto: {nombre}\nCantidad en Stock: {cantidad}\nPrecio unitario: {precio}\nValor total del stock: {costo_total}")
    
#En este bloque de codigo llamamos las funciones creadas, a las funciones que nos devuelven un valor les asignamos variables. Al final esas variables las usamos como parametros para imprimir la informacion del producto
nombre, cantidad, precio = solicitar_datos()
costo_total = precio_stock(cantidad,precio)
mostrar_resultado(nombre, cantidad, precio,costo_total)

'''Este programa de inventario permite registrar la información básica de un producto.
Primero, solicita al usuario el nombre del producto (texto), el precio unitario (que puede ser un número entero o decimal) y la cantidad disponible (número entero).
Con estos datos, el programa calcula automáticamente el valor total del inventario para ese producto, es decir, el precio total de todas las unidades disponibles.
Finalmente, muestra en pantalla un resumen con toda la información ingresada y el resultado del cálculo'''

