import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Simulation with AI")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (255, 80, 80)
GREEN = (80, 255, 120)

# Physics object
class Ball:
    def __init__(self, x, y, radius=15, color=BLUE):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.mass = radius

    def update(self):
        # Gravity
        self.vy += 0.2

        # Move
        self.x += self.vx
        self.y += self.vy

        # Wall collisions
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.vx *= -0.9

        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.vy *= -0.9
            self.y = min(max(self.radius, self.y), HEIGHT - self.radius)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


# AI-controlled ball that chases a target
class AIBall(Ball):
    def __init__(self, x, y):
        super().__init__(x, y, radius=18, color=RED)

    def chase(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        dist = math.hypot(dx, dy)

        if dist != 0:
            self.vx += (dx / dist) * 0.2
            self.vy += (dy / dist) * 0.2


# Collision detection between balls
def handle_collision(b1, b2):
    dx = b2.x - b1.x
    dy = b2.y - b1.y
    dist = math.hypot(dx, dy)

    if dist < b1.radius + b2.radius:
        # Normalize
        nx = dx / dist
        ny = dy / dist

        # Relative velocity
        dvx = b1.vx - b2.vx
        dvy = b1.vy - b2.vy

        # Dot product
        impact = dvx * nx + dvy * ny

        if impact > 0:
            return

        # Collision response
        impulse = 2 * impact / (b1.mass + b2.mass)

        b1.vx -= impulse * b2.mass * nx
        b1.vy -= impulse * b2.mass * ny
        b2.vx += impulse * b1.mass * nx
        b2.vy += impulse * b1.mass * ny


# Create objects
player = Ball(WIDTH // 2, HEIGHT // 2, color=GREEN)
enemy = AIBall(100, 100)

balls = [player, enemy]

# Add some random balls
for _ in range(5):
    balls.append(Ball(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)))

# Main loop
running = True
while running:
    clock.tick(60)
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player control (arrow keys)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.vx -= 0.5
    if keys[pygame.K_RIGHT]:
        player.vx += 0.5
    if keys[pygame.K_UP]:
        player.vy -= 0.5
    if keys[pygame.K_DOWN]:
        player.vy += 0.5

    # AI behavior
    enemy.chase(player)

    # Update objects
    for ball in balls:
        ball.update()

    # Handle collisions
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            handle_collision(balls[i], balls[j])

    # Draw objects
    for ball in balls:
        ball.draw()

    pygame.display.flip()

pygame.quit()