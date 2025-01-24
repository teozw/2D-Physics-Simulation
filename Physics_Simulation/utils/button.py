import pygame
from typing import Any

pygame.init()
pygame.font.init()


class Button:

    def __init__(self, text: str, size: int, color: str | tuple[int, int, int], pos: list[int] | tuple[int, int]):
        """

        :param text: Text to display on the button
        :param size: Font size
        :param color: Font color
        :param pos: Position of the center of the button
        """
        self.text = text
        self.size = size
        self.color = color
        self.pos = pos
        self.font = pygame.font.Font(pygame.font.match_font('inkfree'), self.size)
        self.surface = self.font.render(self.text, True, self.color)
        self.height = self.surface.get_height()
        self.width = self.surface.get_width()

    def add_button(self, surface: pygame.Surface) -> None:
        text_rect = self.surface.get_rect(center=self.pos)
        surface.blit(self.surface, text_rect)

    def check_input(self, position: list) -> bool:
        """
        Check if user click on button

        :param position: Mouse position
        :return: Returns True if mouse position is within the Button
        """
        dx = (position[0] - self.pos[0] + self.width // 2) * (position[0] - self.pos[0] - self.width // 2)
        dy = (position[1] - self.pos[1] + self.width // 2) * (position[1] - self.pos[1] - self.width // 2)
        return True if dx < 0 and dy < 0 else False


