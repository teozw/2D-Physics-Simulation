import pygame
from PlanetSimulation import Planet
from utils.attribute import Attributes

Surface = pygame.Surface


def draw_planet(planets: list[Planet], surface: Surface, scale: float):
    for planet1 in planets:
        for planet2 in planets:
            if planet1 != planet2:
                planet1.resolve_forces(planet2, scale)
        planet1.move()
        p.draw(surface)
        p.draw_lines(surface)
        update_points(planet1)


def update_points(planet: Planet):
    if planet.num_of_points <= 50:
        p.add_points()
    else:
        p.remove_points()


