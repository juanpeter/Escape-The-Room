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
        self.intBed = 0
        self.windowBroken = 0
        self.intPic = 0
        self.safeOpen = False
        self.hasKey = False

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
        i = 0
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

        #Note
        if 102 <= self.rect[0] <= 142:
            if 157 <= self.rect[1] <= 162:
                speak('note')

        #Bed
        if 107 <= self.rect[1] <= 142:
            if 62 <= self.rect[0] <= 72:
                speak('bed')
            elif self.rect[0] < 62:
                speak('bedInterior')
                if self.intBed <= 2:
                    self.intBed += 1

        #Plant
        if self.rect[0] <= 57:
            if 192 <= self.rect[1] <= 232:
                speak('plant')

        #Bookshelf
        if 212 <= self.rect[1]:
            if 217 <= self.rect[0] <= 272:
                speak('bookshelf')

        #Safe
        if self.rect[1] <= 212:
            if 187 <= self.rect[0] <= 216:
                if protag.safeOpen:
                    speak('safeOpen')
                    protag.hasKey = True
                    safeEmpty = Object('assets/objects/safeEmpty.png', 200, 152)
                    object_group.add(safeEmpty)
                else:
                    safePassword()

        #Window
        if self.rect[1] <= 77:
            if 207 <= self.rect[0] <= 272:
                if self.windowBroken <= 2:
                    speak('window')
                    self.windowBroken += 1
                elif self.windowBroken == 3:
                    windowBroken = Object('assets/objects/windowOpen.png', 204, 16)
                    object_group.remove(window)
                    object_group.add(windowBroken)
                    speak('window')
                    self.windowBroken += 1
                else:
                    speak('windowBroken')

        #Picture
        if 32 <= self.rect[0] <= 72:
            if 42 <= self.rect[1] <= 72:
                speak('picture')

        #ExitDoor
        if self.rect[1] <= 67:
            if 117 <= self.rect[0] <= 172:
                if protag.hasKey:
                    speak('openDoor')
                    doorOpen = Object('assets/objects/doorOpen.png', SCREEN_WIDTH / 2 - 48, 24)
                    object_group.remove(exitDoor)
                    object_group.add(doorOpen)
                else:
                    speak('exitDoor')
        
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

def pictureUpdate():
    if protag.intPic < 6:
        pictures = [
            'assets/objects/picture1.png',
            'assets/objects/picture2.png',
            'assets/objects/picture3.png',
            'assets/objects/picture4.png',
            'assets/objects/picture5.png',
            'assets/objects/picture6.png'
        ]

        picture = Object(pictures[protag.intPic], 32, 25)
        print(protag.intPic)

        object_group.add(picture)

def createWalls():

    Walls = [
        pygame.Rect(0, 0, SCREEN_WIDTH, 56),
        pygame.Rect(0, 0, 24, SCREEN_HEIGHT),
        pygame.Rect(SCREEN_WIDTH - 24, 0, 24, SCREEN_HEIGHT),
        pygame.Rect(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 24),
    ]
    i = 0
    #Criar paredes
    for i in range(4):
        pygame.draw.rect(screen, (255,0,0), Walls[i])

