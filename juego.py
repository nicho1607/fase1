import pygame
import random
import sys

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nave Espacial - PyGame")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fuente
font = pygame.font.SysFont('Arial', 24)

# Clase para la nave del jugador (opcional, como mencionaste)
class Player:
    def __init__(self):
        self.width = 50
        self.height = 30
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 20
        self.speed = 5
        self.color = GREEN
        
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Dibujar punta de la nave
        pygame.draw.polygon(screen, self.color, [
            (self.x + self.width // 2, self.y - 20),
            (self.x, self.y),
            (self.x + self.width, self.y)
        ])
        
    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < WIDTH - self.width:
            self.x += self.speed

# Clase para los enemigos (asteroides)
class Enemy:
    def __init__(self):
        self.size = random.randint(20, 50)
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size
        self.speed = random.randint(2, 5)
        self.color = RED
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x + self.size//2, self.y + self.size//2), self.size//2)
        
    def move(self):
        self.y += self.speed
        return self.y > HEIGHT

# Función para mostrar el menú principal
def show_menu():
    menu = True
    while menu:
        screen.fill(BLACK)
        title = font.render("NAVE ESPACIAL - PYTHON PYGAME", True, WHITE)
        start = font.render("1. Iniciar Juego", True, GREEN)
        instructions = font.render("2. Instrucciones", True, BLUE)
        exit_text = font.render("3. Salir", True, RED)
        
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        screen.blit(start, (WIDTH//2 - start.get_width()//2, 200))
        screen.blit(instructions, (WIDTH//2 - instructions.get_width()//2, 250))
        screen.blit(exit_text, (WIDTH//2 - exit_text.get_width()//2, 300))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "start"
                if event.key == pygame.K_2:
                    return "instructions"
                if event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

# Función para mostrar instrucciones
def show_instructions():
    showing = True
    while showing:
        screen.fill(BLACK)
        title = font.render("INSTRUCCIONES", True, WHITE)
        line1 = font.render("Usa las flechas izquierda y derecha para mover la nave", True, BLUE)
        line2 = font.render("Evita los asteroides rojos", True, BLUE)
        line3 = font.render("Presiona ESC para volver al menú", True, BLUE)
        back = font.render("Presiona ESC para volver", True, GREEN)
        
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        screen.blit(line1, (WIDTH//2 - line1.get_width()//2, 200))
        screen.blit(line2, (WIDTH//2 - line2.get_width()//2, 250))
        screen.blit(line3, (WIDTH//2 - line3.get_width()//2, 300))
        screen.blit(back, (WIDTH//2 - back.get_width()//2, 400))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

# Función para detectar colisiones
def check_collision(player, enemy):
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.size, enemy.size)
    return player_rect.colliderect(enemy_rect)

# Función principal del juego
def game_loop():
    player = Player()
    enemies = []
    score = 0
    enemy_spawn_timer = 0
    game_over = False
    
    clock = pygame.time.Clock()
    
    running = True
    while running:
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if game_over and event.key == pygame.K_r:
                    return "restart"
        
        if not game_over:
            # Movimiento del jugador
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.move("left")
            if keys[pygame.K_RIGHT]:
                player.move("right")
            
            # Generación de enemigos
            enemy_spawn_timer += 1
            if enemy_spawn_timer >= 30:  # Cada 30 frames
                enemies.append(Enemy())
                enemy_spawn_timer = 0
            
            # Movimiento y eliminación de enemigos
            for enemy in enemies[:]:
                if enemy.move():  # Si el enemigo sale de la pantalla
                    enemies.remove(enemy)
                    score += 1
            
            # Detección de colisiones
            for enemy in enemies:
                if check_collision(player, enemy):
                    game_over = True
        
        # Dibujado
        screen.fill(BLACK)
        
        # Dibujar estrellas de fondo
        for _ in range(50):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            pygame.draw.circle(screen, WHITE, (x, y), 1)
        
        player.draw()
        for enemy in enemies:
            enemy.draw()
        
        # Mostrar puntuación
        score_text = font.render(f"Puntuación: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        if game_over:
            game_over_text = font.render("¡GAME OVER! Presiona R para reiniciar", True, RED)
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2))
        
        pygame.display.update()
        clock.tick(60)
    
    return "menu"

# Función principal
def main():
    while True:
        menu_choice = show_menu()
        
        if menu_choice == "start":
            result = game_loop()
            if result == "restart":
                continue
        elif menu_choice == "instructions":
            show_instructions()

if __name__ == "__main__":
    main()