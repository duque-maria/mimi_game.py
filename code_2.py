import pygame
import sys
import random

# Inicializar Pygame
pygame.init()
ANCHO, ALTO = 400, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Salva a Mimi")
reloj = pygame.time.Clock()
FPS = 60

# Cargar imágenes
fondo = pygame.image.load("sprites/fondo.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

hormiga_img = pygame.image.load("sprites/hormiga.png").convert_alpha()
hormiga_img = pygame.transform.scale(hormiga_img, (50, 50))

# Mano (obstáculo)
obstaculo_img = pygame.image.load("sprites/obstaculo.png").convert_alpha()

# --- Escalado proporcional de la mano ---
orig_w, orig_h = obstaculo_img.get_size()           # dimensiones reales (359×649)
target_w = 80                                        # ancho deseado en píxeles
scale_factor = target_w / orig_w                     # factor de escala
target_h = int(orig_h * scale_factor)                # altura calculada
obstaculo_img = pygame.transform.scale(obstaculo_img, (target_w, target_h))
obstaculo_img_inv = pygame.transform.flip(obstaculo_img, False, True)
# ------------------------------------------

restart_img = pygame.image.load("sprites/restart.png").convert_alpha()
restart_rect = restart_img.get_rect(center=(ANCHO // 2, ALTO // 2))

# Variables del juego
gravedad = 0.5
salto = -8
espacio_entre_obstaculos = 200
velocidad_obstaculo = 3
puntos = 0
objetivo = 20         

# Clase Hormiga
class Hormiga:
    def __init__(self):
        self.x = 50
        self.y = ALTO // 2
        self.vel_y = 0
        self.img = hormiga_img
        self.rect = self.img.get_rect(center=(self.x, self.y))

    def actualizar(self):
        self.vel_y += gravedad
        self.y += self.vel_y
        self.rect.centery = self.y

    def saltar(self):
        self.vel_y = salto

    def dibujar(self):
        ventana.blit(self.img, self.rect)

# Clase Obstáculo
class Obstaculo:
    def __init__(self):
        self.x = ANCHO
        self.centro = random.randint(150, ALTO - 150)
        # Creamos los rects usando la imagen ya escalada
        self.rect_arriba = obstaculo_img_inv.get_rect(
            midbottom=(self.x, self.centro - espacio_entre_obstaculos // 2)
        )
        self.rect_abajo = obstaculo_img.get_rect(
            midtop=(self.x, self.centro + espacio_entre_obstaculos // 2)
        )

    def mover(self):
        self.rect_arriba.x -= velocidad_obstaculo
        self.rect_abajo.x -= velocidad_obstaculo

    def dibujar(self):
        ventana.blit(obstaculo_img_inv, self.rect_arriba)
        ventana.blit(obstaculo_img, self.rect_abajo)

    def fuera_pantalla(self):
        return self.rect_abajo.right < 0

# Función para mostrar texto en pantalla
def mostrar_texto(texto, tamano, color, y):
    fuente = pygame.font.SysFont(None, tamano)
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=(ANCHO // 2, y))
    ventana.blit(superficie, rect)

# Inicialización del juego
hormiga = Hormiga()
obstaculos = []
contador_obstaculos = 0
juego_activo = True
ganaste = False

# Bucle principal
while True:
    reloj.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if juego_activo and evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            hormiga.saltar()
        elif not juego_activo and not ganaste and evento.type == pygame.MOUSEBUTTONDOWN:
            if restart_rect.collidepoint(evento.pos):
                # Reiniciar juego tras perder
                hormiga = Hormiga()
                obstaculos.clear()
                puntos = 0
                juego_activo = True
        elif ganaste and evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
            # Reiniciar juego tras ganar
            hormiga = Hormiga()
            obstaculos.clear()
            puntos = 0
            juego_activo = True
            ganaste = False

    ventana.blit(fondo, (0, 0))

    if juego_activo:
        hormiga.actualizar()
        hormiga.dibujar()

        # Generar nuevos obstáculos
        contador_obstaculos += 1
        if contador_obstaculos > 90:
            obstaculos.append(Obstaculo())
            contador_obstaculos = 0

        # Mover y dibujar cada obstáculo
        for obstaculo in list(obstaculos):
            obstaculo.mover()
            obstaculo.dibujar()

            # Colisiones
            if hormiga.rect.colliderect(obstaculo.rect_arriba) or hormiga.rect.colliderect(obstaculo.rect_abajo):
                juego_activo = False

            # Contar puntos al pasar
            if obstaculo.rect_abajo.right < hormiga.x and not hasattr(obstaculo, 'pasado'):
                puntos += 1
                obstaculo.pasado = True

            # Borrar fuera de pantalla
            if obstaculo.fuera_pantalla():
                obstaculos.remove(obstaculo)

        # Chequear límites superior/inferior
        if hormiga.y < 0 or hormiga.y > ALTO:
            juego_activo = False

        # Mostrar puntaje
        mostrar_texto(f"Puntos: {puntos}", 36, (0, 0, 0), 40)

        # Verificar victoria
        if puntos >= objetivo:
            juego_activo = False
            ganaste = True

    elif ganaste:
        mostrar_texto("¡Ganaste!", 60, (0, 150, 0), ALTO // 2)
        mostrar_texto("Presiona R para reiniciar", 30, (0, 0, 0), ALTO // 2 + 50)

    else:
        mostrar_texto("Perdiste", 60, (200, 0, 0), ALTO // 2 - 50)
        ventana.blit(restart_img, restart_rect)

    pygame.display.update()
