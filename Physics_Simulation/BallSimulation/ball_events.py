import random
import pygame
from BallSimulation.ball import Ball
from BallSimulation.pendulum import Pendulum
from utils.attributes import Attributes
from typing import Optional, NewType, Any

# Type Hinting
Surface = pygame.surface


def create_balls(num: int, width: int, height: int) -> list[Ball]:
    balls = []
    for i in range(num):
        r = random.randint(10, 20)
        x = random.randint(r, width - r)
        y = random.randint(r, height - r)
        vx = random.randint(-5, 5)
        vy = random.randint(-5, 5)
        balls.append(Ball(x, y, vx, vy, 10, 'white', i, 5, 0.9))
    return balls


def create_pendulum(pivot: Optional[list | tuple], ball_pos: Optional[list | tuple]) -> Pendulum:
    return Pendulum(pivot, ball_pos)


def draw_balls(balls: list[Ball], screen: Surface, dt: float, gravity: float, width: int, height: int,
               substep: int, scale: int, show_vector: bool = None) -> None:

    for j in balls:
        for k in range(substep):
            j.move(dt, gravity, width - 250, height, scale)
        j.draw(screen)
        if show_vector:
            j.draw_vector(screen, scale)

    for i in balls:
        i.check_collision(balls)


def draw_pendulums(pendulum: list[Pendulum], screen: Surface, gravity: float, dt: float, scale: int,
                   show_vector: bool) -> None:
    for p in pendulum:
        if show_vector:
            p.draw_vector(screen, scale)
        p.draw_pendulum(screen)
        p.update_pos(gravity, dt, scale)


def create_gravity_attr(screen, pairings: dict[pygame.key, list[Any]]) -> list[list[Any]]:
    attributes = []
    x_pos, y_pos = screen.get_width() - 40, 130
    for key, values in pairings.items():
        attr = Attributes(values[1], 20, 'white', [x_pos, y_pos], values[2], False)
        alignment = x_pos - attr.get_width() / 2
        attr.pos[0] = alignment
        attributes.append(attr)
        y_pos += 20

    return attributes


def display_gravity_attr(screen: Surface, attributes: list[Attributes]) -> None:
    for attr in attributes:
        display_toggle(attr, attr.attribute, screen)
        attr.draw_text(screen)


def draw_border(screen: Surface) -> None:
    width, height = screen.get_width() - 250, screen.get_height()
    pygame.draw.line(screen, 'white',[width, 0], [width, height])
    pygame.draw.line(screen, 'white', [width, 360], [width + 250, 360])
    pygame.draw.line(screen, 'white', [width, 100], [width + 250, 100])
    pygame.draw.line(screen, 'white', [width, 430], [width + 250, 430])
    pygame.draw.line(screen, 'white', [width, 510], [width + 250, 510])


def display_toggle(attribute: Attributes, toggle: bool, screen: Surface) -> None:
    """

    :param attribute: Simulation Attributes
    :param toggle: Whether the specific feature of simulation has been toggled
    :param screen: screen to display the toggle button
    :return: None
    """
    color = 'red' if not toggle else 'green'
    x_pos = attribute.pos[0] + attribute.get_width() / 2 + 10
    pygame.draw.circle(screen, color, [x_pos, attribute.pos[1]], 5)


def right_align_attributes(*args: Attributes | list, position: list[float | int], screen: Surface) -> None:
    """

    :param args: Attributes objects to display on screen
    :param position: A reference point/line to align attributes to
    :param screen: Screen to display simulation attributes
    :return: None
    """
    x_pos, y_pos = position
    for arg in args:
        arg.pos[0] = x_pos - arg.get_width() / 2
        arg.draw_text(screen)
        display_toggle(arg, arg.attribute, screen)

