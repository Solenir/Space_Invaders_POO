from pygame import *
from helpers import constants

class Ship(sprite.Sprite):
    """
    Classe que representa a nave do jogador no jogo.
    Herda de pygame.sprite.Sprite para permitir funcionalidades de sprites.
    """
    
    def __init__(self, game, speed=4):
        """
        Inicializa a nave do jogador com configurações padrão.
        
        Parâmetros:
            game (object): Referência ao objeto principal do jogo
            speed (int): Velocidade de movimento da nave (padrão: 4)
        """
        sprite.Sprite.__init__(self)
        
        # Carrega a imagem da nave a partir das constantes do jogo
        self.image = constants.IMAGES['ship']
        
        # Define o retângulo de colisão e posição inicial
        # Posição inicial: x=385 (centralizado horizontalmente considerando uma tela de ~800px)
        # y=550 (próximo à parte inferior da tela)
        self.rect = self.image.get_rect(topleft=(385, 550))
        
        # Configura a velocidade de movimento da nave
        self.speed = speed
        
        # Armazena referência ao objeto do jogo principal
        self.game = game

    def update(self, keys, *args):
        """
        Atualiza o estado da nave a cada frame do jogo.
        Responsável por processar entrada do jogador e movimentação.
        
        Parâmetros:
            keys (list): Lista de estados das teclas pressionadas
            *args: Argumentos adicionais (não utilizados)
        """
        # Movimentação para a esquerda
        # Verifica se tecla esquerda está pressionada E se a nave não passou do limite esquerdo (10px)
        if keys[K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.speed  # Move a nave para esquerda
        
        # Movimentação para a direita
        # Verifica se tecla direita está pressionada E se a nave não passou do limite direito (740px)
        if keys[K_RIGHT] and self.rect.x < 740:
            self.rect.x += self.speed  # Move a nave para direita
        
        # Desenha a nave na tela do jogo
        # Utiliza a superfície de tela armazenada no objeto game principal
        self.game.screen.blit(self.image, self.rect)