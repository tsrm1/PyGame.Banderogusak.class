import pygame                           # импортируем библиотеку pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def strip_from_sheet(self, col_row, col_span, width1, height1, width2, height2, colour=(0, 0, 0)):
        """ Strips individual frames from specific sprite sheet. """
        images = []
        for i in range(col_span):
            for j in range(col_row):
                image = pygame.Surface((width1, height1)).convert_alpha()
                image.blit(self.sheet, (0, 0), (j * width1, i * height1, width1, height1))
                image = pygame.transform.scale(image, (width2, height2))
                image.set_colorkey(colour)
                images.append(image)
        return images