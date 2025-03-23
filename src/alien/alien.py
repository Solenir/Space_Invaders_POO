
from pygame import *
from helpers import constants

'''
    Representa um alienígena no jogo, que pode alternar entre duas imagens.
    Cada alienígena possui uma linha e uma coluna, além de uma referência ao jogo.
'''
class Alien(sprite.Sprite):
    def __init__(self, row, column, game):
        sprite.Sprite.__init__(self)
        self.row = row
        self.column = column
        self.images = []  # Lista para armazenar as imagens do alienígena
        self._load_images()  # Carrega as imagens para animação
        self.index = 0 # Índice da imagem atual
        self.image = self.images[self.index] # Define a imagem inicial
        self.rect = self.image.get_rect() # Referência ao objeto do jogo
        self.game = game

    
    def _toggle_image(self):
        """Alterna entre as imagens do alienígena para criar um efeito de animação."""
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0 # Retorna ao início se ultrapassar o limite
        self.image = self.images[self.index]  # Atualiza a imagem
   
    def update(self, *args):
        """
        Função responsável por atualizar a posição e exibe a imagem na tela do jogo.        
        Essa função é chamada a cada frame para redesenhar o alienígena.
        """
        self.game.screen.blit(self.image, self.rect)

    
    def _load_images(self):
        """
        Função responsável por carregar as imagens dos alienígenas com base na linha da formação.
        Cada alienígena tem duas imagens alternadas para criar um efeito de movimento.
        """
        images = {0: ['1_2', '1_1'],
                  1: ['2_2', '2_1'],
                  2: ['2_2', '2_1']
                  }
        # Obtém as imagens correspondentes à linha do alienígena
        img1, img2 = [constants.IMAGES[f'alien{img_num}'] for img_num in images[self.row]]

        # Redimensiona e armazena as imagens
        self.images.append(transform.scale(img1, (40, 35)))
        self.images.append(transform.scale(img2, (40, 35)))