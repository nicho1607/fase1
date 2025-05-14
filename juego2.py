import pygame
import sys

# Inicialización de PyGame
pygame.init()

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mi Juego en PyGame")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Función para mostrar el menú principal
def mostrar_menu():
    screen.fill(NEGRO)
    fuente = pygame.font.Font(None, 74)
    texto = fuente.render("Presiona ESPACIO para jugar", True, BLANCO)
    screen.blit(texto, (100, 250))
    pygame.display.flip()

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    esperando = False

# Función principal del juego
def juego():
    jugador = pygame.Rect(50, 50, 50, 50)
    enemigo = pygame.Rect(700, 50, 50, 50)
    velocidad_jugador = 5
    velocidad_enemigo = 3

    en_juego = True
    while en_juego:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Controles del jugador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            jugador.y -= velocidad_jugador
        if teclas[pygame.K_DOWN]:
            jugador.y += velocidad_jugador
        if teclas[pygame.K_LEFT]:
            jugador.x -= velocidad_jugador
        if teclas[pygame.K_RIGHT]:
            jugador.x += velocidad_jugador

        # Movimiento del enemigo
        enemigo.x -= velocidad_enemigo
        if enemigo.x < 0:
            enemigo.x = ANCHO

        # Detección de colisión
        if jugador.colliderect(enemigo):
            print("¡Colisión!")
            en_juego = False

        # Dibujar en pantalla
        screen.fill(NEGRO)
        pygame.draw.rect(screen, BLANCO, jugador)
        pygame.draw.rect(screen, ROJO, enemigo)
        pygame.display.flip()
        clock.tick(30)

# Función principal
def main():
    mostrar_menu()
    juego()
    pygame.quit()

if __name__ == "__main__":
    main()
