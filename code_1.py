import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de ventana
ANCHO = 400
ALTO = 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Lleva a Mimi al hormiguero")

# Colores
marron_claro = (222, 184, 135)
marrón = (205, 133, 63)
VERDE = (0, 200, 0)
NEGRO = (0, 0, 0)


# Fuente
fuente = pygame.font.SysFont(None, 40)

# Reloj
clock = pygame.time.Clock()
FPS = 60

# Parámetros de la hormiga
hormi_x = 50
hormi_y = 300
hormi_vel = 0
GRAVEDAD = 0.3
SALTO = -6
radio_hormi = 15

# Tubos
tubos = []
espacio_tubos = 200
ancho_tubo = 70
vel_tubos = 4

# Puntaje
puntos = 0

def crear_tubo():
    altura = random.randint(100, 400)
    return {'x': ANCHO, 'altura': altura}

def dibujar_texto(texto, x, y):
    img = fuente.render(texto, True, NEGRO)
    VENTANA.blit(img, (x, y))

def colision(hormi_y, tubos):
    for tubo in tubos:
        en_rango_x = tubo['x'] < hormi_x + radio_hormi < tubo['x'] + ancho_tubo
        en_rango_y = hormi_y - radio_hormi < tubo['altura'] or hormi_y + radio_hormi > tubo['altura'] + espacio_tubos
        if en_rango_x and en_rango_y:
            return True
    return hormi_y + radio_hormi > ALTO or hormi_y - radio_hormi < 0

def mostrar_splash_screen():
    VENTANA.fill(marron_claro)
    dibujar_texto("Lleva a Mimi a el hormiguero", 10, 200)
    dibujar_texto("¡Buena suerte!", 100, 300)
    dibujar_texto("Presiona una tecla", 60, 400)
    dibujar_texto("para que inicie el juego...", 60, 440)
    pygame.display.update()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                esperando = False

# Mostrar splash screen antes del juego
mostrar_splash_screen()

# Bucle principal del juego
while True:
    clock.tick(FPS)
    VENTANA.fill(marrón)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                hormi_vel = SALTO

    hormi_vel += GRAVEDAD
    hormi_y += hormi_vel

    if not tubos or tubos[-1]['x'] < ANCHO - 250:
        tubos.append(crear_tubo())

    nuevos_tubos = []
    for tubo in tubos:
        tubo['x'] -= vel_tubos
        if tubo['x'] + ancho_tubo > 0:
            nuevos_tubos.append(tubo)
        pygame.draw.rect(VENTANA, VERDE, (tubo['x'], 0, ancho_tubo, tubo['altura']))
        pygame.draw.rect(VENTANA, VERDE, (tubo['x'], tubo['altura'] + espacio_tubos, ancho_tubo, ALTO))
        if tubo['x'] + ancho_tubo == hormi_x:
            puntos += 1

    tubos = nuevos_tubos

    pygame.draw.circle(VENTANA, NEGRO, (hormi_x, int(hormi_y)), radio_hormi)

    if colision(hormi_y, tubos):
        dibujar_texto("Game Over", 100, 250)
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    dibujar_texto(str(puntos), 10, 10)

    pygame.display.update()