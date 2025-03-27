from pygame import sprite, transform, time, mixer
from helpers import constants

class Mystery(sprite.Sprite):
    """
    Classe que representa a nave misteriosa  que aparece ocasionalmente no topo da tela.
    Herda de sprite.Sprite para integração com os grupos de sprites do Pygame.

    Atributos:
        image (Surface): Imagem redimensionada da nave misteriosa
        rect (Rect): Área e posição da nave na tela
        row (int): Linha fixa onde a nave se move (normalmente no topo)
        move_time (int): Intervalo de tempo entre movimentos (em ms)
        direction (int): Direção do movimento (1 = direita, -1 = esquerda)
        timer (int): Momento do último movimento
        sound (Sound): Efeito sonoro quando a nave aparece
        play_sound (bool): Flag para controlar a reprodução do som
        game (object): Referência ao objeto principal do jogo
    """

    def __init__(self, game):
        """
        Inicializa a nave misteriosa com suas propriedades básicas.

        Args:
            game (object): Referência ao objeto principal do jogo
        """
        super().__init__()  # Inicializa a classe base Sprite

        # Configuração visual
        self.image = transform.scale(constants.IMAGES['mystery'], (75, 35))
        self.rect = self.image.get_rect(topleft=(-80, 45))  # Posição inicial fora da tela
        self.row = 5  # Linha fixa de movimento (topo)

        # Configuração de movimento
        self.move_time = 25000  # 25 segundos entre aparições
        self.direction = 1  # Começa movendo para a direita
        self.timer = time.get_ticks()  # Inicia o temporizador

        # Configuração de áudio
        self.sound = mixer.Sound(constants.SOUND_PATH + 'mysteryentered.wav')
        self.sound.set_volume(0.3)  # Volume reduzido
        self.play_sound = True  # Permite tocar o som na próxima entrada

        # Referência do jogo
        self.game = game

    def update(self, keys, current_time, *args):
        """
        Atualiza o estado da nave misteriosa a cada frame.

        Args:
            keys (dict): Estado das teclas pressionadas (não utilizado)
            current_time (int): Tempo atual do jogo em milissegundos
            *args: Argumentos variáveis para compatibilidade
        """
        elapsed_time = current_time - self.timer
        reset_timer = False

        # Só começa a mover após o tempo de espera
        if elapsed_time > self.move_time:
            self._handle_movement(current_time)
            reset_timer = self._check_boundaries(current_time)

        # Reinicia o temporizador se necessário
        if elapsed_time > self.move_time and reset_timer:
            self.timer = current_time

    def _handle_movement(self, current_time):
        """
        Controla o movimento da nave misteriosa e a reprodução do som.

        Args:
            current_time (int): Tempo atual do jogo em milissegundos
        """
        # Toca o som quando a nave entra na tela
        if (self.rect.x < 0 or self.rect.x > 800) and self.play_sound:
            self.sound.play()
            self.play_sound = False

        # Movimento para a direita
        if self.rect.x < 840 and self.direction == 1:
            self.sound.fadeout(4000)  # Fadeout do som
            self.rect.x += 2  # Velocidade de movimento
            self.game.screen.blit(self.image, self.rect)

        # Movimento para a esquerda
        if self.rect.x > -100 and self.direction == -1:
            self.sound.fadeout(4000)  # Fadeout do som
            self.rect.x -= 2  # Velocidade de movimento
            self.game.screen.blit(self.image, self.rect)

    def _check_boundaries(self, current_time):
        """
        Verifica se a nave atingiu os limites da tela e precisa inverter direção.

        Args:
            current_time (int): Tempo atual do jogo em milissegundos

        Returns:
            bool: True se o temporizador precisa ser resetado, False caso contrário
        """
        reset_timer = False
        
        # Saiu pelo lado direito
        if self.rect.x > 830:
            self.play_sound = True
            self.direction = -1  # Inverte para esquerda
            reset_timer = True

        # Saiu pelo lado esquerdo
        elif self.rect.x < -90:
            self.play_sound = True
            self.direction = 1  # Inverte para direita
            reset_timer = True

        return reset_timer