""" Игра 'Бандерогусак'
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
    RED = (255, 0, 0),              # цвет красный
    backgrounds = []
    enemies = []
    bonuses = []
    weapons = []
    explotions = []

    score = 0               # количество "бонусов"
    hiscore = 100000        # рекорд "бонусов"
    score_fail = 0          # количество пропущенных "ракет"
    score_damage = 0        # количество сбитых "ракет"
    score_weapon_max = 9    # максимально допустимое количество "снарядов"
    score_weapon = 3        # текущее количество "снарядов"
    font_score = pygame.font.SysFont('Verdana', 20)         # устанавливаем шрифт и размер текста (px) для отображения "бонуса"
    font_game_over = pygame.font.SysFont('Verdana', 40)     # устанавливаем шрифт и размер текста (px) для отображения "Game Over"
    game_over_massege = False
    
    BG_IMG_PATH = 'image/background.png'
    BG_IMG_SPEED = 2
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
    ENEMY_IMAGES = [pygame.transform.scale(pygame.image.load(ENEMY_IMG_PATH + '/' + file).convert_alpha(), ENEMY_IMG_SIZE) for file in listdir(ENEMY_IMG_PATH)]
    ENEMY_IMG_MAX = len(ENEMY_IMAGES)

    BONUS_IMG_PATH = 'image/Bonus'
    BONUS_IMG_SIZE = 50, 83
    BONUS_IMAGES = [pygame.transform.scale(pygame.image.load(BONUS_IMG_PATH+ '/' + file).convert_alpha(), BONUS_IMG_SIZE) for file in listdir(BONUS_IMG_PATH)]  
    BONUS_IMG_MAX = len(BONUS_IMAGES)

    HERO_EXPLOTION_IMG_PATH = 'image/sprite-explosion-48p-255x255.png'
    HERO_EXPLOTION_IMG_SIZE = 256, 256
    sprite_sheet_image_explotion_hero = pygame.image.load(HERO_EXPLOTION_IMG_PATH).convert_alpha()
    sprite_sheet_hero_explotion = spritesheet.SpriteSheet(sprite_sheet_image_explotion_hero)
    HERO_EXPLOTION_IMAGES = sprite_sheet_hero_explotion.strip_from_sheet(8, 6, 256, 256, 256, 256)   # (col_row, col_span, width_in, height_in, width_out, height_out, colour=(0, 0, 0))
    HERO_EXPLOTION_IMG_MAX = len(HERO_EXPLOTION_IMAGES)


    ENEMY_EXPLOTION_PATH = 'image/sprite-explosion-20p-192x192.png'
    ENEMY_EXPLOTION_SIZE = 192, 192
    sprite_sheet_image_explotion_bonus = pygame.image.load(ENEMY_EXPLOTION_PATH).convert_alpha()
    sprite_sheet_bonus_explotion = spritesheet.SpriteSheet(sprite_sheet_image_explotion_bonus)
    ENEMY_EXPLOTION_IMAGES = sprite_sheet_bonus_explotion.strip_from_sheet(5, 4, 192, 192, 192, 192)   # (col_row, col_span, width_in, height_in, width_out, height_out, colour=(0, 0, 0))
    ENEMY_EXPLOTION_IMG_MAX = len(ENEMY_EXPLOTION_IMAGES)

    WEAPON_IMG_PATH = 'image/sprite_farbe_9.png'
    WEAPON_IMG_SIZE = 150, 150
    sprite_sheet_image_weapon = pygame.image.load(WEAPON_IMG_PATH).convert_alpha()
    sprite_sheet_weapon = spritesheet.SpriteSheet(sprite_sheet_image_weapon)
    WEAPON_IMAGES = sprite_sheet_weapon.strip_from_sheet(3, 3, 700, 700, 150, 150)   # (col_row, col_span, width, height, scale, colour=(0, 0, 0))
    WEAPON_IMG_MAX = len(WEAPON_IMAGES)

    images = [BG_IMAGES, HERO_IMAGES, ENEMY_IMAGES, BONUS_IMAGES, ENEMY_EXPLOTION_IMAGES, HERO_EXPLOTION_IMAGES, WEAPON_IMAGES]

      
    # Создаём фон, type = 0
    backgrounds.append(BaseObject(0, 0, *SCREEN_SIZE, 0, BG_IMG_SPEED, 0, BG_IMG_MAX))  # инициазируем объект класса BaseObject 
    backgrounds.append(BaseObject(WIDTH, 0, *SCREEN_SIZE, 0, BG_IMG_SPEED, 0, BG_IMG_MAX))


    # Создаём героя, type = 1
    hero = BaseObject(WIDTH/2, HEIGHT/2, *HERO_IMG_SIZE, 1, *HERO_IMG_SPEED, HERO_IMG_MAX)  # инициазируем объект класса BaseObject 


    # Создаём врага, type = 2
    def create_enemy():
        enemy_img_speed_x = random.randint(BG_IMG_SPEED +2, BG_IMG_SPEED +4)    # создаём произвольную скорость "врага"        
        enemy_img_speed_y = random.random()         # создаём произвольную скорость "врага"        
        enemy = BaseObject(WIDTH-70, random.randint(0, BILDINGS_HEIGHT), *ENEMY_IMG_SIZE, 2, enemy_img_speed_x, enemy_img_speed_y, ENEMY_IMG_MAX)  # инициазируем объект класса BaseObject 
        return enemy                                # возвращяем данные очередного "врага"
    
    # Создаём бонус, type = 3
    def create_bonus():
        bonus_img_speed = random.randint(2, 4)      # создаём произвольную скорость "бонуса"   
        bonus = BaseObject(random.randint(0, WIDTH), 0, *BONUS_IMG_SIZE, 3, BG_IMG_SPEED, bonus_img_speed, BONUS_IMG_MAX)
        return bonus                                # возвращяем данные очередного "бонуса"

    # Создаём взрыв, type = 4
    def create_explotion_air(x, y, speed_x, speed_y):
        exploation = BaseObject(x - 96, y -96, *ENEMY_EXPLOTION_SIZE, 4, speed_x, speed_y, ENEMY_EXPLOTION_IMG_MAX)
        return exploation                                # возвращяем данные очередного "воздушного взрыва"
    
    # Создаём взрыв, type = 5
    def create_explotion_hero(x, y, speed_x, speed_y):
        exploation = BaseObject(x - 128, y -128, *HERO_EXPLOTION_IMG_SIZE, 5, speed_x, speed_y, HERO_EXPLOTION_IMG_MAX)
        return exploation                                # возвращяем данные очередного "воздушного взрыва"
    hero_explode = False

    # Создаём оружие, type = 6
    def create_weapon(x, y):
        weapon = BaseObject(x - 150, y - 75, *WEAPON_IMG_SIZE, 6, BG_IMG_SPEED, 0, WEAPON_IMG_MAX)  # инициазируем объект класса BaseObject 
        return weapon                                # возвращяем данные очередного "оружия"


    GAME_OVER_FINAL_COUNTDOWN = pygame.USEREVENT + 1
    
    GAME_OVER_TIMER_MESSAGE = pygame.USEREVENT + 2

    CHANGE_IMG_HERO = pygame.USEREVENT + 3
    pygame.time.set_timer(CHANGE_IMG_HERO, 125)     # установка таймера вызова функции смены изображения "героя", 125 мс

    CREATE_ENEMY = pygame.USEREVENT + 4
    pygame.time.set_timer(CREATE_ENEMY, 1500)       # установка таймера вызова функции создания нового "врага", 1500 мс

    CHANGE_IMG_ENEMY = pygame.USEREVENT + 5
    pygame.time.set_timer(CHANGE_IMG_ENEMY, 125)    # установка таймера вызова функции смены изображения "врага", 125 мс

    CREATE_BONUS = pygame.USEREVENT + 6
    pygame.time.set_timer(CREATE_BONUS, 1500)       # установка таймера вызова функции сосздания нового "бонуса", 2000 мс

    CHANGE_IMG_BONUS = pygame.USEREVENT + 7
    pygame.time.set_timer(CHANGE_IMG_BONUS, 125)    # установка таймера вызова функции смены изображения "врага", 125 мс
    CHANGE_IMG_BONUS = pygame.USEREVENT + 7
    pygame.time.set_timer(CHANGE_IMG_BONUS, 125)    # установка таймера вызова функции смены изображения "врага", 125 мс

    CHANGE_IMG_EXPLODE = pygame.USEREVENT + 8
    pygame.time.set_timer(CHANGE_IMG_EXPLODE, 125)  # установка таймера вызова функции смены изображения "взрыва", 125 мс

    CHANGE_IMG_WEAPONS = pygame.USEREVENT + 9
    pygame.time.set_timer(CHANGE_IMG_WEAPONS, 300)    # установка таймера вызова функции смены изображения "врага", 300 мс





    # start game loop
    hero.active = True                              # флаг "герой жив", "герой умирает"
    game_over = False                               # флаг "конец игры", игра закончилась
    while not game_over:                            # start game loop
        for event in pygame.event.get():            # переменная event принимает значение сообщений из очереди событий pygame.event.
            if event.type == pygame.QUIT:           # проверяем ТИП события event, равно ли QUIT (нажата ли иконка закрытия рабочего окна)
                game_over = True                    # выход из основного цикла
            elif event.type == pygame.KEYDOWN:      # если событие - это нажатие кнопки на клавиатуре
                if event.key == pygame.K_SPACE and score_weapon >0:  # если нажатая и отрущена кнопка Space
                    weapons.append(create_weapon(hero.x, hero.y + hero.height / 2))
                    score_weapon -=1
            
            if event.type == CHANGE_IMG_HERO:       # если появилось событие изменить изображение "героя"
                hero.img_change()

            if event.type == GAME_OVER_FINAL_COUNTDOWN:       # если появилось событие "конец игры"
                game_over = True
                
            if event.type == GAME_OVER_TIMER_MESSAGE:       # если появилось событие "Game over"
                game_over_massege = True

            if event.type == CREATE_ENEMY:          # если появилось событие создать "врага"
                enemies.append(create_enemy())      # в список "врагов" добавляем нового "врага"

            if event.type == CHANGE_IMG_ENEMY:      # если появилось событие изменить изображение "героя"
                for enemy in enemies:
                    enemy.img_change()

            if event.type == CREATE_BONUS:          # если появилось событие создать "бонус"
                bonuses.append(create_bonus())      # в список "врагов" добавляем новый "бонус"

            if event.type == CHANGE_IMG_BONUS:      # если появилось событие изменить изображение "бонус"
                for bonus in bonuses:
                    bonus.img_change()   

            if event.type == CHANGE_IMG_EXPLODE:      # если появилось событие изменить изображение "бонус"
                for explotion in explotions:
                    explotion.img_change()   
                    if explotion.img_numer >= explotion.img_numer_max - 1:
                        explotions.pop(explotions.index(explotion))           # удаляем "взрыв" из списка "взрывов"

            if event.type == CHANGE_IMG_WEAPONS:      # если появилось событие изменить изображение "оружия"
                for weapon in weapons:
                    weapon.img_change()   

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

        # Враги
        for enemy in enemies:
            enemy.move(-1, 1)

        # Бонусы
        for bonus in bonuses:
            bonus.move(-1, 1)    
        
        # Взрывы
        for explotion in explotions:
            explotion.move(-1, 1) 

        # Оружие
        for weapon in weapons:
            weapon.move(-1, 1) 
        
        #################################################################################################################
        # Вычисление пересечений
        # Ракеты с бонусами, зданиями, пределами игрового поля, оружием, героем
        for enemy in enemies:
            delete_enemy = 0
            explotion = 0
            for bonus in bonuses:
                if enemy.rect.colliderect(bonus.rect):      # если враг попал в бонус
                    bonuses.pop(bonuses.index(bonus))       # удаляем "бонус" из списка "бонусов"            
                    delete_enemy +=1
                    explotion +=1
                    # score_fail += 1                         # увеличиваем счётчик прилётов
            for weapon in weapons:
                if enemy.rect.colliderect(weapon.rect):      # если враг попал в оружие
                    weapons.pop(weapons.index(weapon))       # удаляем "оружие" из списка "оружий"            
                    delete_enemy +=1
                    explotion +=1
                    score_damage += 1
            if enemy.x + enemy.width <= 0:
                    delete_enemy +=1
                    score_fail += 1                         # увеличиваем счётчик прилётов
            if enemy.y + enemy.height >  BILDINGS_HEIGHT + 200:
                    delete_enemy +=1
                    score_fail += 1                         # увеличиваем счётчик прилётов
                    explotion +=1
            if enemy.rect.colliderect(hero.rect):
                    delete_enemy +=1
                    explotion +=1
                    score_damage += 1
                    hero.active = False
                    hero_explode = True
                    pygame.time.set_timer(GAME_OVER_FINAL_COUNTDOWN, 8000)               # установка таймера "конец игры", 8000 мс   
                    pygame.time.set_timer(GAME_OVER_TIMER_MESSAGE, 4000)               # установка таймера вывод сообщения "Game over", 5000 мс   

            if delete_enemy:
                if hero_explode:
                    explotions.append(create_explotion_hero(enemy.x, enemy.y + enemy.height/2, (enemy.speed_x + BG_IMG_SPEED) /3, enemy.speed_y))
                    hero_explode = False
                else:
                    explotions.append(create_explotion_air(enemy.x, enemy.y + enemy.height/2, (enemy.speed_x + BG_IMG_SPEED) /3, enemy.speed_y))
                enemies.pop(enemies.index(enemy))           # удаляем "врага" из списка "врагов"
        
        # Бонусы с пределами игрового поля, героем
        for bonus in bonuses:
            delete_bonus = 0
            if bonus.rect.colliderect(hero.rect):      # если бонус попал в героя
                delete_bonus +=1
                if score_weapon <= score_weapon_max -3:
                    score_weapon += 3
            if bonus.y + bonus.height > HEIGHT:
                delete_bonus +=1

            if delete_bonus:
                bonuses.pop(bonuses.index(bonus))           # удаляем "бонус" из списка "бонусов"




        #################################################################################################################
        # Построение картинки
        # Фон
        for bg in backgrounds:
            main_surface.blit(images[bg.type][bg.img_numer], (bg.x, bg.y))                # накладываем поверности "бэкграунд" на основную поверхность "фон"
        
        # Герой
        if hero.active:
            main_surface.blit(images[hero.type][hero.img_numer], (hero.x, hero.y))              # накладываем поверность "героя" на основную поверхность "фон"
        
        # Враги
        for enemy in enemies:
            main_surface.blit(images[enemy.type][enemy.img_numer], (enemy.x, enemy.y))       # накладываем поверхности "врага" на основную поверхность "фон"

        # Бонусы
        for bonus in bonuses:
            main_surface.blit(images[bonus.type][bonus.img_numer], (bonus.x, bonus.y))       # накладываем поверхности "бонусы" на основную поверхность "фон"

        # Оружие
        for weapon in weapons:
            main_surface.blit(images[weapon.type][weapon.img_numer], (weapon.x, weapon.y))       # накладываем поверхности "оружие" на основную поверхность "фон"

        # Взрывы
        for explotion in explotions:
            main_surface.blit(images[explotion.type][explotion.img_numer], (explotion.x, explotion.y))    # накладываем поверхности "взрывы" на основную поверхность "фон"

        # Инфо
        if hero.active:
            score = score_damage - score_fail
        main_surface.blit(font_score.render('Пострілів: '+str(score_weapon), True, RED), (50, 0))  # накладываем поверность "текст" на основную поверхность "фон"
        main_surface.blit(font_score.render('Ракет у повiтрi: '+str(len(enemies)), True, RED), (250, 0))  # накладываем поверность "текст" на основную поверхность "фон"
        main_surface.blit(font_score.render('Прильотів: '+str(score_fail), True, RED), (510, 0))  # накладываем поверность "текст" на основную поверхность "фон"
        main_surface.blit(font_score.render('Збито ракет: '+str(score_damage), True, RED), (730, 0))  # накладываем поверность "текст" на основную поверхность "фон"
        main_surface.blit(font_score.render('Бонусів: '+str(score), True, RED), (970, 0))  # накладываем поверность "текст" на основную поверхность "фон"
        main_surface.blit(font_score.render('Рекорд гусака: '+str(hiscore), True, RED), (1170, 0))  # накладываем поверность "текст" на основную поверхность "фон"

        # Сообщение "Game over"
        if game_over_massege:
            main_surface.blit(font_game_over.render('Гусаку капець. Грі кінець.', True, RED), (WIDTH/2-250, HEIGHT/2-40))  # накладываем поверность "текст" на основную поверхность "фон"
            main_surface.blit(font_game_over.render('Твій результат: ' + str(score), True, RED), (WIDTH/2-250, HEIGHT/2+10))  # накладываем поверность "текст" на основную поверхность "фон"

        pygame.display.update()             # вывод прямоугольной области (списка областей) из буфера
        clock.tick(FPS)                     # вызывааем метод tick() класса Clock(), устанавливаем задержку для цикла, FPS
                                            # FPS раз в секунду с учётом времени на выполнение операций в самом цикле
 
    # pygame.display.update()             # вывод прямоугольной области (списка областей) из буфера
    # time.sleep(4)                       # устанавливаем задержку на 4 секунды
    pygame.quit()                       # выход из модуля pygame
    quit()                              # выход из программы
