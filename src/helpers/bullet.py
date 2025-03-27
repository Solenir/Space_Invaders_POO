from pygame import sprite
from helpers import constants

class Bullet(sprite.Sprite):
    """
    Classe que representa um projétil no jogo, podendo ser tanto do jogador quanto de inimigos.

    Atributos:
        image (Surface): Imagem visual do projétil
        rect (Rect): Área e posição do projétil na tela
        speed (int): Velocidade de movimento do projétil
        direction (int): Direção do movimento (1 para baixo, -1 para cima)
        side (str): Origem do projétil ('player' ou 'enemy')
        filename (str): Nome do arquivo de imagem usado
        game (object): Referência ao objeto principal do jogo
    """

    def __init__(self, xpos, ypos, direction, speed, filename, side, game):
        """
        Inicializa um projétil com suas propriedades básicas.

        Args:
            xpos (int): Posição horizontal inicial
            ypos (int): Posição vertical inicial
            direction (int): Direção do movimento (1 ou -1)
            speed (int): Velocidade do projétil
            filename (str): Chave para a imagem no dicionário constants.IMAGES
            side (str): Identificador de origem ('player' ou 'enemy')
            game (object): Referência ao objeto do jogo principal
        """
        super().__init__()  # Inicializa a classe base Sprite

        # Configuração visual do projétil
        self.image = constants.IMAGES[filename]
        self.rect = self.image.get_rect(topleft=(xpos, ypos))

        # Propriedades de movimento
        self.speed = speed
        self.direction = direction

        # Identificação e controle
        self.side = side
        self.filename = filename
        self.game = game

    def update(self, keys=None, *args):
        """
        Atualiza o estado do projétil a cada frame.

        Args:
            keys (dict, optional): Estado das teclas pressionadas (para projéteis do jogador)
            *args: Argumentos variáveis para compatibilidade
        """
        # 1. Renderiza o projétil na tela
        self.game.screen.blit(self.image, self.rect)
        
        # 2. Move o projétil na direção especificada
        self.rect.y += self.speed * self.direction
        
        # 3. Verifica se saiu dos limites da tela
        self._check_boundaries()

    def _check_boundaries(self):
        """
        Verifica se o projétil saiu dos limites da tela e deve ser removido.
        Método interno para encapsular a lógica de verificação.
        """
        screen_height = self.game.screen.get_height()
        if self.rect.y < 15 or self.rect.y > screen_height:
            self.kill()  # Remove o projétil do grupo ao qual pertence