estudiantes = {
    "A001": {"nombre": "Ana Torres", "edad": 20, "calificaciones": [9, 8.5, 7.8]},
    "A002": {"nombre": "Luis Pérez", "edad": 22, "calificaciones": [8.8, 9.1, 7.9]}
}

def mostrar():
    if not estudiantes:
        print("Sin alumnos")
        return
    for id_est, d in estudiantes.items():
        prom = sum(d["calificaciones"]) / len(d["calificaciones"])
        print(f"{id_est} - {d['nombre']} - Edad: {d['edad']} - Promedio: {prom:.2f}")

def promedio():
    id_est = input("ID: ").strip()
    if id_est not in estudiantes:
        print("No existe")
        return
    d = estudiantes[id_est]
    prom = sum(d["calificaciones"]) / len(d["calificaciones"])
    print(f"{id_est} - {d['nombre']} - Promedio: {prom:.2f}")