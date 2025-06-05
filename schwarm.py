# -*- coding: utf-8 -*-
import pygame
import random
import math

# Pygame initialisieren
pygame.init()
pygame.mixer.init()

# Sound laden
click_sound = pygame.mixer.Sound("click.mp3")

# Fenstergröße
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Partikelschwarm")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Partikelklasse
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity_x = random.uniform(-5, 5)
        self.velocity_y = random.uniform(-5, 5)
        self.mass = 1
        self.sound_played = False
        self.trail = []
        self.trail_length = 50
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update(self, mouse_x, mouse_y, particles):
        # Gravitationskraft zum Mauszeiger berechnen
        distance_x_mouse = mouse_x - self.x
        distance_y_mouse = mouse_y - self.y
        distance_mouse = math.sqrt(distance_x_mouse ** 2 + distance_y_mouse ** 2)
        distance_mouse = max(distance_mouse, 5)
        force_mouse = 100 / distance_mouse ** 2

        force_x_mouse = force_mouse * distance_x_mouse / distance_mouse
        force_y_mouse = force_mouse * distance_y_mouse / distance_mouse

        acceleration_x = force_x_mouse / self.mass
        acceleration_y = force_y_mouse / self.mass

        # Gravitationskraft zwischen den Partikeln berechnen
        for other in particles:
            if other is not self:
                distance_x = other.x - self.x
                distance_y = other.y - self.y
                distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
                distance = max(distance, 5)  # Verhindet Division durch Null

                force = 1 / distance ** 2  # Schwache Anziehungskraft

                force_x = force * distance_x / distance
                force_y = force * distance_y / distance

                acceleration_x += force_x / self.mass
                acceleration_y += force_y / self.mass

                # Kollisionserkennung und Sound abspielen
                if distance < 20 and not self.sound_played:
                    try:
                        click_sound.play()
                        self.sound_played = True
                    except Exception as e:
                        print(f"Error playing sound: {e}")

        # Geschwindigkeit aktualisieren
        self.velocity_x += acceleration_x
        self.velocity_y += acceleration_y

        # Dämpfung hinzufügen
        self.velocity_x *= 0.99
        self.velocity_y *= 0.99

        # Position aktualisieren
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Trail aktualisieren
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)

        # Begrenzung der Bildschirmränder
        if self.x < 0 or self.x > WIDTH:
            self.velocity_x *= -1
        if self.y < 0 or self.y > HEIGHT:
            self.velocity_y *= -1

    def draw(self, screen):
        # Trail zeichnen
        for i, pos in enumerate(self.trail):
            color_value = int(255 * (i / len(self.trail)))
            color = (self.color[0], self.color[1], color_value)
            pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), 3)
        # Partikel zeichnen
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)

# Schwarm erstellen
particles = []
for _ in range(100):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    particles.append(Particle(x, y))

# Hauptschleife
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mausposition abrufen
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Bildschirm löschen
    screen.fill(BLACK)

    # Partikel aktualisieren und zeichnen
    for particle in particles:
        particle.update(mouse_x, mouse_y, particles)
        particle.draw(screen)

    # Rotes Objekt zeichnen, das dem Mauszeiger folgt
    pygame.draw.circle(screen, RED, (mouse_x, mouse_y), 10)

    # Bildschirm aktualisieren
    pygame.display.flip()

# Pygame beenden
pygame.quit()
