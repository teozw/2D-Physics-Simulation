import pygame
from utils.function import *
from utils.button import Button
from utils.attributes import Attributes
from PlanetSimulation.planet import Planet

pygame.init()

clock = pygame.time.Clock()
running = True

# CONSTANTS
timestep = 3600 * 24 * 30
G = 6.67430e-11
Mass_of_Sun = 1.989e30
AU = 1.496e11
Mass_of_Earth = 5.972e24
Earth_Velocity = 29784.8
Scale = 250 / AU


def main_planet_simulation(w, h):

    # Initialization
    global running
    WIDTH, HEIGHT = w, h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Planet Simulation')

    # Buttons
    Back_Button = Button('Back', 50, 'white', [WIDTH * 9 / 10, HEIGHT - 50])

    # Variables
    dt = 0.05
    fps = 1 / dt * 5

    # Planet
    planet = []
    num_of_planets = len(planet)
    Sun = Planet(WIDTH // 2, HEIGHT // 2, 0,0, 10, 'yellow', 0, Mass_of_Sun / 100000)
    Earth1 = Planet(WIDTH // 2 - AU * Scale , HEIGHT // 2, 100, 0, 5, 'white', 1, Mass_of_Earth)
    Earth2 = Planet(WIDTH // 2 + AU * Scale, HEIGHT // 2 + 50, -100, 0, 5, 'white', 1, Mass_of_Earth)
    # num_of_planets += 1
    planet.append(Sun)
    # planet.append(Earth1)
    # planet.append(Earth2)

    # Display Attributes
    total_planet = Attributes('Number of Planet', 20, 'white', [WIDTH * 1 / 10, 25], num_of_planets)
    show_fps = Attributes('FPS', 15, 'white', [WIDTH - 50, 25], int(clock.get_fps()))

    while running:

        screen.fill('black')
        Back_Button.add_button(screen)
        show_fps.attribute = int(clock.get_fps())
        show_fps.draw_text(screen)
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            elif events.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if Back_Button.check_input(mouse_pos):
                    from MainMenu import main_menu
                    main_menu()
                else:
                    mouse_state = pygame.mouse.get_pressed()
                    if mouse_state[0]:
                        planet.append(Planet(mouse_pos[0], mouse_pos[1], 100, 0, 5, 'white', num_of_planets + 1, Mass_of_Earth))
                        num_of_planets += 1
                    elif mouse_state[2] and num_of_planets != 0:
                        del planet[-1]
                        num_of_planets -= 1

        for p in planet:
            for k in planet:
                if p != k:
                    p.resolve_forces(k, Scale)
                    num_of_planets = p.collision(k, planet, num_of_planets)
            p.move()
            p.draw(screen)
            p.draw_lines(screen)
            #p.draw_vector(screen, Scale)
            if p.num_of_points <= 50:
                p.add_points()
            else:
                p.remove_points()


        # Update_Attributes
        total_planet.update_attribute(num_of_planets, True)
        show_fps.update_attribute(int(clock.get_fps()), True)

        # Display Attribute
        show_fps.draw_text(screen)
        total_planet.draw_text(screen)

        clock.tick(300)
        pygame.display.update()


if __name__ == "__main__":
    main_planet_simulation()


