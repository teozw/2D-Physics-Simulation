import pygame
import random
from utils.button import Button
from utils.attributes import Attributes
from utils.function import *
from BallSimulation.ball import Ball
from BallSimulation.pendulum import Pendulum
from BallSimulation.ball_events import *
from resources.constants import *

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
running = True


def main_ball_simulation(w : int | float, h : int | float):
    # Initialization
    global running
    pygame.display.set_caption('Particle Simulation')
    WIDTH, HEIGHT = w, h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    # Create Ball (Max around 300)
    balls: list[Ball] = create_balls(0, w, h)

    # Create Pendulum
    pendulums: list[Pendulum] = [create_pendulum([350, 150], [300, 170])]

    # Buttons
    Back_Button = Button('Back', 50, 'white', [WIDTH - 65, HEIGHT - 40])
    CLear_Button = Button("Clear", 30, 'white', [WIDTH - 65, HEIGHT - 140])

    # Variables
    num_of_balls = len(balls)
    num_of_pendulum = len(pendulums)
    gravity_traits = [Earth_Gravity, "Earth(0)", True, 0]
    gravity = gravity_traits[0]
    substep = 1
    scale = 100  # 100 px : 1 meter
    dt = 0.003 / substep
    draw_ball = False
    draw_pendulum = False
    show_vector = False
    pressed = False
    pivot_point = None
    key_gravity_pairs = {
        pygame.K_0: [Earth_Gravity, "Earth(0)", True, 0],
        pygame.K_1: [Mercury_Gravity, "Mercury(1)", False, 1],
        pygame.K_2: [Venus_Gravity, "Venus(2)", False, 2],
        pygame.K_3: [Mars_Gravity, "Mars(3)", False, 3],
        pygame.K_4: [Jupiter_Gravity, "Jupiter(4)", False, 4],
        pygame.K_5: [Saturn_Gravity, "Saturn(5)", False, 5],
        pygame.K_6: [Uranus_Gravity, "Uranus(6)", False, 6],
        pygame.K_7: [Neptune_Gravity, "Neptune(7)", False, 7],
        pygame.K_8: [Pluto_Gravity, "Pluto(8)", False, 8],
        pygame.K_9: [Moon_Gravity, "Moon(9)", False, 9],
        pygame.K_MINUS: [0, "Weightless(-)", False, 10]
    }

    # Display Attributes
    show_scale = Attributes("Scale", 15, 'white', [WIDTH - 320, 25], f"{scale} px : 1 m")
    total_ball = Attributes('Number of Balls', 15, 'white', [WIDTH - 80, 60], num_of_balls)
    total_pendulum = Attributes('Number of Pendulum', 15, 'white', [WIDTH - 80, 80], num_of_pendulum)
    show_fps = Attributes('FPS', 15, 'white', [WIDTH - 50, 25], int(clock.get_fps()))
    show_gravity = Attributes("Gravity", 17, 'white', [WIDTH - 110, 390], f"{gravity_traits[1]}, {gravity_traits[0]}m/s^2")
    toggle_vector = Attributes("Vector(V)", 17, 'white', [WIDTH - 60, 450], show_vector, False)
    toggle_pendulum = Attributes("Pendulum(P)", 17, 'white', [WIDTH - 60, 470], draw_pendulum, False)
    toggle_ball = Attributes("Ball(B)", 17, 'white', [WIDTH - 60, 490], draw_ball, False)
    gravity_keys: list[Attributes] = create_gravity_attr(screen, key_gravity_pairs)
    length_pendulum = Attributes("Length", 17, 'white')

    while running:

        screen.fill('black')
        # Display Button
        Back_Button.add_button(screen)
        CLear_Button.add_button(screen)

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            elif events.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
                if Back_Button.check_input([mouse_pos_x, mouse_pos_y]):
                    import MainMenu
                    MainMenu.main_menu()
                elif CLear_Button.check_input([mouse_pos_x, mouse_pos_y]):
                    num_of_balls = 0
                    num_of_pendulum = 0
                    balls.clear()
                    pendulums.clear()
                else:
                    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    mouse_state = pygame.mouse.get_pressed()
                    if draw_pendulum:
                        if mouse_state[0]:
                            if not pressed:
                                pressed = True
                                draw_ball = False
                                pivot_point = (mouse_pos_x, mouse_pos_y)
                            else:
                                pressed = False
                                pendulums.append(Pendulum(pivot_point, (mouse_pos_x, mouse_pos_y)))
                                num_of_pendulum += 1
                        elif mouse_state[2] and num_of_pendulum > 0:
                            del pendulums[-1]
                            num_of_pendulum -= 1
                    else:
                        if mouse_state[0]:
                            if not draw_ball:
                                draw_ball = True
                                balls.append(Ball(mouse_pos_x, mouse_pos_y, 0, 0, 10, color, num_of_balls + 1, 5, 0.9))
                            elif draw_ball:
                                draw_ball = False
                                balls[-1].velo = list(map(lambda x, y: -(x - y) * 5/ scale, balls[-1].pos, [mouse_pos_x, mouse_pos_y]))
                                num_of_balls += 1
                                balls[-1].id = num_of_balls
                        elif mouse_state[2] and num_of_balls > 0:
                            del balls[-1]
                            draw_ball = False
                            num_of_balls -= 1

            elif events.type == pygame.KEYDOWN:
                if events.key in key_gravity_pairs:
                    gravity_keys[gravity_traits[3]].attribute = False
                    gravity_traits = key_gravity_pairs[events.key]
                    gravity_keys[gravity_traits[3]].attribute = True
                    gravity_traits[2] = True
                    gravity = gravity_traits[0]
                elif events.key == pygame.K_UP:
                    gravity *= -1
                elif events.key == pygame.K_p and not draw_pendulum:
                    draw_pendulum = True if not draw_pendulum else False
                elif events.key == pygame.K_v:
                    show_vector = True if not show_vector else False
                elif events.key == pygame.K_b and draw_pendulum:
                    draw_pendulum = not draw_pendulum

        if draw_ball:
            end_pos = balls[-1].pos
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.line(screen, 'white', end_pos, mouse_pos)

        if pressed:
            mouse_position = pygame.mouse.get_pos()
            length = round(get_distance(mouse_position, pivot_point) / scale, 2)
            pygame.draw.line(screen, 'white', mouse_position, pivot_point)
            pygame.draw.circle(screen, 'white', mouse_position, 10)
            new_position = list(map(lambda x: x + 30, mouse_position))
            length_pendulum.update_position(new_position)
            length_pendulum.update_attribute(length, True)
            length_pendulum.draw_text(screen)

        # Draw Objects
        draw_balls(balls, screen, dt, gravity, WIDTH, HEIGHT, substep, scale, show_vector)
        draw_pendulums(pendulums, screen, gravity, dt, scale, show_vector)
        draw_border(screen)
        display_toggle(toggle_vector, show_vector, screen)
        display_toggle(toggle_pendulum, draw_pendulum, screen)
        display_toggle(toggle_ball, not draw_pendulum, screen)

        # Update Attributes
        total_ball.update_attribute(num_of_balls, True)
        total_pendulum.update_attribute(num_of_pendulum, True)
        show_fps.update_attribute(int(clock.get_fps()), True)
        show_gravity.update_attribute(f"{gravity_traits[1][:-3]}, {gravity}m/s^2", True)
        toggle_vector.update_attribute(show_vector)
        toggle_pendulum.update_attribute(draw_pendulum)
        toggle_ball.update_attribute(not draw_pendulum)

        # Display Attributes
        display_gravity_attr(screen, gravity_keys)
        total_ball.draw_text(screen)
        total_pendulum.draw_text(screen)
        show_gravity.draw_text(screen)
        show_fps.draw_text(screen)
        show_scale.draw_text(screen)
        right_align_attributes(toggle_ball, toggle_vector, toggle_pendulum, position=[WIDTH - 50, 400], screen=screen)

        clock.tick(1/dt)
        pygame.display.update()


if __name__ == "__main__":
    main_ball_simulation(800, 800)
