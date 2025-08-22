import ejercicio4_mostrar as mostrar

def eliminar():
    id_est = input("ID: ").strip()
    if id_est not in mostrar.estudiantes:
        print("No existe")
        return
    del mostrar.estudiantes[id_est]
    print("Eliminado")