import json, random
from pathlib import Path

ARCHIVO_JUGADORES = "jugadores.json"

# -------------------------
# Funciones de menú y opciones
# -------------------------
def pedir_opcion(mensaje, opciones):
    print(mensaje)
    for i, op in enumerate(opciones, 1):
        print(f"{i}. {op}")
    eleccion = 0
    while eleccion not in range(1, len(opciones)+1):
        try:
            eleccion = int(input("Elige un número: "))
            if eleccion not in range(1, len(opciones)+1):
                print(f"Debes elegir un número entre 1 y {len(opciones)}")
        except:
            print(f"Debes escribir un número entre 1 y {len(opciones)}")
    return eleccion - 1

# -------------------------
# Jugadores
# -------------------------
def cargar_jugadores():
    if Path(ARCHIVO_JUGADORES).exists():
        with open(ARCHIVO_JUGADORES,"r") as f:
            jugadores=json.load(f)
        for j in jugadores.values():
            if "energia" not in j: j["energia"]=50
            if "vida" not in j: j["vida"]=100
            if "inventario" not in j: j["inventario"]={"pocion":1}
            if "ataques" not in j: j["ataques"]=[{"nombre":"Golpe básico","daño":(5,15),"costo":5}]
            if "equipamiento" not in j: j["equipamiento"]=[]
            if "decisiones" not in j: j["decisiones"]=[]
        return jugadores
    return {}

def guardar_jugadores(jugadores):
    with open(ARCHIVO_JUGADORES,"w") as f:
        json.dump(jugadores,f,indent=4)

def registrar_jugador(jugadores):
    nombre = input("Nombre del jugador: ")
    if nombre in jugadores:
        print("Jugador cargado.")
        return nombre
    clases = ["humano","nephilim","demonio","purgador oscuro"]
    clase = clases[pedir_opcion("Elige tu clase:", clases)]
    jugador = {
        "clase":clase,
        "nivel":1,
        "vida":100,
        "energia":50,
        "inventario":{"pocion":1},
        "ataques":[{"nombre":"Golpe básico","daño":(5,15),"costo":5}],
        "equipamiento":[],
        "decisiones":[]
    }
    jugadores[nombre]=jugador
    print(f"\n¡Tu aventura comienza! {nombre}, serás un {clase.capitalize()} con 100 vida y 50 energía.\n")
    guardar_jugadores(jugadores)
    return nombre

# -------------------------
# Enemigos y jefes
# -------------------------
def enemigo_random():
    posibles = [
        {"nombre":"Espectro menor","vida":30,"energia":30,"ataques":[{"nombre":"Garra","daño":(4,9),"costo":5}]},
        {"nombre":"Alma perdida","vida":25,"energia":25,"ataques":[{"nombre":"Sombra","daño":(3,8),"costo":4}]},
        {"nombre":"Demonio menor","vida":35,"energia":35,"ataques":[{"nombre":"Llama","daño":(6,12),"costo":6}]},
        {"nombre":"Guardia del purgatorio","vida":40,"energia":40,"ataques":[{"nombre":"Golpe de Purgatorio","daño":(5,10),"costo":5}]}
    ]
    return random.choice(posibles)

def jefe_final():
    return {"nombre":"El Equilibrio","vida":200,"energia":100,"ataques":[{"nombre":"Golpe Supremo","daño":(15,30),"costo":15}]}

# -------------------------
# Loot y habilidades
# -------------------------
def loot(jugador):
    items=["poción","espada","armadura"]
    encontrado=random.choice(items)
    jugador["inventario"][encontrado]=jugador["inventario"].get(encontrado,0)+1
    print(f"¡Encontraste {encontrado}!")

def desbloquear_habilidades(jugador):
    clase = jugador["clase"]
    nivel = jugador["nivel"]
    if nivel==2:
        if clase=="humano":
            jugador["ataques"].append({"nombre":"Ataque Fuerte","daño":(15,25),"costo":10})
            print("¡Desbloqueaste Ataque Fuerte!")
        elif clase=="demonio":
            jugador["ataques"].append({"nombre":"Llama Infernal","daño":(18,30),"costo":12})
            print("¡Desbloqueaste Llama Infernal!")
        elif clase=="purgador oscuro":
            jugador["ataques"].append({"nombre":"Purgación Oscura","daño":(17,28),"costo":12})
            print("¡Desbloqueaste Purgación Oscura!")
    elif nivel>=3 and clase=="nephilim":
        jugador["ataques"].append({"nombre":"Luz Purificadora","daño":(20,35),"costo":15})
        print("¡Desbloqueaste Luz Purificadora!")

# -------------------------
# Inventario y objetos
# -------------------------
def mostrar_inventario_combate(jugador):
    print("\nInventario:")
    lista_objetos = list(jugador["inventario"].keys())
    for i, item in enumerate(lista_objetos,1):
        print(f"{i}. {item} x{jugador['inventario'][item]}")
    print(f"{len(lista_objetos)+1}. Cancelar")

    try:
        eleccion = int(input("Elige un número: ")) - 1
    except:
        eleccion = -1

    if eleccion == len(lista_objetos) or eleccion<0 or eleccion>=len(lista_objetos):
        print("Cancelado.")
        return 0,0
    item = lista_objetos[eleccion]

    efecto_dano = 0
    reduccion_dano = 0
    if jugador["inventario"][item]>0:
        if item=="poción":
            jugador["vida"] += 20
            print(f"Usaste poción, vida actual: {jugador['vida']}")
        elif item=="espada":
            efecto_dano = 5
            print("Tu espada aumentará el daño de tu próximo ataque!")
        elif item=="armadura":
            reduccion_dano = 5
            print("Tu armadura reducirá daño recibido en el próximo ataque enemigo!")
        jugador["inventario"][item]-=1
    else:
        print("No tienes ese objeto.")
    return efecto_dano, reduccion_dano

