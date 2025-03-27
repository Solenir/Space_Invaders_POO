from pygame import sprite, Surface

class Blocker(sprite.Sprite):
    """
    Classe que representa um bloco de barreira no jogo, usado para proteger o jogador.

    Atributos:
        height (int): Altura do bloco em pixels
        width (int): Largura do bloco em pixels
        color (tuple): Cor do bloco no formato RGB (ex: (255, 0, 0))
        image (Surface): Superfície visual do bloco
        rect (Rect): Retângulo que define posição e área do bloco
        row (int): Linha da grade onde o bloco está posicionado
        column (int): Coluna da grade onde o bloco está posicionado
        game (object): Referência ao objeto principal do jogo
    """

    def __init__(self, size, color, row, column, game):
        """
        Inicializa um bloco de barreira com propriedades básicas.

        Args:
            size (int): Tamanho do bloco (altura e largura iguais)
            color (tuple): Cor do bloco no formato RGB
            row (int): Posição na linha da grade de barreiras
            column (int): Posição na coluna da grade de barreiras
            game (object): Referência ao objeto do jogo principal
        """
        super().__init__()  # Inicializa a classe base Sprite

        # Define dimensões e cor do bloco
        self.height = size
        self.width = size
        self.color = color

        # Cria a superfície visual do bloco
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)

        # Define a área e posição do bloco
        self.rect = self.image.get_rect()

        # Armazena posição na grade e referência do jogo
        self.row = row
        self.column = column
        self.game = game

    def update(self, keys=None, *args):
        """
        Atualiza o bloco a cada frame, desenhando-o na tela.

        Args:
            keys (dict, optional): Estado das teclas pressionadas (não utilizado)
            *args: Argumentos variáveis para compatibilidade
        """
        # Desenha o bloco na sua posição atual
        self.game.screen.blit(self.image, self.rect)