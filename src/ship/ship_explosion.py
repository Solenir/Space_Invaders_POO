from pygame import *
from helpers import constants

class ShipExplosion(sprite.Sprite):
    """
    Classe que representa a animação de explosão da nave do jogador.
    Herda de pygame.sprite.Sprite para funcionalidades básicas de sprites.
    
    Controla a exibição temporizada da explosão e sua remoção automática.
    """
    
    def __init__(self, game, ship, *groups):
        """
        Inicializa a explosão da nave.
        
        Parâmetros:
            game (object): Referência ao objeto principal do jogo
            ship (Ship): Objeto da nave que está explodindo
            *groups: Grupos de sprites aos quais esta explosão deve pertencer
        """
        super(ShipExplosion, self).__init__(*groups)
        
        # Usa a mesma imagem da nave para a explosão (considerar trocar por imagem de explosão)
        self.image = constants.IMAGES['ship']
        
        # Posiciona a explosão no mesmo local da nave
        self.rect = self.image.get_rect(topleft=(ship.rect.x, ship.rect.y))
        
        # Marca o tempo inicial para controle da animação
        self.timer = time.get_ticks()
        
        # Referência ao jogo principal para acesso à tela
        self.game = game

    def update(self, current_time, *args):
        """
        Atualiza o estado da explosão a cada frame.
        Controla a exibição temporizada e remove a explosão quando completa.
        
        Parâmetros:
            current_time (int): Tempo atual do jogo em milissegundos
            *args: Argumentos adicionais (não utilizados)
        """
        # Calcula quanto tempo passou desde o início da explosão
        elapsed_time = current_time - self.timer
        
        # Fase 1: Exibe a explosão entre 300ms e 600ms (0.3s a 0.6s)
        if 300 < elapsed_time <= 600:
            self.game.screen.blit(self.image, self.rect)
        
        # Fase 2: Remove a explosão após 900ms (0.9s)
        elif elapsed_time > 900:
            self.kill()  # Remove o sprite de todos os grupos