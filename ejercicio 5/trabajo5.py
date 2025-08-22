def leer_estudiantes():
    try:
        with open("estudiantes.txt", "r") as f:
            lineas = f.readlines()
        estudiantes = []
        for linea in lineas:
            try:
                nombre, calificacion = linea.strip().split(",")
                estudiantes.append((nombre, float(calificacion)))
            except ValueError:
                print(f"Formato inválido en la línea: {linea.strip()}")
        return estudiantes
    except FileNotFoundError:
        print("El archivo 'estudiantes.txt' no existe.")
        return []


def calcular_promedio(estudiantes):
    if not estudiantes:
        return 0
    total = sum([c for _, c in estudiantes])
    return total / len(estudiantes)


def generar_reporte(estudiantes, promedio):
    with open("reporte.txt", "w") as f:
        for nombre, calificacion in estudiantes:
            f.write(f"{nombre},{calificacion}\n")
        f.write(f"Promedio general: {promedio:.1f}\n")
    print("Reporte generado en 'reporte.txt'.")


def agregar_estudiante():
    nombre = input("Nombre del estudiante: ")
    calificacion = input("Calificación: ")
    try:
        calificacion = float(calificacion)
        with open("estudiantes.txt", "a") as f:
            f.write(f"{nombre},{calificacion}\n")
        print("Estudiante agregado.")
    except ValueError:
        print("Calificación inválida.")


def main():
    while True:
        print("\n--- Menú ---")
        print("1. Leer estudiantes y generar reporte")
        print("2. Agregar estudiante")
        print("3. Salir")
        opcion = input("Opción: ")

        if opcion == "1":
            estudiantes = leer_estudiantes()
            promedio = calcular_promedio(estudiantes)
            generar_reporte(estudiantes, promedio)
        elif opcion == "2":
            agregar_estudiante()
        elif opcion == "3":
            print("Adiós!")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()