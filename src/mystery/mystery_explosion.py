from pygame import sprite, time
from helpers import constants
from helpers.text import Text

class MysteryExplosion(sprite.Sprite):
    """
    Classe que representa a explosão/efeito visual quando um nabe é destruída.
    Antes de desaparecer mostra a pontuação obtida.

    Atributos:
        text (Text): Objeto de texto que mostra a pontuação
        timer (int): Momento em que a explosão foi criada (em milissegundos)
        game (object): Referência ao objeto principal do jogo
    """

    def __init__(self, game, mystery, score, *groups):
        """
        Inicializa o efeito de explosão do alienígena.

        Args:
            game (object): Referência ao objeto do jogo principal
            mystery (sprite.Sprite): alienígena que foi destruído
            score (int): Pontuação a ser exibida
            *groups: Grupos de sprites aos quais esta explosão será adicionada
        """
        super().__init__(*groups)  # Inicializa a classe base Sprite

        # Cria o texto que mostra a pontuação obtida
        self.text = Text(
            font=constants.FONT, 
            size=20, 
            message=str(score), 
            color=constants.WHITE,
            xpos=mystery.rect.x + 20,  # Centralizado horizontalmente
            ypos=mystery.rect.y + 6    # Centralizado verticalmente
        )

        # Configura o temporizador para controlar a animação
        self.timer = time.get_ticks()
        self.game = game

    def update(self, current_time, *args):
        """
        Atualiza a animação da explosão com base no tempo atual.

        Args:
            current_time (int): Tempo atual do jogo em milissegundos
            *args: Argumentos variáveis para compatibilidade
        """
        elapsed_time = current_time - self.timer

        # Animação de piscar (visível nos intervalos 0-200ms e 400-600ms)
        if elapsed_time <= 200 or 400 < elapsed_time <= 600:
            self.text.draw(self.game.screen)
        
        # Remove o efeito após 600ms
        elif elapsed_time > 600:
            self.kill()