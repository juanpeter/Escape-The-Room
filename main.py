import pygame
from pygame.locals import *

from PIL import Image

#CONFIGURAÇÕES PRINCIPAIS
TITLE = 'Escape the Room'
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 288
FPS = 24

#Velocidade do protag
CHAR_WIDTH, CHAR_HEIGHT = ((32),(32))
SPEED = 5

#Medidas do ground
GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

#Medidas da Pipe
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 200

#gravidade
GRAVITY = 1
#velocidade horizontal do jogo
GAME_SPEED = 10

#Criar classe Protag, o personagem principal
class Protag(pygame.sprite.Sprite):

    stepCounter = 0
    #código de inicialização de toda classe Sprite do pygame
    def __init__(self):
        #inicializar sprite
        pygame.sprite.Sprite.__init__(self)

        #Trocar apenas as sprites de acordo com o movimento
        self.images = [
            #front
            pygame.image.load('assets/chars/protagonist/front.png').convert_alpha(),
            #back
            pygame.image.load('assets/chars/protagonist/back.png').convert_alpha(),
            #Side NOTA: Sempre está a direita, usar flip()
            pygame.image.load('assets/chars/protagonist/side1.png').convert_alpha(),
            pygame.image.load('assets/chars/protagonist/side2.png').convert_alpha()
        ]
        # Tamanho das sprites
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i], (CHAR_WIDTH, CHAR_HEIGHT))

        #Velocidade
        self.speed = SPEED

        #A função convert_alpha faz imagens png serem transparentes
        self.image = self.images[0]
        #Criar máscara de colisão
        self.mask = pygame.mask.from_surface(self.image)
        #Necessário para posicionar a sprite na tela
        self.rect = self.image.get_rect()
        #Desenhar o pássaro na metade da tela. o [0] se refere a posição X
        self.rect[0] = SCREEN_WIDTH / 2
        #Desenhar o pássaro na metade da tela. o [1] se refere a posição Y
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
  
        #controles do jogador
        control = pygame.key.get_pressed()

        if control[pygame.K_UP]:
            self.walk('up')
        if control[pygame.K_DOWN]:
            self.walk('down')
        if control[pygame.K_LEFT]:
            self.walk('left')
        if control[pygame.K_RIGHT]:
            self.walk('right')

    def walk(self, pos):

        if pos == 'up':

            self.image = self.images[1]
            protag.rect[1] -= SPEED

            if self.stepCounter % 2 == 0:
                self.image = pygame.transform.flip(self.image, True, False)
            self.stepCounter += 1

        if pos == 'down':
            self.image = self.images[0]
            protag.rect[1] += SPEED

            if self.stepCounter % 2 == 0:
                # time.sleep(SPEED)
                self.image = pygame.transform.flip(self.image, True, False)
            self.stepCounter += 1

        if pos == 'right':
            self.image = self.images[2]

            if self.stepCounter % 2 == 0:
                self.image = self.images[3]

            protag.rect[0] += SPEED
            self.stepCounter += 1

        if pos == 'left':
            self.image = self.images[2]

            if self.stepCounter % 2 == 0:
                self.image = self.images[3]

            self.image = pygame.transform.flip(self.image, True, False)
            
            protag.rect[0] -= SPEED
            self.stepCounter += 1

class Object(pygame.sprite.Sprite):

    def __init__(self, path, positionX, positionY):
        # , imageWidth = Image.width, imageHeight = Image.height
        pygame.sprite.Sprite.__init__(self)
        
        image = Image.open(path)
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, ((2 * image.width), (2 * image.height)))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = positionX
        self.rect[1] = positionY
        self.hitbox = pygame.Rect(positionX, positionY, 2 * image.width - 8, 2 * image.height - 8)
        pygame.draw.rect(screen, (0,255,0), self.hitbox)

    def update(self):
        if self.hitbox.colliderect(protag):
            print('Colidiu!')
            #Left
            if protag.rect.left >= self.rect.left:
                protag.rect.left += SPEED
            #Right
            if protag.rect.right <= self.rect.right:
                protag.rect.right -= SPEED
            #Top
            if protag.rect.top >= self.rect.top:
                protag.rect.top += SPEED
            #Bottom
            if protag.rect.bottom <= self.rect.bottom:
                protag.rect.bottom -= SPEED
            # if protag.rect[1] <= self.rect.bottom:
            #     protag.rect[1] += SPEED
            # if protag.rect[0] >= self.rect.right:
            #     protag.rect[0] += SPEED
            # if protag.rect[1] <= self.rect.top:
            #     protag.rect[1] -= SPEED

#Função para verificar se a sprite está fora da tela
def is_of_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

# Inicializador do jogo
pygame.init()

#display do nome do jogo
pygame.display.set_caption(TITLE)

#configurações de tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pygame.image.load('assets/room.png')

#A imagem de bg terá o tamanho (SCREEN_WIDTH, SCREEN_HEIGHT)
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH + 64, SCREEN_HEIGHT + 48))

#Criar um grupo de protag, criar um protag e adicioná-lo no grupo
protag_group = pygame.sprite.Group()
protag = Protag()
protag_group.add(protag)

#criar grupo de objetos
object_group = pygame.sprite.Group()
bed = Object('assets/objects/bed.png', 32, 96)
window = Object('assets/objects/window.png', 220, 16)
table = Object('assets/objects/table.png', SCREEN_WIDTH / 2 - 48, 48)
object_group.add(window, bed, table)

#fps
clock = pygame.time.Clock()

while True:
    #definir fps no jogo
    clock.tick(FPS)

    Walls = [
        pygame.Rect(0, 0, SCREEN_WIDTH, 56),
        pygame.Rect(0, 0, 24, SCREEN_HEIGHT),
        pygame.Rect(SCREEN_WIDTH - 24, 0, 24, SCREEN_HEIGHT),
        pygame.Rect(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 24),
    ]

    #Loop básico
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    #Criar paredes
    for i in range(4):
        pygame.draw.rect(screen, (255,0,0), Walls[i])
        #Colisão com as paredes
        if Walls[i].colliderect(protag):
            #left
            if protag.rect[0] <=24:
                protag.rect[0] += SPEED
            #top
            if protag.rect[1] <= 52:
                protag.rect[1] += SPEED
            #right
            if protag.rect[0] >= (SCREEN_WIDTH - 47):
                protag.rect[0] -= SPEED
            #bottom
            if protag.rect[1] >= (SCREEN_HEIGHT - 54):
                protag.rect[1] -= SPEED

    screen.blit(BACKGROUND, (-32,-20))

    object_group.update()
    object_group.draw(screen)

    protag_group.update()
    protag_group.draw(screen)

    if False:
        #O jogo acaba
        break

    pygame.display.update()