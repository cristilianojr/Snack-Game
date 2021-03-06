# Pygame Imports
import pygame
from pygame import Surface
from pygame import Rect


class Snake:
    def __init__(self, color: tuple, x: int, y: int, width: int, height: int, size: int = 3) -> None:
        # Basics Attributes
        self.width: int = width
        self.height: int = height
        self.color: tuple = color
        self.x: int = x
        self.y: int = y
        self.size: int = size
        self.direction: tuple[int, int] = [1, 0]
        self._positions: list = [(self.x, self.y),]

        # Create first shape
        self.add_shape()
        self.add_shape()
        self.add_shape()

    def area(self) -> tuple:
        return (self.x, self.y), (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), (self.x, self.y + self.height)

    def move(self) -> list:
        """Ajust positions by a vector 2d"""

        self._positions.insert(0, (
            self._positions[0][0] + self.width * self.direction[0], 
            self._positions[0][1] + self.height * self.direction[1]
            ))

        self.x = self._positions[0][0] + self.width * self.direction[0]
        self.y = self._positions[0][1] + self.height * self.direction[1]

        del self._positions[-1]

    def add_shape(self) -> None:
        """Create a shape in the end of snake"""

        self._positions.append((
            self._positions[-1][0] - self.width * self.direction[0], 
            self._positions[-1][1] - self.height * self.direction[1]
            ))

    def draw(self, surface: Surface) -> tuple:
        for pos in self._positions:
            pygame.draw.rect(surface, self.color, Rect(*pos, self.width, self.height))


class Food:
    def __init__(self, color: tuple, x: int, y: int, width: int, height: int) -> None:
        self.color: tuple = color
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height

    def area(self) -> tuple:
        return [(self.x, self.y), (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), (self.x, self.y + self.height)]

    def draw(self, surface: Surface) -> tuple:
        pygame.draw.rect(surface, self.color, Rect(self.x, self.y, self.width, self.height))
