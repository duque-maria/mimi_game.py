import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de pantalla
ANCHO, ALTO = 400, 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Salva a Mimi")
RELOJ = pygame.time.Clock()

# Cargar y preparar imágenes
FONDO = pygame.image.load("sprites/fondo.png").convert()
FONDO = pygame.transform.scale(FONDO, (ANCHO, ALTO))

HORMIGA_IMG = pygame.image.load("sprites/hormiga.png").convert_alpha()
HORMIGA_IMG = pygame.transform.scale(HORMIGA_IMG, (50, 50))

# — Carga y escala de obstáculos —

# Mano corta
OBST_CORTA_IMG = pygame.image.load("sprites/obstaculo_corta.png").convert_alpha()
w_corta, h_corta = OBST_CORTA_IMG.get_size()
target_w_corta = 60
scale_c = target_w_corta / w_corta
OBST_CORTA_IMG = pygame.transform.scale(
    OBST_CORTA_IMG,
    (target_w_corta, int(h_corta * scale_c))
)
OBST_CORTA_INV = pygame.transform.flip(OBST_CORTA_IMG, False, True)

# Mano larga
OBST_LARGA_IMG = pygame.image.load("sprites/obstaculo_larga.png").convert_alpha()
OBST_LARGA_INV = pygame.transform.flip(OBST_LARGA_IMG, False, True)

# Botón reiniciar
RESTART_IMG = pygame.image.load("sprites/restart.png").convert_alpha()
RESTART_RECT = RESTART_IMG.get_rect(center=(ANCHO // 2, ALTO // 2))

# Splash screen
SPLASH_IMG = pygame.image.load("sprites/splash.png").convert()
SPLASH_IMG = pygame.transform.scale(SPLASH_IMG, (ANCHO, ALTO))
SPLASH_FONT = pygame.font.SysFont('comicsansms', 24)

# Fuente de juego
GAME_FONT = pygame.font.SysFont(None, 36)

# Parámetros
GRAVEDAD = 0.5
SALTO = -8
GAP = 200
VEL_OBST = 4
OBJETIVO = 20

class Hormiga:
    def __init__(self):
        self.imagen = HORMIGA_IMG
        self.rect = self.imagen.get_rect(center=(100, ALTO // 2))
        self.vel = 0

    def saltar(self):
        self.vel = SALTO

    def mover(self):
        self.vel += GRAVEDAD
        self.rect.y += self.vel

    def dibujar(self):
        PANTALLA.blit(self.imagen, self.rect)

class ParObstaculos:
    def __init__(self):
        x = ANCHO + 50
        # y_gap es la coordenada vertical donde termina el obstáculo de arriba
        y_gap = random.randint(100, ALTO - GAP - 100)

        # Elegir tipo de mano para cada uno
        img_sup = random.choice([OBST_CORTA_INV, OBST_LARGA_INV])
        img_inf = random.choice([OBST_CORTA_IMG, OBST_LARGA_IMG])

        # Crear rects anclados a los bordes con gap
        self.rect_sup = img_sup.get_rect(midbottom=(x, y_gap))
        self.rect_inf = img_inf.get_rect(midtop=(x, y_gap + GAP))

        self.img_sup = img_sup
        self.img_inf = img_inf
        self.pasado = False

    def mover(self):
        self.rect_sup.x -= VEL_OBST
        self.rect_inf.x -= VEL_OBST

    def dibujar(self):
        PANTALLA.blit(self.img_sup, self.rect_sup)
        PANTALLA.blit(self.img_inf, self.rect_inf)

    def colisiona(self, hormiga):
        return (self.rect_sup.colliderect(hormiga.rect) or
                self.rect_inf.colliderect(hormiga.rect))

    def fuera_pantalla(self):
        return self.rect_inf.right < 0

def mostrar_splash():
    esperando = True
    while esperando:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
                esperando = False
        PANTALLA.blit(SPLASH_IMG, (0, 0))
        texto = SPLASH_FONT.render("Presiona SPACE para comenzar", True, (255,255,255))
        rect = texto.get_rect(center=(ANCHO//2, ALTO - 50))
        PANTALLA.blit(texto, rect)
        pygame.display.update()
        RELOJ.tick(60)

def mostrar_texto(texto, tamaño, x, y, color=(255,255,255)):
    fuente = pygame.font.SysFont(None, tamaño)
    surf = fuente.render(texto, True, color)
    PANTALLA.blit(surf, (x, y))

def juego():
    hormiga = Hormiga()
    obstaculos = []
    punt = 0
    jugando = True

    EVENT_OBST = pygame.USEREVENT
    pygame.time.set_timer(EVENT_OBST, 1500)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if jugando and ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
                hormiga.saltar()
            if ev.type == EVENT_OBST and jugando:
                obstaculos.append(ParObstaculos())
            if not jugando and ev.type == pygame.MOUSEBUTTONDOWN:
                if RESTART_RECT.collidepoint(ev.pos):
                    return

        PANTALLA.blit(FONDO, (0,0))
        hormiga.mover()
        hormiga.dibujar()

        for par in list(obstaculos):
            par.mover()
            par.dibujar()
            if par.colisiona(hormiga) or hormiga.rect.top < 0 or hormiga.rect.bottom > ALTO:
                jugando = False
            if not par.pasado and par.rect_inf.right < hormiga.rect.left:
                punt += 1
                par.pasado = True
            if par.fuera_pantalla():
                obstaculos.remove(par)

        mostrar_texto(f"Puntos: {punt}", 36, 10, 10)

        if punt >= OBJETIVO:
            mensaje = GAME_FONT.render("¡GANASTE!", True, (0,200,0))
            PANTALLA.blit(mensaje, mensaje.get_rect(center=(ANCHO//2, ALTO//2)))
            pygame.display.update()
            pygame.time.delay(2000)
            return

        if not jugando:
            PANTALLA.blit(RESTART_IMG, RESTART_RECT)

        pygame.display.update()
        RELOJ.tick(60)

# Bucle principal
while True:
    mostrar_splash()
    juego()
