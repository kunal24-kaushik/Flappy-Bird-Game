import pygame # type: ignore
import random
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize sound system

# Game Variables
WIDTH, HEIGHT = 400, 600
PIPE_WIDTH = 70
PIPE_GAP = 200  # Vertical gap between pipes
GRAVITY = 0.5
FLAP_STRENGTH = -7  # Reduced flap for easier control
FPS = 60

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 150, 255)

# Setup full screen display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
clock = pygame.time.Clock()

# Load fonts
font = pygame.font.SysFont("Arial", 32)
big_font = pygame.font.SysFont("Arial", 64)

# Load bird image
bird_img = pygame.image.load(r"C:\Users\Kunal\OneDrive\Pictures\bird.png")
bird_img = pygame.transform.scale(bird_img, (40, 40))  # Resize the bird image

# Load flap sound (✅ NEW)
flap_sound = pygame.mixer.Sound(r"C:\Users\Kunal\OneDrive\Documents\W.mp3")

# Button class
class Button:
    def __init__(self, x, y, w, h, text=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        if self.text == "Play":
            pygame.draw.rect(screen, GREEN, self.rect)
        elif self.text == "Exit":
            pygame.draw.rect(screen, RED, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 3)
        text_surf = font.render(self.text, True, WHITE)
        screen.blit(text_surf, (self.rect.centerx - text_surf.get_width() // 2,
                                self.rect.centery - text_surf.get_height() // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Bird class
class Bird:
    def __init__(self):
        self.x = SCREEN_WIDTH // 4
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def draw(self):
        screen.blit(bird_img, (self.x - 20, int(self.y) - 20))

    def get_rect(self):
        return pygame.Rect(self.x - 20, self.y - 20, 40, 40)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)

    def update(self):
        self.x -= 3

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT))

    def get_upper_rect(self):
        return pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)

    def get_lower_rect(self):
        return pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT)

# Collision detection
def check_collision(bird, pipes):
    if bird.y - 20 <= 0 or bird.y + 20 >= SCREEN_HEIGHT:
        return True
    for pipe in pipes:
        if bird.get_rect().colliderect(pipe.get_upper_rect()) or bird.get_rect().colliderect(pipe.get_lower_rect()):
            return True
    return False

# Start Menu
def start_menu():
    play_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 40, 200, 80, "Play")

    menu = True
    while menu:
        screen.fill(WHITE)
        title = big_font.render("Flappy Bird", True, RED)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
        play_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(event.pos):
                    menu = False

        pygame.display.flip()
        clock.tick(60)

# Game Over Screen
def game_over_screen(score):
    exit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 80, "Exit")

    screen.fill(BLACK)
    game_over = big_font.render("Game Over", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    motiv_text = font.render("Next time, keep playing buddy!", True, WHITE)

    screen.blit(game_over, (SCREEN_WIDTH // 2 - game_over.get_width() // 2, 200))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))
    screen.blit(motiv_text, (SCREEN_WIDTH // 2 - motiv_text.get_width() // 2, 350))

    exit_button.draw()
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Main Game Loop
def main_game():
    PIPE_DISTANCE = 250
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + i * PIPE_DISTANCE) for i in range(3)]  # 3 pipes to start
    score = 0

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.flap()
                flap_sound.play()  # ✅ Play sound on flap

        bird.update()
        for pipe in pipes:
            pipe.update()

        if pipes[0].x + PIPE_WIDTH < 0:
            pipes.pop(0)
            pipes.append(Pipe(pipes[-1].x + PIPE_DISTANCE))
            score += 1

        if check_collision(bird, pipes):
            game_over_screen(score)
            return

        bird.draw()
        for pipe in pipes:
            pipe.draw()

        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (20, 20))

        if score >= 5:
            congrats_text = font.render("Congrats Buddy!", True, GREEN)
            screen.blit(congrats_text, (SCREEN_WIDTH // 2 - congrats_text.get_width() // 2, 60))

        pygame.display.flip()

# Game Loop
while True:
    start_menu()
    main_game()
