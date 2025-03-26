from pygame import sprite, transform
from helpers import constants

class Life(sprite.Sprite):
    """
    Classe que representa uma vida extra do jogador na interface.

    Atributos:
        image (Surface): Imagem redimensionada da nave do jogador.
        rect (Rect): Área e posição da vida na tela.
        game (object): Referência ao objeto principal do jogo.
    """

    def __init__(self, xpos, ypos, game):
        """
        Inicializa um indicador de vida extra.

        Args:
            xpos (int): Posição horizontal inicial.
            ypos (int): Posição vertical inicial.
            game (object): Referência ao objeto do jogo principal.
        """
        super().__init__()  
        # Carrega e redimensiona a imagem da nave
        self.image = transform.scale(
            constants.IMAGES['ship'],  # Imagem original da nave
            (25, 25)  # Dimensões desejadas
        )

        # Define a posição do indicador de vida
        self.rect = self.image.get_rect(topleft=(xpos, ypos))

        # Referência ao jogo principal para acesso à tela
        self.game = game

    def update(self, *args):
        """
        Atualiza a exibição da vida na tela.
        
        Args:
            *args: Argumentos variáveis (compatibilidade com sprite.Group)
        """
        # Renderiza a imagem na posição atual
        self.game.screen.blit(self.image, self.rect)