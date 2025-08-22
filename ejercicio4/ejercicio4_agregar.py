import ejercicio4_mostrar as mostrar

def agregar():
    id_est = input("ID: ").strip()
    if id_est in mostrar.estudiantes:
        print("ID existente")
        return
    nombre = input("Nombre: ").strip()
    try:
        edad = int(input("Edad: "))
        calif = list(map(float, input("Calificaciones: ").split()))
    except ValueError:
        print("Datos inválidos")
        return
    mostrar.estudiantes[id_est] = {"nombre": nombre, "edad": edad, "calificaciones": calif}
    print("Agregado")