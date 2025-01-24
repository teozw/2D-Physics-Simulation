import pygame
import math
from utils.function import *
from BallSimulation.ball import Ball


class Pendulum:

    def __init__(self, pivot: list[float], init_pos: list[float]):
        self.ball = Ball(init_pos[0], init_pos[1], 0, 0, 10, 'white', 1, 5, 1)
        self.pivot = pivot
        self.length = get_distance(init_pos, pivot)
        self.angle = math.pi / 2 - get_angle(init_pos, pivot)
        self.angular_acceleration = 0
        self.velocity = 0
        self.damping = 0.5

    def draw_pendulum(self, screen):
        self.ball.draw(screen)
        pygame.draw.line(screen, 'white', self.ball.pos, self.pivot)

    def update_pos(self, gravity, dt, scale):
        self.angular_acceleration += -gravity * math.sin(self.angle) / self.length * self.damping
        self.ball.pos[0] = self.pivot[0] + self.length * math.sin(self.angle)
        self.ball.pos[1] = self.pivot[1] + self.length * math.cos(self.angle)
        self.angle += self.angular_acceleration * dt ** 2 * scale

    def draw_vector(self, screen, scale):
        self.velocity = self.angular_acceleration * self.length * 0.05
        self.ball.velo[0] = self.velocity * math.cos(self.angle) * 0.1
        self.ball.velo[1] = -self.velocity * math.sin(self.angle) * 0.1
        self.ball.draw_vector(screen, scale)




