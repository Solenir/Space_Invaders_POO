from pygame import *
from helpers import constants


''' Esta classe é responsável por representar as vidas disponíveis no
jogo Space Invaders
'''

class Life(sprite.Sprite):
    def __init__(self, xpos, ypos, game):
        sprite.Sprite.__init__(self)
        # Carrega a imagem do sprite a partir dos recursos do jogo
        self.image = constants.IMAGES['ship']
        # Redimensiona a imagem para um tamanho fixo de 25x25 pixels
        self.image = transform.scale(self.image, (25, 25))
        # Define o retângulo de colisão e posiciona no local especificado
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
        # Mantém uma referência ao jogo para poder acessar a tela
        self.game = game
    
    """
    Função responsável por atualizar a posição e exibir a imagem na tela do jogo.
    Esse método é chamado a cada frame para redesenhar o sprite.
    """
    def update(self, *args):
        self.game.screen.blit(self.image, self.rect)