# -------------------------
# Combate
# -------------------------
def combate(jugador, enemigo, jugadores):
    print(f"\n¡Te enfrentas a {enemigo['nombre']}! Vida: {enemigo['vida']} | Energía: {enemigo['energia']}")
    buff_dano = 0
    reduccion_dano = 0

    while enemigo["vida"]>0 and jugador["vida"]>0:
        print(f"\nTus ataques (Energía: {jugador['energia']}):")
        for i, atk in enumerate(jugador["ataques"],1):
            print(f"{i}. {atk['nombre']} (Costo: {atk['costo']})")
        print(f"{len(jugador['ataques'])+1}. Usar objeto")
        print(f"{len(jugador['ataques'])+2}. Salir y guardar")

        try:
            elec = int(input("Elige acción: "))-1
        except:
            elec = 0

        if elec==len(jugador['ataques']):
            efecto_d, reduccion = mostrar_inventario_combate(jugador)
            buff_dano += efecto_d
            reduccion_dano += reduccion
            guardar_jugadores(jugadores)
            continue
        elif elec==len(jugador['ataques'])+1:
            guardar_jugadores(jugadores)
            print("Juego guardado. Saliendo del combate...")
            exit()
        elif elec<0 or elec>=len(jugador['ataques']):
            elec=0

        ataque = jugador["ataques"][elec]
        if jugador["energia"]<ataque["costo"]:
            print("No tienes suficiente energía!")
            continue

        jugador["energia"]-=ataque["costo"]
        daño=random.randint(*ataque["daño"]) + buff_dano
        buff_dano=0
        enemigo["vida"]-=daño
        print(f"Usaste {ataque['nombre']} y causaste {daño}. Vida enemigo: {max(enemigo['vida'],0)}")

        if enemigo["vida"]<=0:
            print(f"¡Has vencido a {enemigo['nombre']}!")
            jugador["nivel"]+=1
            desbloquear_habilidades(jugador)
            loot(jugador)
            jugador["energia"]=50
            guardar_jugadores(jugadores)
            return

        atk_enem=random.choice(enemigo["ataques"])
        daño_enem=random.randint(*atk_enem["daño"])-reduccion_dano
        reduccion_dano=0
        daño_enem=max(0,daño_enem)
        jugador["vida"]-=daño_enem
        print(f"{enemigo['nombre']} usó {atk_enem['nombre']} y causó {daño_enem}. Vida actual: {max(jugador['vida'],0)}")

# -------------------------
# Escenas de exploración y diálogos
# -------------------------
def escena_exploracion(jugador,jugadores):
    print("\nExploras el entorno...")
    opciones = ["Investigar la aldea","Seguir el río","Subir la colina"]
    elec = pedir_opcion("Qué haces?", opciones)
    if elec==0:
        print("Encuentras enemigos mientras investigas...")
        combate(jugador, enemigo_random(), jugadores)
    elif elec==1:
        print("Encuentras a un anciano sabio que te da información y algún objeto.")
        loot(jugador)
        guardar_jugadores(jugadores)
    else:
        print("Subes la colina y encuentras un lugar seguro para descansar.")
        jugador["vida"]=min(100,jugador["vida"]+10)
        jugador["energia"]=50
        print(f"Vida y energía restauradas. Vida: {jugador['vida']} | Energía: {jugador['energia']}")
    guardar_jugadores(jugadores)

# -------------------------
# Historia lineal con jefe final
# -------------------------
def aventura_completa(jugador, jugadores, nombre):
    print("\n--- Inicia la historia ---")
    # Escena inicial
    atacante=""
    if jugador["clase"]=="humano" or jugador["clase"]=="nephilim":
        atacante="demonios"
    elif jugador["clase"]=="demonio":
        atacante="ángeles"
    else:
        atacante="purgadores"
    print(f"\nTu pueblo es atacado por {atacante}!")
    combate(jugador, enemigo_random(), jugadores)
    if jugador["vida"]<=0:
        print("\n¡Has muerto! Fin de la aventura."); return

    # Exploraciones con enemigos aleatorios y loot
    for _ in range(2):
        escena_exploracion(jugador,jugadores)
        if jugador["vida"]<=0:
            print("\n¡Has muerto! Fin de la aventura."); return

    # Jefe final
    print("\n¡Has llegado al jefe final!")
    combate(jugador, jefe_final(), jugadores)
    if jugador["vida"]<=0:
        print("\n¡Has muerto ante el jefe final! Fin de la aventura."); return

    print("\n¡Felicidades! Has completado la aventura.")
    jugador["energia"]=50
    guardar_jugadores(jugadores)

# -------------------------
# Menú principal
# -------------------------
def menu_principal():
    jugadores = cargar_jugadores()
    nombre = registrar_jugador(jugadores)
    jugador = jugadores[nombre]

    while True:
        opcion = pedir_opcion("\n--- Menú principal ---", ["Aventura","Inventario","Guardar y salir"])
        if opcion==0:
            aventura_completa(jugador,jugadores,nombre)
        elif opcion==1:
            print("\nInventario:")
            for k,v in jugador["inventario"].items():
                print(f"{k} x{v}")
        else:
            guardar_jugadores(jugadores)
            print("Juego guardado. ¡Hasta luego!")
            break

if __name__=="__main__":
    menu_principal()