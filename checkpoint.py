import pygame

class Checkpoint:
    def __init__(self, location):
        self.location = location
        self.image = pygame.image.load("data/checkpoint/checkpoint.png")
        self.make_rects()

    def make_rects(self):
        x_cord = self.location[0]
        y_cord = self.location[1]
        self._rect = pygame.Rect(x_cord, y_cord, self.image.get_width(),
                                 self.image.get_height())
        
    def get_checkpoint(self):
        """
        Return a rect containing the location and size of the checkpoint
        """
        return self._rect
