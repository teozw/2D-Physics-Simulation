import pygame
from utils.function import *


class Planet:

    AU = 1.496e11
    Scale = 250 / AU
    timestep = 3600 * 24 * 30
    G = 6.67430e-11

    def __init__(self, xpos, ypos, velox, veloy, radius, color, id, mass):
        self.pos = [xpos, ypos]
        self.velo = [velox, veloy]
        self.radius = radius
        self.color = color
        self.id = id
        self.mass = mass
        self.points = []
        self.num_of_points = 0

    def move(self):
        self.pos[0] += self.velo[0] * self.Scale * self.timestep
        self.pos[1] += self.velo[1] * self.Scale * self.timestep

    def resolve_forces(self, other, scaling):
        angle = abs(get_angle(self.pos, other.pos))
        force = (self.G * self.mass * other.mass / (get_distance(self.pos, other.pos)/ scaling) ** 2)
        dx = other.pos[0] - self.pos[0]
        dy = other.pos[1] - self.pos[1]
        fx = force * math.cos(angle) if dx > 0 else -force * math.cos(angle)
        fy = force * math.sin(angle) if dy > 0 else -force * math.cos(angle)
        self.velo[0] += fx / self.mass * self.timestep
        self.velo[1] += fy / self.mass * self.timestep

    def draw(self, surface):
        pygame.draw.circle(surface, color=self.color, center=self.pos, radius=self.radius)

    def collision(self, other, planets, num):
        if get_distance(self.pos, other.pos) < other.radius + self.radius:
            overlapped_distance = self.radius + other.radius - get_distance(self.pos, other.pos)
            seperate(self, other, overlapped_distance, self.pos[0] - other.pos[0], self.pos[1] - other.pos[1])
            planets.remove(self) if self.id != 0 else planets.remove(other)
            return num - 1
        return num

    def add_points(self):
        updated_pos = [self.pos[0], self.pos[1]]
        self.points.append(updated_pos)
        self.num_of_points += 1

    def remove_points(self):
        self.points.pop(0)
        self.num_of_points -= 1

    def draw_lines(self, surface):
        if self.num_of_points >= 2:
            pygame.draw.aalines(surface, 'white', False, self.points)

    def draw_vector(self, screen, scale):
        end_pos = list(map(lambda x, y: (x + y * scale / 5), self.pos, self.velo))
        pygame.draw.line(screen, "red", self.pos, end_pos)

