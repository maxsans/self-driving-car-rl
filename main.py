# main.py

import pygame
from game.car import Car
from game.track import Track
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Simulation de Conduite Autonome 2D")
    clock = pygame.time.Clock()

    # Initialiser la voiture et le circuit
    track = Track('assets/track.png')
    car = Car(*track.start_point)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # Temps écoulé depuis la dernière frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Gestion des touches
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            car.accelerate()
        if keys[pygame.K_DOWN]:
            car.brake()
        if keys[pygame.K_LEFT]:
            car.turn_left()
        if keys[pygame.K_RIGHT]:
            car.turn_right()

        # Mettre à jour la voiture
        car.update()
        car.check_collision(track)

        # distances = car.cast_rays(track)
        # print("Ray distances:", distances)

        # Rendu
        screen.fill((0, 0, 0))  # Fond noir
        track.draw(screen)
        car.draw(screen)
        car.draw_rays(screen, track)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
