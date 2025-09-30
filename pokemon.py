import os
import time
import random
import json

# --- Configuración y Constantes ---

# Configuración de limpieza de pantalla
def cls():
    """Limpia la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

# EMOJIS para el mapa
PLAYER_ICON = '👤'
GRASS_ICON = '🌿'
MAP_WIDTH = 20
MAP_HEIGHT = 10

# Tabla de Efectividades (Solo Agua, Fuego, Planta, Normal)
EFFECTIVENESS_TABLE = {
    'Fuego': {'Planta': 2.0, 'Agua': 0.5, 'Fuego': 1.0, 'Normal': 1.0},
    'Agua': {'Fuego': 2.0, 'Planta': 0.5, 'Agua': 1.0, 'Normal': 1.0},
    'Planta': {'Agua': 2.0, 'Fuego': 0.5, 'Planta': 1.0, 'Normal': 1.0},
    'Normal': {'Fuego': 1.0, 'Agua': 1.0, 'Planta': 1.0, 'Normal': 1.0},
}

# Definición de movimientos base
MOVEMENT_BASE_STATS = {
    'Placaje': {'poder': 40, 'tipo': 'Normal', 'variante': 'Ataque básico'},
    'Ascuas': {'poder': 40, 'tipo': 'Fuego', 'variante': 'Ataque básico'},
    'Pistola Agua': {'poder': 40, 'tipo': 'Agua', 'variante': 'Ataque básico'},
    'Latigo Cepa': {'poder': 45, 'tipo': 'Planta', 'variante': 'Ataque básico'},
    'Ataque Rapido': {'poder': 40, 'tipo': 'Normal', 'variante': 'Ataque básico'},
    'Furia Dragon': {'poder': 60, 'tipo': 'Normal', 'variante': 'Ataque doble'},
    'Burbuja': {'poder': 20, 'tipo': 'Agua', 'variante': 'Ataque doble'},
    'Viento Plata': {'poder': 60, 'tipo': 'Normal', 'variante': 'Ataque básico'},
    'Bostezo': {'poder': 0, 'tipo': 'Normal', 'variante': 'Ataque pierde turno'},
    'Salpicadura': {'poder': 0, 'tipo': 'Normal', 'variante': 'Sin efecto'},
}

# --- 1. Clases Principales ---

class Movimiento:
    """Clase base para representar un movimiento de ataque."""
    def __init__(self, nombre, poder, tipo):
        self.nombre = nombre
        self.poder = poder
        self.tipo = tipo
        stats = MOVEMENT_BASE_STATS.get(nombre, {})
        self.variante = stats.get('variante', 'Ataque básico')
        if nombre not in MOVEMENT_BASE_STATS:
            MOVEMENT_BASE_STATS[nombre] = {'poder': poder, 'tipo': tipo, 'variante': self.variante}

    def atacar(self):
        """Simula el efecto de la variante de ataque y devuelve el multiplicador de daño."""
        
        if self.variante == 'Ataque doble':
            print(f"[{self.nombre}] - ¡Doble impacto!")
            return 2 
        elif self.variante == 'Sin efecto':
            print(f"[{self.nombre}] - ¡No tuvo efecto!")
            return 0
        elif self.variante == 'Ataque pierde turno':
            print(f"[{self.nombre}] - ¡Necesita recargar! (Efecto no implementado completamente)")
            return 1
        else: # Ataque básico
            return 1

    def __str__(self):
        return f"{self.nombre} ({self.tipo} | Pwr: {self.poder} | Var: {self.variante})"

class Pokemon:
    """Clase Padre para todos los Pokémon."""
    def __init__(self, arte_ascii, nombre, tipo, ataque, defensa, hp_max, habilidad, movimientos_nombres):
        self.arte_ascii = arte_ascii
        self.nombre = nombre
        self.tipo = tipo
        self.ataque = ataque
        self.defensa = defensa
        self.hp_max = hp_max
        self.hp_actual = hp_max
        self.habilidad_nombre = habilidad
        
        self.movimientos = []
        for nombre in movimientos_nombres:
            stats = MOVEMENT_BASE_STATS.get(nombre)
            if stats:
                self.movimientos.append(Movimiento(nombre, stats['poder'], stats['tipo']))

    def atacar(self, movimiento_obj, objetivo, tabla_tipos):
        """
        Calcula el daño final considerando el poder, stats, STAB y efectividad de tipo.
        (Método: Atacar (Tomar en cuenta efectividad de tipo y STAB))
        """
        
        variante_multi = movimiento_obj.atacar()
        if variante_multi == 0:
            return 0 

        damage_pre_mod = ((((self.ataque * movimiento_obj.poder) / objetivo.defensa) / 10) + 1)
        stab = 1.5 if self.tipo == movimiento_obj.tipo else 1.0
        efectividad = tabla_tipos.get(movimiento_obj.tipo, {}).get(objetivo.tipo, 1.0)
        final_damage = int(damage_pre_mod * stab * efectividad * variante_multi)
        
        objetivo.hp_actual = max(0, objetivo.hp_actual - final_damage)
        
        if efectividad > 1.0:
            print("¡Es SÚPER EFICAZ!")
        elif efectividad < 1.0 and efectividad > 0:
            print("No es muy eficaz...")
        elif efectividad == 0:
            print("¡No tiene efecto!")

        return final_damage

    def habilidad(self):
        """Muestra la habilidad del Pokémon."""
        return self.habilidad_nombre

    def esta_derrotado(self):
        """(Un pokemon es derrotado?)"""
        return self.hp_actual <= 0
    
    def to_dict(self):
        """Serializa el objeto para guardar."""
        return {
            'clase': self.__class__.__name__,
            'arte_ascii': self.arte_ascii,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'ataque': self.ataque,
            'defensa': self.defensa,
            'hp_max': self.hp_max,
            'hp_actual': self.hp_actual,
            'habilidad_nombre': self.habilidad_nombre,
            'movimientos_nombres': [m.nombre for m in self.movimientos]
        }
    
    @staticmethod
    def from_dict(data):
        """Reconstruye el objeto desde un diccionario."""
        cls_name = data['clase']
        
        if cls_name in globals() and issubclass(globals()[cls_name], Pokemon):
            cls_obj = globals()[cls_name]
            instance = cls_obj.__new__(cls_obj)
            
            instance.arte_ascii = data.get('arte_ascii', '❓') 
            instance.nombre = data['nombre']
            instance.tipo = data['tipo']
            instance.ataque = data['ataque']
            instance.defensa = data['defensa']
            instance.hp_max = data['hp_max']
            instance.hp_actual = data['hp_actual']
            instance.habilidad_nombre = data['habilidad_nombre']
            
            instance.movimientos = []
            for nombre in data['movimientos_nombres']:
                 stats = MOVEMENT_BASE_STATS.get(nombre)
                 if stats:
                    instance.movimientos.append(Movimiento(nombre, stats['poder'], stats['tipo']))
                 else:
                    instance.movimientos.append(Movimiento(nombre, 40, 'Normal'))
            return instance
        return None

    def __str__(self):
        return f"{self.nombre} ({self.tipo}) - HP: {self.hp_actual}/{self.hp_max}"

# --- 1. Clases Hijas de Pokemon (10 Pokémon) ---
# *Se usan las mismas 10 clases para la funcionalidad (Charmander, Squirtle, Bulbasaur, etc.)*

class Charmander(Pokemon):
    def __init__(self, nivel=5):
        hp = random.randint(39, 45)
        super().__init__(
            arte_ascii='🔥', nombre='Charmander', tipo='Fuego',
            ataque=random.randint(52, 60), defensa=random.randint(43, 50),
            hp_max=hp, habilidad='Mar Llamas', movimientos_nombres=['Ascuas', 'Placaje']
        )
class Squirtle(Pokemon):
    def __init__(self, nivel=5):
        hp = random.randint(44, 50)
        super().__init__(
            arte_ascii='💧', nombre='Squirtle', tipo='Agua',
            ataque=random.randint(48, 55), defensa=random.randint(65, 72),
            hp_max=hp, habilidad='Torrente', movimientos_nombres=['Pistola Agua', 'Placaje']
        )
class Bulbasaur(Pokemon):
    def __init__(self, nivel=5):
        hp = random.randint(45, 49)
        super().__init__(
            arte_ascii='🌱', nombre='Bulbasaur', tipo='Planta',
            ataque=random.randint(49, 55), defensa=random.randint(49, 55),
            hp_max=hp, habilidad='Espesura', movimientos_nombres=['Latigo Cepa', 'Placaje']
        )
class Pidgey(Pokemon):
    def __init__(self, nivel=5):
        hp = random.randint(40, 45)
        super().__init__(
            arte_ascii='🦅', nombre='Pidgey', tipo='Normal',
            ataque=random.randint(45, 50), defensa=random.randint(40, 45),
            hp_max=hp, habilidad='Tumbos', movimientos_nombres=['Ataque Rapido', 'Placaje']
        )
class Rattata(Pokemon):
    def __init__(self, nivel=5):
        hp = random.randint(30, 35)
        super().__init__(
            arte_ascii='🐀', nombre='Rattata', tipo='Normal',
            ataque=random.randint(56, 60), defensa=random.randint(35, 40),
            hp_max=hp, habilidad='Fuga', movimientos_nombres=['Furia Dragon', 'Placaje']
        )
class Growlithe(Pokemon):
    def __init__(self, nivel=5):
        hp = random.randint(55, 60)
        super().__init__(
            arte_ascii='🐕', nombre='Growlithe', tipo='Fuego',
            ataque=random.randint(70, 75), defensa=random.randint(45, 50),
            hp_max=hp, habilidad='Intimidación', movimientos_nombres=['Ascuas', 'Ataque Rapido']
        )
class Poliwag(Pokemon):
    def __init__(self, nivel=5):
        hp = random.randint(40, 45)
        super().__init__(
            arte_ascii='🐸', nombre='Poliwag', tipo='Agua',
            ataque=random.randint(50, 55), defensa=random.randint(40, 45),
            hp_max=hp, habilidad='Humedad', movimientos_nombres=['Pistola Agua', 'Burbuja']
        )
class Oddish(Pokemon):
    def __init__(self, nivel=5):
        hp = random.randint(45, 50)
        super().__init__(
            arte_ascii='🍄', nombre='Oddish', tipo='Planta',
            ataque=random.randint(50, 55), defensa=random.randint(50, 55),
            hp_max=hp, habilidad='Clorofila', movimientos_nombres=['Latigo Cepa', 'Burbuja']
        )
class Ponyta(Pokemon):
    def __init__(self, nivel=5):
        hp = random.randint(50, 55)
        super().__init__(
            arte_ascii='🐎', nombre='Ponyta', tipo='Fuego',
            ataque=random.randint(75, 80), defensa=random.randint(45, 50),
            hp_max=hp, habilidad='Fuga', movimientos_nombres=['Ascuas', 'Viento Plata']
        )
class Goldeen(Pokemon):
    def __init__(self, nivel=5):
        hp = random.randint(45, 50)
        super().__init__(
            arte_ascii='🐟', nombre='Goldeen', tipo='Agua',
            ataque=random.randint(67, 72), defensa=random.randint(60, 65),
            hp_max=hp, habilidad='Nado Rápido', movimientos_nombres=['Pistola Agua', 'Viento Plata']
        )

WILD_POKEMON_CLASSES = [Pidgey, Rattata, Growlithe, Poliwag, Oddish, Ponyta, Goldeen]


# --- 2. Clase de Control del Juego ---

class Juego:
    """Clase principal que maneja la lógica y el flujo del juego."""
    def __init__(self):
        self.partida_actual = self.default_partida_data()
        self.mapa = self.generar_mapa()
        self.efectividades = EFFECTIVENESS_TABLE

    def default_partida_data(self):
        """Datos por defecto para una nueva partida."""
        return {
            'nombre_jugador': '',
            'equipo': [],
            'posicion_mapa': (int(MAP_WIDTH/2), int(MAP_HEIGHT/2)),
            'historial_combates': [], # Aunque no se muestra, se mantiene para guardar el estado del juego
            'pokemones_disponibles': ['Charmander', 'Squirtle', 'Bulbasaur']
        }

    # --- Persistencia (Guardar/Cargar) ---
    def guardar_partida(self):
        """Guarda la partida."""
        if not self.partida_actual['nombre_jugador']: return
        data_to_save = self.partida_actual.copy()
        data_to_save['equipo'] = [p.to_dict() for p in self.partida_actual['equipo']]
        try:
            with open(f"{self.partida_actual['nombre_jugador']}_partida.txt", 'w') as f:
                json.dump(data_to_save, f, indent=4)
        except Exception:
            pass # No mostrar errores en el juego para mantener el foco en la jugabilidad

    def cargar_partida(self, nombre_partida=''):
        """Carga la partida."""
        cls()
        if not nombre_partida:
             nombre_partida = input("Ingrese el nombre de la partida a cargar (Jugador): ").strip()
             if not nombre_partida: return False

        filename = f"{nombre_partida}_partida.txt"
        
        try:
            with open(filename, 'r') as f:
                data_loaded = json.load(f)
            
            equipo_cargado = [Pokemon.from_dict(poke_data) for poke_data in data_loaded['equipo'] if Pokemon.from_dict(poke_data)]
            
            self.partida_actual = data_loaded
            self.partida_actual['equipo'] = equipo_cargado
            
            print(f"Partida de {nombre_partida} cargada con éxito.")
            time.sleep(1)
            return True

        except FileNotFoundError:
            print(f"No se encontró la partida con el nombre '{nombre_partida}'.")
            time.sleep(1.5)
            return False
        except Exception as e:
            print(f"Error al cargar la partida: {e}")
            time.sleep(1.5)
            return False

    def borrar_partida(self):
        """Borra la partida."""
        cls()
        nombre = input("Ingrese el nombre de la partida a borrar: ").strip()
        if not nombre: return
        
        filename = f"{nombre}_partida.txt"
        
        if os.path.exists(filename):
            confirm = input(f"¿Seguro que desea borrar la partida de '{nombre}'? (S/N): ").upper()
            if confirm == 'S':
                os.remove(filename)
                print(f"Partida de {nombre} borrada.")
                time.sleep(1)
            else:
                print("Borrado cancelado.")
                time.sleep(1)
        else:
            print(f"No se encontró la partida con el nombre '{nombre}'.")
            time.sleep(1)

    # --- 2. Menús del Juego ---
    def menu_principal(self):
        """(MENÚ PRINCIPAL)"""
        while True:
            cls()
            print("=== MENÚ PRINCIPAL ===")
            print("1. Crear partida")
            print("2. Continuar partida")
            print("3. Borrar partida")
            print("4. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.menu_creacion()
                if self.partida_actual['nombre_jugador']:
                    self.mostrar_mapa()
            elif opcion == '2':
                if self.cargar_partida():
                    self.mostrar_mapa()
            elif opcion == '3':
                self.borrar_partida()
            elif opcion == '4':
                cls()
                print("¡Gracias por jugar!")
                input("Presione Enter para salir...") # Pausa para mantener la terminal abierta
                break
            else:
                print("Opción no válida. Intente de nuevo.")
                time.sleep(1.5)

    def menu_creacion(self):
        """(MENU DE CREACION)"""
        cls()
        nombre = input("Ingrese el nombre del jugador: ").strip()
        if not nombre: return
        
        self.partida_actual = self.default_partida_data()
        self.partida_actual['nombre_jugador'] = nombre
        
        print("\n--- ELIGE TU POKÉMON INICIAL ---")
        pokemones = self.partida_actual['pokemones_disponibles']
        
        for i, p_name in enumerate(pokemones):
            poke_class = globals().get(p_name) 
            if poke_class:
                temp_poke = poke_class() 
                print(f"{i+1}. {p_name} {temp_poke.arte_ascii}")
            
        while True:
            eleccion = input("Seleccione el número de su Pokémon inicial: ")
            try:
                index = int(eleccion) - 1
                if 0 <= index < len(pokemones):
                    poke_name = pokemones[index]
                    inicial = eval(f"{poke_name}()") 
                    self.partida_actual['equipo'].append(inicial)
                    print(f"\n¡{nombre} ha elegido a {inicial.nombre}! ¡A la aventura!")
                    time.sleep(2)
                    self.guardar_partida()
                    break
                else:
                    print("Número fuera de rango.")
            except ValueError:
                print("Entrada no válida.")

    def menu_estados(self, pokemon_target=None):
        """(MENÚ DE ESTADOS) - Muestra Arte ASCII, Nombre, HP, Habilidad, Tipo."""
        cls()
        if not self.partida_actual['equipo']:
            print("El equipo está vacío.")
            time.sleep(1)
            return
            
        print("=== MENÚ DE ESTADOS ===")
        
        if not pokemon_target:
            pokemon_target = self.partida_actual['equipo'][0] 
            
        p = pokemon_target
        print(f"\nArte ASCII: {p.arte_ascii}")
        print(f"Nombre: {p.nombre}")
        print(f"Tipo: {p.tipo}")
        print(f"HP Actual: {p.hp_actual}/{p.hp_max}")
        print(f"Ataque: {p.ataque} | Defensa: {p.defensa}")
        print(f"Habilidad: {p.habilidad_nombre}")
        print("Movimientos:")
        for mov in p.movimientos:
            print(f"  - {mov}")
        
        input("\nPresione Enter para continuar...")
        cls()
        
    # --- 3. Mapa y Exploración ---

    def generar_mapa(self):
        """Inicializa el mapa con hierba."""
        mapa = [[GRASS_ICON for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        return mapa

    def dibujar_mapa(self):
        """(MOSTRAR MAPA CUADRADO) - Renderiza el mapa y la posición del jugador."""
        cls()
        x, y = self.partida_actual['posicion_mapa']
        
        display_map = [row[:] for row in self.mapa]
            
        display_map[y][x] = PLAYER_ICON
        
        print("╔" + "═" * (MAP_WIDTH * 2 + 1) + "╗")
        for row in display_map:
            print("║ " + " ".join(row) + " ║")
        print("╚" + "═" * (MAP_WIDTH * 2 + 1) + "╝")
        
        print("\n|WASD-Movimiento | M - Menu | V-Volver") # Comandos estrictos del diagrama

    def gestionar_movimiento(self, tecla):
        """(Movimientos del jugador) - Mueve al jugador y gestiona eventos."""
        x, y = self.partida_actual['posicion_mapa']
        new_x, new_y = x, y
        
        if tecla == 'w' and y > 0: new_y -= 1
        elif tecla == 's' and y < MAP_HEIGHT - 1: new_y += 1
        elif tecla == 'a' and x > 0: new_x -= 1
        elif tecla == 'd' and x < MAP_WIDTH - 1: new_x += 1
        elif tecla == 'm': self.menu_estados()
        elif tecla == 'v': 
            self.guardar_partida()
            return 'VOLVER'
        else:
            return 

        # Si el movimiento es válido, actualizar posición
        if (new_x, new_y) != (x, y):
            self.partida_actual['posicion_mapa'] = (new_x, new_y)
            
            # Chequeo de Eventos (Ocurre Combate Aleatorio?)
            if random.random() < 0.05: 
                print("\n¡Un Pokémon salvaje apareció!")
                time.sleep(1)
                self.iniciar_combate() 
                return

    def mostrar_mapa(self):
        """Bucle principal de exploración del mapa."""
        while True:
            self.dibujar_mapa()
            comando = input("> ").lower().strip()
            
            resultado = self.gestionar_movimiento(comando)
            
            if resultado == 'VOLVER':
                break
            
            if comando not in ['w', 'a', 's', 'd', 'm', 'v']:
                print("Comando no reconocido. Use WASD, M o V.")
                time.sleep(0.5)


    # --- 4. Sistema de Combate ---

    def generar_pokemon_rival(self):
        """Genera un Pokémon rival aleatorio."""
        rival_class = random.choice(WILD_POKEMON_CLASSES)
        rival = rival_class()
        return rival

    def iniciar_combate(self):
        """Inicia y gestiona el combate."""
        
        if not self.partida_actual['equipo'] or self.partida_actual['equipo'][0].esta_derrotado():
            print("Tu Pokémon principal está debilitado. Debes curarlo primero.")
            time.sleep(2)
            return

        jugador_pokemon = self.partida_actual['equipo'][0] 
        rival_pokemon = self.generar_pokemon_rival()
        
        print(f"--- ¡COMBATE INICIADO! ---")
        print(f"¡{jugador_pokemon.nombre} VS. {rival_pokemon.nombre} salvaje!")
        time.sleep(1.5)

        combate_activo = True
        
        while combate_activo:
            cls()
            print(f"== RIVAL: {rival_pokemon.nombre} ==")
            print(f"HP: {rival_pokemon.hp_actual}/{rival_pokemon.hp_max}")
            print("-" * 20)
            print(f"== TÚ: {jugador_pokemon.nombre} ==")
            print(f"HP: {jugador_pokemon.hp_actual}/{jugador_pokemon.hp_max}")
            print("-" * 20)
            
            # (MENÚ DE COMBATE)
            print("1. Luchar | 2. Estado | 3. Huir")
            opcion = input("Seleccione una acción: ")

            if opcion == '1': # Luchar -> Lista de Movimientos -> Luchar
                self.turno_jugador(jugador_pokemon, rival_pokemon)
            elif opcion == '2': # Estado -> MENÚ DE ESTADOS
                self.menu_estados(jugador_pokemon)
                continue 
            elif opcion == '3': # Huir
                if self.intentar_huir():
                    print("¡Has huido con éxito!")
                    combate_activo = False
                    break
                else:
                    print("¡No pudiste huir!")
                    time.sleep(1)
            else:
                print("Opción no válida.")
                time.sleep(1)
                continue

            # Chequeo de fin de combate después del turno del jugador (Un pokemon es derrotado?)
            if rival_pokemon.esta_derrotado():
                print(f"¡{rival_pokemon.nombre} ha sido derrotado!")
                combate_activo = False
                break
            
            # Turno del Rival
            if combate_activo:
                self.turno_rival(jugador_pokemon, rival_pokemon)
                
                # Chequeo del jugador (Un pokemon es derrotado?)
                if jugador_pokemon.esta_derrotado():
                    print(f"¡{jugador_pokemon.nombre} no puede continuar!")
                    print("Has sido derrotado.")
                    combate_activo = False
                    break
        
        self.guardar_partida()
        print("\nEl combate ha terminado.")
        input("Presione Enter para volver al mapa...")


    def turno_jugador(self, p_jugador, p_rival):
        """(Lista de Movimientos a utilizar) -> Luchar"""
        while True:
            cls()
            print(f"--- MOVIMIENTOS DE {p_jugador.nombre} ---")
            for i, mov in enumerate(p_jugador.movimientos):
                print(f"{i+1}. {mov}")
            
            eleccion = input("Seleccione el número del movimiento: ")
            
            try:
                index = int(eleccion) - 1
                if 0 <= index < len(p_jugador.movimientos):
                    movimiento_elegido = p_jugador.movimientos[index]
                    
                    cls()
                    print(f"¡{p_jugador.nombre} usó {movimiento_elegido.nombre}!")
                    time.sleep(1)
                    
                    damage = p_jugador.atacar(movimiento_elegido, p_rival, self.efectividades)
                    
                    print(f"{p_rival.nombre} recibió {damage} de daño.")
                    time.sleep(1.5)
                    break
                else:
                    print("Selección no válida.")
            except ValueError:
                print("Entrada no válida.")

    def turno_rival(self, p_jugador, p_rival):
        """Gestión del ataque del rival (sólo ataque)."""
        
        movimiento_rival = random.choice(p_rival.movimientos)
        
        cls()
        print(f"--- TURNO DE {p_rival.nombre} ---")
        print(f"¡{p_rival.nombre} usó {movimiento_rival.nombre}!")
        time.sleep(1)
        
        p_rival.atacar(movimiento_rival, p_jugador, self.efectividades)
        
        print(f"{p_jugador.nombre} HP: {p_jugador.hp_actual}/{p_jugador.hp_max}")
        time.sleep(1.5)

    def intentar_huir(self):
        """(Huir) - Lógica simple para huir (50% de probabilidad)."""
        print("Intentando huir...")
        time.sleep(1)
        return random.choice([True, False])


# --- 7. Inicialización del Juego (INICIO DEL JUEGO) ---

if __name__ == "__main__":
    juego = Juego()
    juego.menu_principal()