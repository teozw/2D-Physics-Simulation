import pygame
from typing import Any


class Attributes:

    def __init__(self, text: str, size: int, color: str | tuple[int], pos: list = None, attribute: Any = None,
                 display: bool = True):
        """

        :param text: Text to display
        :param size: Font size
        :param color: Font color
        :param pos: Position of the center of attributes surface
        :param attribute: Simulation attributes to display
        :param display: Whether to display the attribute
        """
        self.text = text
        self.size = size
        self.color = color
        self.pos = pos
        self.attribute = attribute
        self.font = pygame.font.Font(pygame.font.match_font('inkfree'), self.size)
        self.display = display

        if self.display:
            self.text_surface = self.font.render(f'{self.text}: {self.attribute}', True, self.color)
        else:
            self.text_surface = self.font.render(f'{self.text}', True, self.color)

    def draw_text(self, surface: pygame.Surface):
        text_rect = self.text_surface.get_rect(center=self.pos)
        surface.blit(self.text_surface, text_rect)

    def update_attribute(self, attributes: Any, text_surface_update: bool = False) -> None:
        """
        Updates the attribute by changing the Attributes class object text_surface
        :param attributes: new attribute
        :param text_surface_update: whether to update the text_surface
        :return: None
        """
        self.attribute = attributes
        if text_surface_update:
            self.text_surface = self.font.render(f'{self.text}: {self.attribute}', True, self.color)

    def update_position(self, new_position: list | tuple):
        self.pos = new_position

    def get_width(self):
        return self.text_surface.get_width()

