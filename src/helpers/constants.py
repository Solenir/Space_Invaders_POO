import os
from pygame import *

# Configura caminhos de acesso aos diretórios das fontes, imagens e sons utilizados
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FONT_PATH = BASE_PATH + '\\assets\\fonts\\'
IMAGE_PATH = BASE_PATH + '\\assets\\images\\'
SOUND_PATH = BASE_PATH + '\\assets\\sounds\\'

# Configura as cores utilizadas no jogo (R, G, B)
WHITE_COLOR = (255, 255, 255)
GREEN_COLOR = (78, 255, 87)
PURPLE_COLOR = (203, 0, 255)
RED_COLOR = (237, 28, 36)

# Configura o tamanho da tela que o jogo será executado
SCREEN = display.set_mode((800, 600))
FONT = FONT_PATH + 'space_invaders_game.ttf'
IMG_NAMES = ['ship', 'mystery',
             'alien1_1', 'alien1_2',
             'alien2_1', 'alien2_2',
             'explosionpurple', 'explosiongreen',
             'laser', 'enemylaser']
IMAGES = {name: image.load(IMAGE_PATH + '{}.png'.format(name)).convert_alpha()
          for name in IMG_NAMES}

# Configura a posição inicial de alguns componentes do jogo
BLOCKERS_POSITION = 440
ENEMY_DEFAULT_POSITION = 60 
ENEMY_MOVE_DOWN = 30
