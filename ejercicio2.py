import numpy as np

def ingresar_matriz(nombre):
    f = int(input(f"Filas de {nombre}: "))
    c = int(input(f"Columnas de {nombre}: "))
    datos = []
    for i in range(f):
        fila = list(map(float, input(f"Fila {i+1} (separar números con espacio): ").split()))
        while len(fila) != c:
            print("La cantidad de números no coincide con las columnas")
            fila = list(map(float, input(f"Fila {i+1}: ").split()))
        datos.append(fila)
    return np.array(datos)

while True:
    print("\nCalculadora de Matrices")
    print("1. Suma")
    print("2. Resta")
    print("3. Multiplicación")
    print("4. Transposición")
    print("5. Salir")
    op = input("Seleccione opción: ")

    if op in ["1", "2", "3"]:
        A, B = ingresar_matriz("A"), ingresar_matriz("B")

        if op == "1":
            if A.shape == B.shape:
                print("\nResultado de la suma:")
                print(np.add(A, B))
            else:
                print("No se pueden sumar: ambas matrices deben tener el mismo número de filas y columnas")

        elif op == "2":
            if A.shape == B.shape:
                print("\nResultado de la resta:")
                print(np.subtract(A, B))
            else:
                print("No se pueden restar: ambas matrices deben tener el mismo número de filas y columnas")

        elif op == "3":
            if A.shape[1] == B.shape[0]:
                print("\nResultado de la multiplicación:")
                print(np.matmul(A, B))
            else:
                print("No se pueden multiplicar: el número de columnas de la primera matriz debe ser igual al número de filas de la segunda")

    elif op == "4":
        A = ingresar_matriz("A")
        print("\nTransposicion")
        print(np.transpose(A))

    elif op == "5":
        print("Saliendo del programa")
        break

    else:
        print("Opción no válida")