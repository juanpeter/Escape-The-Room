import pygame
from pygame.locals import *

from PIL import Image

#CONFIGURAÇÕES PRINCIPAIS
TITLE = 'Escape the Room'
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 288
FPS = 24
GAME_TIMER = 100
FONT_SIZE = 16

#Velocidade do protag
CHAR_WIDTH, CHAR_HEIGHT = ((32),(32))
SPEED = 5

#Criar classe Protag, o personagem principal
class Protag(pygame.sprite.Sprite):
    #código de inicialização de toda classe Sprite do pygame
    def __init__(self):
        #inicializar sprite
        pygame.sprite.Sprite.__init__(self)

        self.stepCounter = 0

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
        self.rect[0] = 32
        #Desenhar o pássaro na metade da tela. o [1] se refere a posição Y
        self.rect[1] = 112

    def update(self):

        #Colisão com as paredes
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
        if control[pygame.K_x] or control[pygame.K_z]:
           self.interact()

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

    def interact(self):

        #Nota da mesa
        if 102 <= self.rect[0] <= 142 and 157 <= self.rect[1] <= 162:
            speak('note')

        #cama
        if 107 <= self.rect[1] <= 142:
            if 62 <= self.rect[0] <= 72:
                print('É uma cama')
            elif self.rect[0] < 62:
                print('Voltar a dormir?')

        #planta
        if self.rect[0] <= 57:
            if 192 <= self.rect[1] <= 232:
                print('Plant!')

        #Armário
        if self.rect[1] <= 212:
            if 217 <= self.rect[0] <= 272:
                print('Armário!')

        #Cofre
        if self.rect[1] <= 212:
            if 187 <= self.rect[0] <= 216:
                print('Cofre!')

        #Janela
        if self.rect[1] <= 77:
            if 207 <= self.rect[0] <= 272:
                print('Janela!')

        #ExitDoor
        if self.rect[1] <= 67:
            if 117 <= self.rect[0] <= 172:
                print('A porta está trancada')
        
class Object(pygame.sprite.Sprite):

    def __init__(self, path, positionX, positionY, colision = True, scale = True):
        pygame.sprite.Sprite.__init__(self)
        image = Image.open(path)
        self.image = pygame.image.load(path)
        if scale:
            self.image = pygame.transform.scale(self.image, ((2 * image.width), (2 * image.height)))
            self.hitbox = pygame.Rect(positionX, positionY, 2 * image.width - 8, 2 * image.height - 8)
        else:
            self.hitbox = pygame.Rect(positionX, positionY, image.width - 8, image.height - 8)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = positionX
        self.rect[1] = positionY    
        pygame.draw.rect(screen, (0, 0, 0, 0), self.hitbox)
        self.colision = colision

    def update(self):
        if self.colision:
            if self.hitbox.colliderect(protag):
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

def pictureUpdate(num):
    pictures = [
        'assets/objects/picture1.png',
        'assets/objects/picture2.png',
        'assets/objects/picture3.png',
        'assets/objects/picture4.png',
        'assets/objects/picture5.png',
        'assets/objects/picture6.png'
    ]

    picture = Object(pictures[num], 32, 25)

    # if protag.stepCounter >= GAME_TIMER:
    #     picture = Object(pictures[1], 32, 25)
    #     #TO DO talvez fazer isso
    #     # BACKGROUND = pygame.image.load('assets/roomDark.png')
    #     # screen.blit(BACKGROUND, (-32,-20))

    # if protag.stepCounter >= 2 * GAME_TIMER:
    #     picture = Object(pictures[2], 32, 25)
    
    # if protag.stepCounter >= 3 * GAME_TIMER:
    #     picture = Object(pictures[3], 32, 25)

    # if protag.stepCounter >= 4 * GAME_TIMER:
    #     picture = Object(pictures[4], 32, 25)

    # if protag.stepCounter >= 5 * GAME_TIMER:
    #     picture = Object(pictures[5], 32, 25)
        #Dar game over aqui
        # BACKGROUND = pygame.image.load('assets/roomDark.png')

    object_group.add(picture)

def createWalls():

    Walls = [
        pygame.Rect(0, 0, SCREEN_WIDTH, 56),
        pygame.Rect(0, 0, 24, SCREEN_HEIGHT),
        pygame.Rect(SCREEN_WIDTH - 24, 0, 24, SCREEN_HEIGHT),
        pygame.Rect(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 24),
    ]

    #Criar paredes
    for i in range(4):
        pygame.draw.rect(screen, (255,0,0), Walls[i])

def speak(obj):
    speakBubble = Object('assets/speakBubble.png', SCREEN_WIDTH / 2 - 140, SCREEN_HEIGHT - 100, False, False)
    object_over.add(speakBubble)

    if obj == 'note':
        message = 'Encontre a chave antes que seja tarde...'

    print(message)

    text = font.render(message, 1, (0, 0, 0))
    screen.blit(text, speakBubble)
    
# Inicializador do jogo
pygame.init()

#Fontes
pygame.font.init()
font = pygame.font.SysFont('assets/fonts/pixelated.ttf', FONT_SIZE)

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
bed = Object('assets/objects/bed.png', 32, 112, False)
window = Object('assets/objects/window.png', 220, 16)
table = Object('assets/objects/table.png', SCREEN_WIDTH / 2 - 48, SCREEN_HEIGHT / 2 - 24)
chair2 = Object('assets/objects/chair2.png', 260, 200, False)
carpet = Object('assets/objects/carpet.png', SCREEN_WIDTH / 2 - 48, 72, False)
carpet2 = Object('assets/objects/carpet.png', 200, 210, False)
books = Object('assets/objects/books.png', 232, 152)
pot = Object('assets/objects/pot.png', 32, 230)
safe = Object('assets/objects/safe.png', 200, 152)
exitDoor = Object('assets/objects/exitDoor.png', SCREEN_WIDTH / 2 - 32, 24)
object_group.add(window, carpet, carpet2, table, bed,  books, chair2, pot, safe, exitDoor)

object_over = pygame.sprite.Group()
plant = Object('assets/objects/plant.png', 32, 190, False)
sheets = Object('assets/objects/sheets.png', 32, 133, False)
chair = Object('assets/objects/chair.png', SCREEN_WIDTH / 2 + 8, 156, False)
object_over.add(sheets, plant, chair)

#fps
clock = pygame.time.Clock()
createWalls()
pictureUpdate(0)

while True:
    #definir fps no jogo
    clock.tick(FPS)

    #Loop básico
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        
    if protag.stepCounter == GAME_TIMER:
        pictureUpdate(1)

    if protag.stepCounter == 2 * GAME_TIMER:
        pictureUpdate(2)

    if protag.stepCounter == 3 * GAME_TIMER:
        pictureUpdate(3)

    if protag.stepCounter == 4 * GAME_TIMER:
        pictureUpdate(4)

    if protag.stepCounter == 5 * GAME_TIMER:
        pictureUpdate(5)

    #Criar Background
    screen.blit(BACKGROUND, (-32,-20))

    object_group.update()
    object_group.draw(screen)

    protag_group.update()
    protag_group.draw(screen)

    object_over.update()
    object_over.draw(screen)

    if False:
        #O jogo acaba
        break

    pygame.display.update()
