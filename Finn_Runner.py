import pygame
from sys import exit
from random import randint, choice

#Clase de Finn
class Finn(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        # Animaciones de Finn corriendo, saltando y agachado
        finn_run_1 = pygame.image.load('graphics/Player/Finn_corriendo.png').convert_alpha()
        finn_run_2 = pygame.image.load('graphics/Player/Finn_corriendo2.png').convert_alpha()
        self.finn_run = [finn_run_1, finn_run_2]
        self.finn_index = 0 
        self.finn_jump = pygame.image.load('graphics/Player/Finn_saltando.png').convert_alpha()
        self.finn_duck = pygame.image.load('graphics/Player/Finn_agachado.png').convert_alpha()
        self.image = self.finn_run[self.finn_index] 
        self.rect = self.image.get_rect(midbottom=(80, 300)) # Posicion de Finn
        self.gravity = 0 # Gravedad
        self.is_jumping = False 
        self.is_ducking = False 
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)
    
    # Entrada del jugador
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.is_jumping = True
            self.jump_sound.play()
        if keys[pygame.K_DOWN] and not self.is_jumping:  # Solo agacharse si no está saltando
            self.is_ducking = True
        else:
            self.is_ducking = False

    # Gravedad
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            self.gravity = 0
            self.is_jumping = False

    # Animaciones de Finn
    def update_animation(self):
        if self.is_jumping:
            self.image = self.finn_jump
        elif self.is_ducking:
            self.image = self.finn_duck
            self.rect = self.image.get_rect(midbottom=(80, 320))
        else:
            self.finn_index += 0.1
            if self.finn_index >= len(self.finn_run):
                self.finn_index = 0
            self.image = self.finn_run[int(self.finn_index)]

    # Actualizacion de Finn
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.update_animation()


        
#Clase de obstaculos
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 215 #Posicion donde salen las moscas
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1-1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2-1.png').convert_alpha()
            self.frames = [snail_1,snail_2]
            y_pos  = 300 #Posicion donde salen los caracoles

        self.animation_index = 0 
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos)) # Posicion de los obstaculos
    
    # Animacion de los obstaculos
    def animation_state(self):
        self.animation_index += 0.1 # Velocidad de la animacion
        if self.animation_index >= len(self.frames): self.animation_index = 0 # Reiniciamos la animacion
        self.image = self.frames[int(self.animation_index)] # Actualizamos la animacion

    # Actualizacion de los obstaculos
    def update(self):
        self.animation_state()
        self.rect.x -= 8 # Velocidad de los obstaculos
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:  # Si el obstaculo sale de la pantalla
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time # Tiempo que lleva el jugador jugando
    score_surf = test_font.render(f'Puntaje: {current_time}',False,(64,64,64)) # Texto del tiempo
    score_rect = score_surf.get_rect(center = (400,50)) # Posicion del tiempo
    screen.blit(score_surf,score_rect) # Mostramos el tiempo que lleva el jugador jugando
    return current_time # Retornamos el tiempo que lleva el jugador jugando

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False): # Si Finn choca con un obstaculo
        obstacle_group.empty() # Eliminamos el obstaculo
        return False
    else: return True

pygame.init()
screen = pygame.display.set_mode((800,400)) # Dimensiones de la pantalla
pygame.display.set_caption('Finn Runner') # Nombre del juego
clock = pygame.time.Clock()# Reloj del juego
test_font = pygame.font.Font('font/Pixeltype.ttf', 50) # Fuente del texto
game_active = False # Juego activo
start_time = 0 # Tiempo inicial
score = 0 # Tiempo que lleva el jugador jugando
bg_music = pygame.mixer.Sound('audio/tema2.wav') # Musica de fondo
bg_music.play(loops = -1) # Reproducimos la musica de fondo

player = pygame.sprite.GroupSingle() # Grupo de Finn
player.add(Finn()) # Agregamos a Finn al grupo

obstacle_group = pygame.sprite.Group() # Grupo de obstaculos
sky_surface = pygame.image.load('graphics/2.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

#Pantalla de inicio

finn_stand = pygame.image.load('graphics/Player/cabeza-2.png').convert_alpha() # Imagen de Finn
finn_stand = pygame.transform.rotozoom(finn_stand,0,2) # Escalamos la imagen de Finn
finn_stand_rect = finn_stand.get_rect(center = (400,200)) # Posicion de Finn

game_name = test_font.render('Finn Runner',False,(111,196,169)) # Texto del nombre del juego
game_name_rect = game_name.get_rect(center = (400,80)) # Posicion del nombre del juego

game_message = test_font.render('Presiona espacio para comenzar',False,(111,196,169)) # Texto de instruccion
game_message_rect = game_message.get_rect(center = (400,330)) # Posicion de la instruccion

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500) # Tiempo de aparicion de los obstaculos

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail']))) # Aparecen obstaculos

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000) # Inicia el tiempo

    if game_active:
        screen.blit(sky_surface,(0,0)) # Fondo del juego
        screen.blit(ground_surface,(0,300)) # Suelo del juego
        score = display_score() # Tiempo que lleva el jugador jugando
        
        player.draw(screen) # Dibujamos a Finn
        player.update() # Actualizamos a Finn

        obstacle_group.draw(screen) # Dibujamos los obstaculos
        obstacle_group.update() # Actualizamos los obstaculos

        game_active = collision_sprite() # Si Finn choca con un obstaculo

    else:
        screen.fill((94,129,162)) # Color de fondo
        screen.blit(finn_stand,finn_stand_rect) # Dibujamos a Finn

        score_message = test_font.render(f'Tu Puntaje: {score}',False,(111,196,169)) # Texto del tiempo que lleva el jugador jugando
        score_message_rect = score_message.get_rect(center = (400,330)) # Posicion del tiempo que lleva el jugador jugando
        screen.blit(game_name,game_name_rect) # Dibujamos el nombre del juego

        if score == 0: screen.blit(game_message,game_message_rect) # Si el tiempo es 0, mostramos la instruccion
        else: screen.blit(score_message,score_message_rect) # Si no, mostramos el tiempo que lleva el jugador jugando

    pygame.display.update() # Actualizamos la pantalla
    clock.tick(60) # FPS




