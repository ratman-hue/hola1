estudiantes = {
    "A001": {"nombre": "Ana Torres", "edad": 20, "calificaciones": [9, 10, 7]},
    "A002": {"nombre": "Luis Pérez", "edad": 22, "calificaciones": [8, 9, 6]}
}

def agregar():
    id_est = input("ID: ").strip()
    if id_est in estudiantes:
        print("El ID ya existe"); return
    nombre = input("Nombre: ").strip()
    try:
        edad = int(input("Edad: "))
        calificaciones = list(map(float, input("Calificaciones: ").split()))
    except ValueError:
        print("Datos invalidos"); return
    estudiantes[id_est] = {"nombre": nombre, "edad": edad, "calificaciones": calificaciones}
    print("Alumno agregado")

def mostrar():
    if not estudiantes:
        print("Sin alumnos"); return
    for id_est, datos in estudiantes.items():
        prom = sum(datos["calificaciones"]) / len(datos["calificaciones"])
        print(f"{id_est} - {datos['nombre']} - Edad: {datos['edad']} - Promedio: {prom:.2f}")

def promedio():
    id_est = input("ID: ").strip()
    if id_est not in estudiantes:
        print("No existe el alumno"); return
    datos = estudiantes[id_est]
    prom = sum(datos["calificaciones"]) / len(datos["calificaciones"])
    print(f"{id_est} - {datos['nombre']} - Promedio: {prom:.2f}")

def eliminar():
    id_est = input("ID: ").strip()
    if id_est not in estudiantes:
        print("No existe el alumno"); return
    del estudiantes[id_est]
    print("Alumno eliminado")

def menu():
    opciones = {"1": agregar, "2": mostrar, "3": promedio, "4": eliminar}
    while True:
        print("\n1. Agregar")
        print("2. Mostrar")  
        print("3. Promedio")
        print("4. Eliminar")
        print("5. Salir")
        op = input("Seleccione una opción: ")
        if op == "5": break
        if op in opciones: opciones[op]()
        else: print("Opcion invalida")
menu()