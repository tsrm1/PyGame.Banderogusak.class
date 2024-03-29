""" Игра "Бандерогусак"
    На основе классов (ООП)
    Анимация героя (управление), фона, врагов, бонусов
"""

import pygame                           # импортируем библиотеку pygame
from baseClass import BaseObject
import spritesheet                      # импортируем библиотеку spritesheet (создали отдельно, находиться в той же папке)
from os import listdir                  # импортируем метод listdir
import random                           # импортируем библиотеку random
import time                             # импортируем библиотеку time  (time.sleep(3))





if __name__ == '__main__':
    pygame.init()                           # инициализируем/вызываем библиотеку pygame
    SCREEN_SIZE = WIDTH, HEIGHT = 1920, 1080  # ширина и высота окна
    main_surface = pygame.display.set_mode((SCREEN_SIZE), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN) # создаём поверхность отрисовки
    # main_surface = pygame.display.set_mode((screen_size), pygame.DOUBLEBUF | pygame.HWSURFACE) # создаём поверхность отрисовки
    # set_mode(Width, Height) - формируем/вызываем окно (щирина, высота) в pixel
    # pygame.DOUBLEBUF - двойная буферизация
    # pygame.HWSURFACE - аппаратное ускорение отрисовки
    # pygame.FULLSCREEN - полноэкранный режим
    # pygame.OPENGL - обработка отображений с помощью библиотеки OpenGL
    # pygame.RESIZABLE - окно с  изменяемыми размерами
    # pygame.NOFRAME - окно без рамки и заголовка
    # pygame.SCALED - разрешение, зависящее от размеров рабочего стола
    pygame.display.set_caption("Banderogusak on PyGame")                        # устанавливаем название окна
    pygame.display.set_icon(pygame.image.load("image/Farm-Goose.ico"))              # устанавливаем иконку окна
    clock = pygame.time.Clock()             # создаём экземпляр класса Clock
    FPS = 30                                # устанавливаем частоту обработки цикла, FPS раз в секунду

    backgrounds = []
    enemies = []
    bonuses = []
    weapons = []

    BG_IMG_PATH = 'image/background.png'
    BG_IMG_SPEED = 2, 0
    BG_IMAGES = [pygame.transform.scale(pygame.image.load(BG_IMG_PATH).convert(), SCREEN_SIZE)]    # создаём поверхность "бекграунд" и загружаем на неё изображение
    BG_IMG_MAX = len(BG_IMAGES)
    
    BILDINGS_HEIGHT = HEIGHT - HEIGHT // 3    # высота неба над уровнем зданий

    HERO_IMG_PATH = 'image/Goose'
    HERO_IMG_SIZE = 100, 30
    HERO_IMG_SPEED = 6, 8
    HERO_IMAGES = [pygame.transform.scale(pygame.image.load(HERO_IMG_PATH + '/' + file ).convert_alpha(), HERO_IMG_SIZE) for file in listdir(HERO_IMG_PATH)]
    HERO_IMG_MAX = len(HERO_IMAGES)

    ENEMY_IMG_PATH = 'image/Enemy'
    ENEMY_IMG_SIZE = 70, 25                     # размер изображения "врага" (ширина, высота) 
    # ENEMY_IMAGES = [pygame.transform.scale(pygame.image.load(ENEMY_IMG_PATH).convert_alpha(),ENEMY_IMG_SIZE)]
    ENEMY_IMAGES = [pygame.transform.scale(pygame.image.load(ENEMY_IMG_PATH + '/' + file ).convert_alpha(), ENEMY_IMG_SIZE) for file in listdir(ENEMY_IMG_PATH)]
    ENEMY_IMG_MAX = len(ENEMY_IMAGES)

    BONUS_IMG_PATH = 'image/bonus.png'
    BONUS_IMG_SIZE = 50, 83
    BONUS_IMAGES = [pygame.transform.scale(pygame.image.load(BONUS_IMG_PATH).convert_alpha(), BONUS_IMG_SIZE)]    # создаём поверхность "бонуса" и загружаем на неё изображение
    BONUS_IMG_MAX = len(BONUS_IMAGES)

    images = [BG_IMAGES, HERO_IMAGES, ENEMY_IMAGES, BONUS_IMAGES]

      
    # Создаём фон, type = 0
    backgrounds.append(BaseObject(0, 0, *SCREEN_SIZE, 0, *BG_IMG_SPEED, BG_IMG_MAX))  # инициазируем объект класса BaseObject 
    backgrounds.append(BaseObject(WIDTH, 0, *SCREEN_SIZE, 0, *BG_IMG_SPEED, BG_IMG_MAX))


    # Создаём героя, type = 1
    hero = BaseObject(WIDTH/2, HEIGHT/2, *HERO_IMG_SIZE, 1, *HERO_IMG_SPEED, HERO_IMG_MAX)  # инициазируем объект класса BaseObject 


    # Создаём врага, type = 2
    def create_enemy():
        enemy_img_speed_x = random.randint(4, 6)      # создаём произвольную скорость "врага"        
        enemy_img_speed_y = random.random()      # создаём произвольную скорость "врага"        
        enemy = BaseObject(WIDTH-70, random.randint(0, BILDINGS_HEIGHT), *ENEMY_IMG_SIZE, 2, enemy_img_speed_x, enemy_img_speed_y, ENEMY_IMG_MAX)  # инициазируем объект класса BaseObject 
        return enemy                                # возвращяем данные очередного "врага"
    
    # Создаём бонус, type = 3
    def create_bonus():
        bonus_img_speed = random.randint(2, 4)      # создаём произвольную скорость "бонуса"   
        bonus = BaseObject(random.randint(0, WIDTH), 0, *BONUS_IMG_SIZE, 3, 2, bonus_img_speed, BONUS_IMG_MAX)
        return bonus                                # возвращяем данные очередного "бонуса"



    CHANGE_IMG_HERO = pygame.USEREVENT + 1
    pygame.time.set_timer(CHANGE_IMG_HERO, 125)               # установка таймера вызова функции смены изображения "героя", 125 мс

    CREATE_ENEMY = pygame.USEREVENT + 2
    pygame.time.set_timer(CREATE_ENEMY, 1500)      # установка таймера вызова функции создания нового "врага", 1500 мс

    CHANGE_IMG_ENEMY = pygame.USEREVENT + 3
    pygame.time.set_timer(CHANGE_IMG_ENEMY, 125)               # установка таймера вызова функции смены изображения "врага", 125 мс

    CREATE_BONUS = pygame.USEREVENT + 4
    pygame.time.set_timer(CREATE_BONUS, 1500)               # установка таймера вызова функции сосздания нового "бонуса", 2000 мс

    # start game loop
    hero.active = True                              # флаг "герой жив", "герой умирает"
    game_over = False                               # флаг "конец игры", игра закончилась
    while not game_over:                            # start game loop
        for event in pygame.event.get():            # переменная event принимает значение сообщений из очереди событий pygame.event.
            if event.type == pygame.QUIT:           # проверяем ТИП события event, равно ли QUIT (нажата ли иконка закрытия рабочего окна)
                game_over = True                    # выход из основного цикла
            
            
            if event.type == CHANGE_IMG_HERO:                       # если появилось событие изменить изображение "героя"
                hero.img_change()
                
            if event.type == CREATE_ENEMY:                          # если появилось событие создать "врага"
                enemies.append(create_enemy())                      # в список "врагов" добавляем нового "врага"

            if event.type == CHANGE_IMG_ENEMY:                       # если появилось событие изменить изображение "героя"
                for enemy in enemies:
                    enemy.img_change()

            if event.type == CREATE_BONUS:                          # если появилось событие создать "бонус"
                bonuses.append(create_bonus())                      # в список "врагов" добавляем новый "бонус"

        #################################################################################################################
        # управление "героем"
        keys = pygame.key.get_pressed()                         # в переменную key записываем состояние всех клавиш на клавиатуре
        # все нажатые кнопки имеют статус TRUE (1), остальные FALSE (0)
        if keys[pygame.K_LEFT] and hero.x > 0:                  # если кнопка K_LEFT нажата и поверхность "героя" не в самом начале
            hero.move(-1, 0)                                    # свдвигаем поверхность "героя" влево
        if keys[pygame.K_RIGHT] and hero.x + hero.width < WIDTH:    # если кнопка K_RIGHT нажата и поверхность "героя" не в самом конце
            hero.move(1, 0)                                     # свдвигаем поверхность "героя" вправо
        if keys[pygame.K_UP] and hero.y > 0:                    # если кнопка K_UP нажата и поверхность "героя" не в самом верху
            hero.move(0, -1)                                    # свдвигаем поверхность "героя" вверх
        if keys[pygame.K_DOWN] and hero.y + hero.height < HEIGHT:   # если кнопка K_DOWN нажата и поверхность "героя" не в самом низу
            hero.move(0, 1)                                     # свдвигаем поверхность "героя" вниз

        #################################################################################################################
        # Сдвиг всей анимации
        # Фон
        for bg in backgrounds:
            bg.move(-1, 0)
            if bg.x <= -WIDTH:
                bg.x = WIDTH
            print(bg.rect)

        # Враги
        for enemy in enemies:
            enemy.move(-1, 1)

        # Бонусы
        for bonus in bonuses:
            bonus.move(-1, 1)    

        #################################################################################################################
        # Построение картинки
        # Фон
        # main_surface.fill((0,0,0))
        for bg in backgrounds:
            main_surface.blit(images[0][bg.img_numer], (bg.x, bg.y))        # накладываем поверность "бэкграунд" на основную поверхность "фон"
        
        # Герой
        main_surface.blit(images[1][hero.img_numer], (hero.x, hero.y))      # накладываем поверность "героя" на основную поверхность "фон"
        
        # Враги
        for enemy in enemies:
            main_surface.blit(images[2][enemy.img_numer], (enemy.x, enemy.y))    # накладываем поверхность "врага" на основную поверхность "фон"

        # Бонусы
        for bonus in bonuses:
            main_surface.blit(images[3][bonus.img_numer], (bonus.x, bonus.y))    # накладываем поверхность "врага" на основную поверхность "фон"

        pygame.display.update()             # вывод прямоугольной области (списка областей) из буфера
        clock.tick(FPS)                     # вызывааем метод tick() класса Clock(), устанавливаем задержку для цикла, FPS
                                            # FPS раз в секунду с учётом времени на выполнение операций в самом цикле
 

    # pygame.display.update()             # вывод прямоугольной области (списка областей) из буфера
    # time.sleep(3)                       # устанавливаем задержку на 3 секунды
    pygame.quit()                       # выход из модуля pygame
    quit()                              # выход из программы
