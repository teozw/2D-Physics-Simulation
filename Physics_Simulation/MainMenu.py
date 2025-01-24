import pygame
from utils.button import Button

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True


def main_menu():
    global running
    pygame.display.set_caption("Main Menu")
    Quit_Button = Button('Quit', 50, 'white', [WIDTH // 2, HEIGHT // 1.3])
    Particle = Button('Particle', 50, 'white', [WIDTH // 4, HEIGHT // 3])
    Planet = Button('Planet', 50, 'white', [3 * WIDTH // 4, HEIGHT // 3])

    while running:

        screen.fill('black')
        Quit_Button.add_button(screen)
        Particle.add_button(screen)
        Planet.add_button(screen)

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            elif events.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if Quit_Button.check_input(mouse_pos):
                    running = False
                    pygame.quit()
                    quit()
                elif Particle.check_input(mouse_pos):
                    from BallSimulation.ball_main import main_ball_simulation
                    main_ball_simulation(WIDTH, HEIGHT) 
                elif Planet.check_input(mouse_pos):
                    from PlanetSimulation.planet_main import main_planet_simulation
                    main_planet_simulation(WIDTH, HEIGHT)

        pygame.display.update()


if __name__ == '__main__':
    main_menu()
