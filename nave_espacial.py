# Todas los imports necesarios
import pygame
import sys
import random
import time

pygame.init()

# Variables Globales
size = ([900, 600])
screen = pygame.display.set_mode(size)
angle = 0

# Colores
WHITE = (255, 255, 255)
RED = (219, 78, 40)
BLACK = (0, 0, 0)
DIMGREY = (105, 105, 105)
DARKRED = (161, 40, 48)

clock = pygame.time.Clock()
pygame.display.set_caption("Don't get hit")
background = pygame.image.load("background.jpg")

# Clase del jugador
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("nave_espacial.png").convert()
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, (54,55))
        self.rect = self.image.get_rect()
        
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        player.rect.x = mouse_pos[0]
        player.rect.y = mouse_pos[1]

# Clase del asteroide
class Asteroid(pygame.sprite.Sprite):
    
    def __init__(self, side, speed_x, speed_y, meteor_size=(20, 20)):
        super().__init__()
        self.image = pygame.image.load("asteroide.png").convert()
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, meteor_size)
        self.rect = self.image.get_rect()
        self.init_position = None
        self.side = side
        self.speed_x = speed_x
        self.speed_y = speed_y
        
# Lista de los sprites
meteor_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
   
# Se crea al jugador y se lo añade a la lista de sprites
player = Player()
all_sprites_list.add(player)
        
# Pantalla del menú principal
def main_menu():
    
    pygame.mouse.set_visible(1)
    done = False
    
    # Fuente de los textos
    font = pygame.font.SysFont("Comic", 50, bold = True)
    font2 = pygame.font.SysFont("Comic", 80, bold = True)
    text1 = font.render('OPRIME UN BOTON PARA CONTINUAR', True, WHITE)
    text2 = font2.render('PLAY', True, WHITE)
    text3 = font2.render('QUIT', True, WHITE)
    
    button_1 = pygame.Rect(150, 200, 600, 100)
    button_2 = pygame.Rect(250, 350, 400, 100)
    
    # Bucle que registra los eventos 
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Click en los botones del menu
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if button_1.collidepoint((mx, my)):
                    play_game()
                elif button_2.collidepoint((mx ,my)):
                    sys.exit()
                    
                
        screen.blit(background, (0, 0))
        
        # Dibujar rectangulos
        pygame.draw.rect(screen, RED, button_1)
        pygame.draw.rect(screen, RED, button_2)
        
        # Mostrar texto por pantalla
        screen.blit(text1, (75, 100))
        screen.blit(text2, (370, 230))
        screen.blit(text3, (370, 380))
        
        pygame.display.flip()
        clock.tick(60)


# La funcion que es el juego en si
def play_game():
    
    # Timer
    start_time = time.time()
    score_time_limit = 10
    time_limit = 3
    
    pygame.mouse.set_visible(0)
    done = False
    
    # Configuracion del fichero
    fichero = open("tiempo.txt", "w")
    fichero.write("3")
    fichero.close()
    fichero = open("tiempo.txt","r")
    decreascent_time = float(fichero.read())
    fichero.close()
    
    # Variables para la aletoriedad de los meteoros
    width, height = screen.get_size()
    sides = ['top', 'bottom', 'left', 'right']
    weights = [width, width, height, height]
    
    # Score
    score = 0
    font = pygame.font.SysFont("Comic", 30, bold = True)
    
    # Bucle principal del juego
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        # Renderizado del score
        text1 = font.render('SCORE = {}'.format(score), True, WHITE)
        
        # Velocidades de los meteoros
        x_speed = random.randint(0, 6)
        y_speed = random.randint(0, 6)
        metor_size = random.randint(30, 120)
        
        # Eleccion random de las variables
        side = random.choices(sides, weights)[0]
        
        if side == 'top':
            y = -100 
            x = random.randrange(width-4)
        elif side == 'bottom':
            y = height +50
            x = random.randrange(width-4)
        elif side == 'left':
            x = -50
            y = random.randrange(height-4)
        elif side == 'right':
            x = width +50
            y = random.randrange(height-4)
        
        # Timer
        elapsed_time = time.time() - start_time
        if decreascent_time > 0.18:    
            if elapsed_time > time_limit:
                meteor = Asteroid(side, x_speed, y_speed, meteor_size=(metor_size, metor_size))
                meteor_list.add(meteor)
                all_sprites_list.add(meteor)                
                meteor.rect.x = x
                meteor.rect.y = y
                meteor.init_position = side
                
                # Aumento de la dificultad disminuyendo el tiempo
                fichero = open("tiempo.txt","r")
                decreascent_time = float(fichero.read())
                decreascent_time -= 0.10
                fichero.close()
                fichero = open("tiempo.txt", "w")
                fichero.write("{}".format(decreascent_time))
                fichero.close()
                time_limit += decreascent_time
        else:
            if elapsed_time > time_limit:
                meteor = Asteroid(side, x_speed, y_speed, meteor_size=(metor_size, metor_size))
                meteor_list.add(meteor)
                all_sprites_list.add(meteor)
                meteor.rect.x = x
                meteor.rect.y = y
                meteor.init_position = side
                time_limit += 0.18
        
        # Actualizar el score
        if elapsed_time > score_time_limit:
            score += 75
            score_time_limit += 10
        
        # Actualiza los sprites
        all_sprites_list.update()
        
        screen.blit(background, (0, 0))
        
        # Agrupa las colisiones
        meteor_hit_list = pygame.sprite.spritecollide(player, meteor_list, True)
        
        if meteor_hit_list:
            all_sprites_list.empty()
            meteor_list.empty()
            all_sprites_list.add(player)
            game_over()
        
        all_sprites_list.draw(screen)
        
        for meteor in meteor_list:
            if meteor.side == 'top':
                meteor.rect.x += meteor.speed_x
                meteor.rect.y += meteor.speed_y
            elif meteor.side == 'left':
                meteor.rect.x += meteor.speed_x
                meteor.rect.y += meteor.speed_y
            elif meteor.side == 'right':
                meteor.rect.x -= meteor.speed_x
                meteor.rect.y += meteor.speed_y
            elif meteor.side == 'bottom':
                meteor.rect.x += meteor.speed_x
                meteor.rect.y -= meteor.speed_y
            
        screen.blit(text1, (20, 20))
        pygame.display.flip()
        clock.tick(60)

        # recorrer meteoros nuevamente y si un meteoro tiene una posicion mayor a la pantalla y un umbral, sacarlo de la lista.
        for meteor in meteor_list:
            if meteor.rect.x > width + 200 or meteor.rect.x < 0 - 200:
                 meteor_list.remove(meteor)
            elif meteor.rect.y > height + 200 or meteor.rect.y < 0 - 200:
                 meteor_list.remove(meteor)

def game_over():
    
    done = False
    
    # Fuentes y textos
    font = pygame.font.SysFont("Comic", 150, bold = True)
    font2 = pygame.font.SysFont("Comic", 40, bold = True)
    text1 = font.render('GAME OVER', True, WHITE)
    text2 = font2.render('OPRIME UNA TECLA PARA CONTINUAR', True, WHITE)
    
    # Bucle de Game Over
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main_menu()
        
        screen.fill(BLACK)
        
        # Mostrar el texto por pantalla
        screen.blit(text1, (75, 200))
        screen.blit(text2, (140, 330))
    
        pygame.display.flip()
        clock.tick(60)

main_menu()
