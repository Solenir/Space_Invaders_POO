from pygame import *

class Text:
    """
    Classe para renderização e exibição de texto na tela usando Pygame.
    
    Atributos:
        font (Font): Objeto de fonte do Pygame
        surface (Surface): Superfície contendo o texto renderizado
        rect (Rect): Retângulo que define a posição e área do texto
    """

    def __init__(self, textFont, size, message, color, xpos, ypos):
        """
        Inicializa o objeto de texto.

        Args:
            textFont (str): Caminho para o arquivo de fonte ou nome da fonte do sistema
            size (int): Tamanho da fonte em pixels
            message (str): Texto a ser exibido
            color (tuple): Cor do texto no formato RGB (ex: (255, 255, 255))
            xpos (int): Posição horizontal do texto
            ypos (int): Posição vertical do texto
        """
        # Inicializa a fonte com o arquivo e tamanho especificados
        self.font = font.Font(textFont, size)
        
        # Renderiza o texto na superfície
        self.surface = self.font.render(message, True, color)
        
        # Define a posição do texto na tela
        self.rect = self.surface.get_rect(topleft=(xpos, ypos))

    def draw(self, surface):
        """
        Desenha o texto na superfície especificada.

        Args:
            surface (Surface): Superfície do Pygame onde o texto será desenhado
        """
        surface.blit(self.surface, self.rect)

    def update_text(self, new_message, new_color=None):
        """
        Atualiza o texto exibido e opcionalmente sua cor.

        Args:
            new_message (str): Novo texto a ser exibido
            new_color (tuple, optional): Nova cor do texto. Mantém a atual se None.
        """
        color = new_color if new_color is not None else self.surface.get_at((0, 0))[:3]
        self.surface = self.font.render(new_message, True, color)
        # Mantém a posição original do retângulo
        original_pos = self.rect.topleft
        self.rect = self.surface.get_rect(topleft=original_pos)