import pygame                           # импортируем библиотеку pygame

class BaseObject:
    def __init__(self, x, y, width, height, type, speed_x, speed_y, img_numer_max):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.active = True
        self.type = type                  # Type of Object: Hero, Bonus, Enemy, Weapon, Fire
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.rect = pygame.Rect(x, y, width, height)
        self.img_numer = 0
        self.img_numer_max = img_numer_max


    def move(self, xn, yn):
        self.x += self.speed_x*xn
        self.y += self.speed_y*yn
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    
    def img_change(self):
        self.img_numer += 1
        if self.img_numer == self.img_numer_max:
            self.img_numer = 0

    
    # def info(self):
    #     print(f'X: {self.x}')
    #     print(f'Y: {self.y}')
    #     print(f'Width: {self.width}')
    #     print(f'Height: {self.width}')
    #     print(f'Active: {self.active}')
    #     print(f'Type: {self.type}')
    #     print(f'Speed_X: {self.speed_x}')
    #     print(f'Speed_Y: {self.speed_y}')
    #     print(f'Rect: {self.rect}')
    #     print(f'Img_numer: {self.img_numer}')
    #     print(f'Img_numer_max: {self.img_numer_max}')