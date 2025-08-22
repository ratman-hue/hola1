import sys
import random

def main():
    if len(sys.argv) != 2:
        print("Uso: python programa.py <cantidad>")
        return

    try:
        cantidad = int(sys.argv[1])
        if cantidad <= 0:
            print("La cantidad debe ser un número positivo.")
            return
    except ValueError:
        print("La cantidad debe ser un número entero.")
        return

    # Generar y mostrar números aleatorios entre 1 y 100
    numeros = [random.randint(1, 100) for _ in range(cantidad)]
    print("Números generados:", *numeros)

if __name__ == "__main__":
    main()
