import ejercicio4_agregar as agregar
import ejercicio4_mostrar as mostrar
import ejercicio4_eliminar as eliminar

def menu():
    opciones = {
        "1": agregar.agregar,
        "2": mostrar.mostrar,
        "3": mostrar.promedio,
        "4": eliminar.eliminar
    }
    while True:
        print("\n1.Agregar  2.Mostrar  3.Promedio  4.Eliminar  5.Salir")
        op = input("Opción: ")
        if op == "5":
            break
        if op in opciones:
            opciones[op]()
        else:
            print("Inválido")

if __name__ == "__main__":
    menu()