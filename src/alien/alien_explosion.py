from pygame import sprite, transform, time
from helpers import constants

class AlienExplosion(sprite.Sprite):
    """
    Classe responsável por modelar a explosão de um alienígena quando ele é atingido por uma bala.
    
    Atributos:
        image (Surface): Primeira imagem da explosão (menor).
        image2 (Surface): Segunda imagem da explosão (maior).
        rect (Rect): Área e posição da explosão na tela.
        timer (int): Momento em que a explosão foi criada (em milissegundos).
        game (object): Referência ao objeto do jogo.
    """

    def __init__(self, game, alien, *groups):
        """
        Inicializa a explosão do alienígena.
        
        :param game: Referência ao objeto do jogo.
        :param alien: Alienígena que foi atingido e explodiu.
        :param groups: Grupos aos quais a explosão pertence.
        """
        super().__init__(*groups)  # Inicializa a classe base (sprite.Sprite)

        # Carrega as imagens da explosão com base na linha do alienígena
        self.image = transform.scale(self._get_explosion_image(alien.row), (40, 35))  # Imagem menor
        self.image2 = transform.scale(self._get_explosion_image(alien.row), (50, 45))  # Imagem maior

        # Define a posição da explosão com base na posição do alienígena
        self.rect = self.image.get_rect(topleft=(alien.rect.x, alien.rect.y))

        # Configura o timer para controlar a duração da explosão
        self.timer = time.get_ticks()

        # Referência ao objeto do jogo
        self.game = game

    @staticmethod
    def _get_explosion_image(row):
        """
        Retorna a imagem da explosão com base na linha do alienígena.
        
        :param row: Linha do alienígena (usada para determinar a cor da explosão).
        :return: Imagem da explosão correspondente.
        """
        # Define as cores das explosões com base na linha do alienígena
        explosion_colors = ['purple', 'green', 'green']
        return constants.IMAGES[f'explosion{explosion_colors[row]}']

    def update(self, current_time, *args):
        """
        Atualiza a explosão na tela com base no tempo atual.
        
        :param current_time: Tempo atual do jogo (em milissegundos).
        """
        elapsed_time = current_time - self.timer  # Calcula o tempo decorrido desde o início da explosão

        # Remove a explosão após 400 milissegundos
        if elapsed_time > 400:
            self.kill()
            return

        # Alterna entre as duas imagens da explosão com base no tempo decorrido
        if elapsed_time <= 100:
            image = self.image  # Usa a imagem menor nos primeiros 100 ms
            position = self.rect.topleft  # Mantém a posição original
        else:
            image = self.image2  # Usa a imagem maior após 100 ms
            position = (self.rect.x - 6, self.rect.y - 6)  # Ajusta a posição para centralizar a imagem maior

        # Desenha a explosão na tela
        self.game.screen.blit(image, position)