import math
import pygame.draw
from PlanetSimulation.planet import Planet
from utils.function import *


class Ball(Planet):

    def __init__(self, xpos, ypos, velox, veloy, radius, color, id, mass, restitution):
        super().__init__(xpos, ypos, velox, veloy, radius, color, id, mass)
        self.res = restitution

    def get_resultant_velo(self):
        return math.sqrt(self.velo[0] ** 2 + self.velo[1] ** 2)

    def move(self, dt, gravity, width, height, scale):
        stop = 0.2
        self.velo = list(map(lambda x: round(x, 5), self.velo))

        # Y-Direction Movement
        if self.pos[1] <= self.radius:
            self.pos[1] += self.radius - self.pos[1]
            self.velo[1] *= -1 * self.res
            self.pos[1] += (self.velo[1] * dt + 0.5 * gravity * dt ** 2) * scale

        elif self.pos[1] >= height - self.radius:
            self.pos[1] -= self.radius - (height - self.pos[1])
            if abs(self.pos[1]) < stop:
                self.velo[1] = 0
            else:
                self.velo[1] *= -1 * self.res
                self.pos[1] += (self.velo[1] * dt + 0.5 * gravity * dt ** 2) * scale

        else:
            self.velo[1] += gravity * dt
            self.pos[1] += (self.velo[1] * dt + 0.5 * gravity * dt ** 2) * scale

        # X-Direction Movement
        if self.pos[0] < self.radius:
            self.pos[0] += self.radius - self.pos[0]
            self.velo[0] *= -1 * self.res

        elif self.pos[0] > width - self.radius:
            self.pos[0] -= self.radius - (width - self.pos[0])
            self.velo[0] *= -1 * self.res

        self.pos[0] += (self.velo[0] * dt) * scale

    def solve_collision(self, other, angle):
        # Variables
        m1 = self.mass
        m2 = other.mass
        sin = round(math.sin(angle), 10)
        cos = round(math.cos(angle), 10)

        # Transformation
        v1_x = self.velo[0] * cos + self.velo[1] * sin
        v1_y = self.velo[0] * -sin + self.velo[1] * cos
        v2_x = other.velo[0] * cos + other.velo[1] * sin
        v2_y = other.velo[0] * -sin + other.velo[1] * cos

        # Velocities after collision
        final_velo1 = (m2 * v2_x * (1 + self.res) + v1_x * (m1 - m2 * self.res)) / (m1 + m2)
        final_velo2 = (m1 * v1_x * (1 + other.res) + v2_x * (m2 - m1 * other.res)) / (m1 + m2)
        self.velo = [final_velo1 * cos - v1_y * sin, final_velo1 * sin + v1_y * cos]
        other.velo = [final_velo2 * cos - v2_y * sin, final_velo2 * sin + v2_y * cos]

    def check_collision(self, particles: list):

        for other in particles:
            if other.id != self.id and other.id != 0:
                dx = self.pos[0] - other.pos[0]
                dy = self.pos[1] - other.pos[1]
                ds = math.sqrt(dx ** 2 + dy ** 2)
                if ds < other.radius + self.radius:
                    extra = self.radius + other.radius - ds
                    angle = seperate(self, other, extra, dx, dy)
                    self.solve_collision(other, angle)