def speak(obj):
    speakBubble = Object('assets/speakBubble.png', SCREEN_WIDTH / 2 - 140, SCREEN_HEIGHT - 100, False, False)
    object_over.add(speakBubble)
    object_over.draw(screen)

    if obj == 'note':
        messages = [
            'PRIMEIRO VEM A ESCURIDÃO INFINITA,',
            'DEPOIS AS MÃOS DAQUELA QUE IMITA A VIDA,',
            'SEGUIDO DOS GUARDIÕES DO CONHECIMENTO,',
            'DECIFRE E ESCAPE.'
        ]

    if obj == 'bed':
        messages = [
            'ESSA NÃO É MINHA CAMA...',
            'COMO EU CHEGUEI AQUI?'
        ]
    if obj == 'bedInterior':
        messages = [
            'EU NÃO TENHO TEMPO PARA ISSO!',
            'ATÉ QUE ESSA CAMA É BEM CONFORTÁVEL...',
            'DORMIR UM POUCO NÃO FARIA MAL, CERTO?',
            '...'
        ]
        messages = [messages[protag.intBed]]

    if obj == 'plant':
        messages = [
            'É UMA PLANTA...DE PLÁSTICO',
            'ELA TEM 8 FOLHAS.'
        ]

    if obj == 'bookshelf':
        messages = [
            'UMA GRANDE ESTANTE CHEIA DE',
            'LIVROS...FALSOS?',
            'APENAS 4 LIVROS SÃO DE VERDADE...'
        ]
    
    if obj == 'window':
        messages = [
            'ESTÁ ESCURO FORA DA JANELA',
            '... ACHO QUE EU CONSIGO ABRI-LA!',
            '...',
            'CONSEGUI!'
        ]
        messages = [messages[protag.windowBroken]]

    if obj == 'windowBroken':
        messages = [
            'ESTA ESCURO LÁ FORA...',
            '?',
            'O NUMERO 3 ESTÁ ESCRITO NA BANCADA...'
        ]

    if obj == 'exitDoor':
        messages = [
            '...',
            'A PORTA ESTÁ TRANCADA!'
        ]
    if obj == 'openDoor':
        messages = [
            '...',
            'A PORTA ABRIU!'
        ]

    if obj == 'picture':
        messages = [
            '...ELA... PARECE COMIGO?',
            'ALGO ESTÁ ESQUISITO AQUI...',
            'ELA ESTÁ... CHORANDO?',
            'TINTA ESTÁ VAZANDO DO QUADRO!',
            '...EU... TENHO QUE SAIR AGORA!',
            'EU ESTOU COM UM PRESSENTIMENTO RUIM...'
        ]

        messages =[messages[protag.intPic]]

    if obj == 'safeOpen':
        messages = [
            'SERÁ QUE ESSA CHAVE ABRE A PORTA?',
            'EU TENHO QUE TENTAR!',
        ]

    speakBubble.center = ((SCREEN_WIDTH / 2 - 140), (SCREEN_HEIGHT - 72))
    i = 0
    for i in range(len(messages)):
        text = font.render(messages[i], 1, (1, 16, 28))
        speakBubble.center = ((32), ((SCREEN_HEIGHT - 92) + (13 * i)))
        screen.blit(text, (speakBubble.center))

    pygame.display.update()
    paused()
    object_over.remove(speakBubble)

def paused():
    pause = True
    while pause:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_x or event.type == pygame.K_z:
                    pause = False
    
def safePassword():

    PASSWORD = '384'
    ANSWER = ''
    NUMS = ['0','1','2','3','4','5','5','6','7','8', '9']

    passwordBubble = Object('assets/speakBubble.png', SCREEN_WIDTH / 2 - 140, SCREEN_HEIGHT / 2  - 72, False, False)
    object_over.add(passwordBubble)
    object_over.draw(screen)
    text = font.render('Isira uma senha', 1, (1, 16, 28))
    passwordBubble.center = ((SCREEN_WIDTH / 2 - font.size('insert password')[0]), ((SCREEN_HEIGHT / 2 - 40)))
    screen.blit(text, (passwordBubble.center))
    pygame.display.update()

    numbers = 0
    i = 0
    pause = True
    while pause:
        while numbers <= 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYUP:
                    for i in range(len(NUMS)):
                        if event.key == getattr(pygame,'K_'+ NUMS[i]):
                            ANSWER += NUMS[i]
                            numbers +=1
                            print(ANSWER)

        if ANSWER == PASSWORD:
            object_group.remove(safe)
            safeOpen = Object('assets/objects/safeOpen.png', 200, 152)
            object_group.add(safeOpen)
            pygame.display.update()
            protag.safeOpen = True

        else:
            print('Senha incorreta!')
            protag.intPic += 1
            pictureUpdate()
            numbers = 0
            ANSWER = ''
            print(numbers)

        pause = False

    object_over.remove(passwordBubble)

# Inicializador do jogo
pygame.init()

#Fontes
pygame.font.init()
font = pygame.font.SysFont('assets/fonts/gameboy.ttf', FONT_SIZE)

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
pictureUpdate()

while True:
    #definir fps no jogo
    clock.tick(FPS)

    #Loop básico
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_x or event.type == pygame.K_z:
                protag.interact()

    #Não funciona, não sei porque
    if protag.stepCounter + 1 % GAME_TIMER == 0 and protag.intPic < 6:
        protag.intPic += 1
        pictureUpdate()

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
