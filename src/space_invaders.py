from pygame import *
from helpers import constants
from helpers.text import Text
from helpers.life import Life
from helpers.blocker import Blocker
from helpers.bullet import Bullet
from alien.alien import Alien
from alien.alien_explosion import AlienExplosion
from alien.alien_group import AliensGroup
from mystery.mystery import Mystery
from mystery.mystery_explosion import MysteryExplosion
from ship.ship import Ship
from ship.ship_explosion import ShipExplosion
from random import choice
import sys

class SpaceInvaders(object):
    """
    Classe principal do jogo Space Invaders.
    Controla toda a lógica do jogo, incluindo:
    - Inicialização do jogo
    - Gerenciamento de estados (menu, jogo, game over)
    - Controle de sprites e colisões
    - Sistema de pontuação e vidas
    """
    
    def __init__(self, frequency, size, channels, buffer):
        """
        Inicializa o jogo com configurações de áudio e prepara os recursos iniciais.
        
        Parâmetros:
            frequency (int): Taxa de amostragem do áudio
            size (int): Tamanho do buffer de áudio
            channels (int): Número de canais de áudio
            buffer (int): Tamanho do buffer de áudio
        """
        # Configuração inicial do mixer de áudio
        mixer.pre_init(frequency, size, channels, buffer)
        init()
        
        # Configurações básicas do jogo
        self.clock = time.Clock()
        self.screen = constants.SCREEN
        
        # Carrega imagens de fundo
        self.welcome_screen = image.load(constants.IMAGE_PATH + 'welcome.png').convert()
        self.background = image.load(constants.IMAGE_PATH + 'background.jpg').convert()
        
        # Estados do jogo
        self.start_game = False
        self.main_screen = True
        self.game_over = False
        
        # Configurações iniciais
        self.enemy_position = constants.ENEMY_DEFAULT_POSITION
        
        # Elementos de texto da interface
        self._setup_text_elements()
        
        # Sistema de vidas
        self._setup_lives_system()
        
    def _setup_text_elements(self):
        """Configura todos os elementos de texto usados no jogo."""
        self.welcome_text = Text(constants.FONT, 50, 'Bem-vindo(a)', constants.WHITE_COLOR, 190, 300)
        self.title_text2 = Text(constants.FONT, 25, 'Presione qualquer tecla para continuar', 
                             constants.WHITE_COLOR, 80, 400)
        self.game_over_text = Text(constants.FONT, 50, 'Fim do Jogo!', constants.WHITE_COLOR, 250, 270)
        self.next_round_text= Text(constants.FONT, 50, 'Proxima rodada', constants.WHITE_COLOR, 240, 270)
        self.score_text = Text(constants.FONT, 20, 'Score', constants.WHITE_COLOR, 5, 5)
        self.lives_text = Text(constants.FONT, 20, 'Vidas ', constants.WHITE_COLOR, 610, 5)
    
    def _setup_lives_system(self):
        """Configura o sistema de vidas do jogador."""
        self.life1 = Life(690, 3, self)
        self.life2 = Life(710, 3, self)
        self.life3 = Life(730, 3, self)
        self.life4 = Life(750, 3, self)
        self.lives_group = sprite.Group(self.life1, self.life2, self.life3, self.life4)

    def reset(self, score):
        """
        Reinicia o jogo com um novo estado, mantendo a pontuação se for uma nova rodada.
        
        Parâmetros:
            score (int): Pontuação atual a ser mantida
        """
        # Configuração do jogador
        self.player = Ship(self)
        self.player_group = sprite.Group(self.player)
        
        # Grupos de sprites
        self.explosions_group = sprite.Group()
        self.bullets = sprite.Group()
        self.enemy_bullets = sprite.Group()
        
        # Inimigos e elementos especiais
        self.mystery_ship = Mystery(self)
        self.mystery_group = sprite.Group(self.mystery_ship)
        self.make_enemies()
        
        # Grupo com todos os sprites
        self.all_sprites = sprite.Group(self.player, self.enemies,
                                      self.lives_group, self.mystery_ship)
        
        # Controles e temporizadores
        self.keys = key.get_pressed()
        self.timer = time.get_ticks()
        self.note_timer = time.get_ticks()
        self.ship_timer = time.get_ticks()
        
        # Estado do jogo
        self.score = score
        self.create_audio()
        self.make_new_ship = False
        self.ship_alive = True

    def make_blockers(self, number):
        """
        Cria barreiras de proteção para o jogador.
        
        Parâmetros:
            number (int): Índice da barreira (0-3)
            
        Retorna:
            sprite.Group: Grupo contendo os blocos da barreira
        """
        blocker_group = sprite.Group()
        for row in range(4):
            for column in range(9):
                blocker = Blocker(10, constants.GREEN_COLOR, row, column, self)
                blocker.rect.x = 50 + (200 * number) + (column * blocker.width)
                blocker.rect.y = constants.BLOCKERS_POSITION + (row * blocker.height)
                blocker_group.add(blocker)
        return blocker_group

    def create_audio(self):
        """Configura todos os efeitos sonoros e músicas do jogo."""
        self.sounds = {}
        for sound_name in ['shoot', 'shoot2', 'invader_killed', 'mystery_killed',
                         'ship_explosion']:
            self.sounds[sound_name] = mixer.Sound(
                constants.SOUND_PATH + '{}.wav'.format(sound_name))
            self.sounds[sound_name].set_volume(0.2)

        self.music_notes = [mixer.Sound(constants.SOUND_PATH + '{}.wav'.format(i)) for i
                         in range(4)]
        for sound in self.music_notes:
            sound.set_volume(0.5)

        self.note_index = 0

    def play_main_music(self, current_time):
        """
        Toca as notas musicais características do jogo de forma sequencial.
        
        Parâmetros:
            current_time (int): Tempo atual do jogo em milissegundos
        """
        if current_time - self.note_timer > self.enemies.move_time:
            self.note = self.music_notes[self.note_index]
            if self.note_index < 3:
                self.note_index += 1
            else:
                self.note_index = 0

            self.note.play()
            self.note_timer += self.enemies.move_time

    @staticmethod
    def should_exit(evt):
        """
        Verifica se o evento deve encerrar o jogo.
        
        Parâmetros:
            evt (Event): Evento do pygame a ser verificado
            
        Retorna:
            bool: True se o evento deve encerrar o jogo
        """
        return evt.type == QUIT or (evt.type == KEYUP and evt.key == K_ESCAPE)

    def check_input(self):
        """Verifica e processa todas as entradas do jogador."""
        self.keys = key.get_pressed()
        for e in event.get():
            if self.should_exit(e):
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    self._handle_shooting()

    def _handle_shooting(self):
        """Controla a lógica de disparo do jogador."""
        if len(self.bullets) == 0 and self.ship_alive:
            if self.score < 1000:
                # Tiro único para pontuação baixa
                bullet = Bullet(self.player.rect.x + 23,
                              self.player.rect.y + 5, -1,
                              15, 'laser', 'center', self)
                self.bullets.add(bullet)
                self.all_sprites.add(self.bullets)
                self.sounds['shoot'].play()
            else:
                # Tiros duplos como recompensa por alta pontuação
                left_bullet = Bullet(self.player.rect.x + 8,
                                  self.player.rect.y + 5, -1,
                                  15, 'laser', 'left', self)
                right_bullet = Bullet(self.player.rect.x + 38,
                                   self.player.rect.y + 5, -1,
                                   15, 'laser', 'right', self)
                self.bullets.add(left_bullet)
                self.bullets.add(right_bullet)
                self.all_sprites.add(self.bullets)
                self.sounds['shoot2'].play()

    def make_enemies(self):
        """Cria o grupo de inimigos na formação inicial."""
        enemies = AliensGroup(10, 3, self)
        for row in range(3):
            for column in range(10):
                enemy = Alien(row, column, self)
                enemy.rect.x = 157 + (column * 50)
                enemy.rect.y = self.enemy_position + (row * 45)
                enemies.add(enemy)

        self.enemies = enemies

    def make_enemies_shoot(self):
        """Faz com que os inimigos atirem aleatoriamente."""
        if (time.get_ticks() - self.timer) > 700 and self.enemies:
            enemy = self.enemies.random_bottom_alien()
            self.enemy_bullets.add(
                Bullet(enemy.rect.x + 14, enemy.rect.y + 20, 1, 5,
                     'enemylaser', 'center', self))
            self.all_sprites.add(self.enemy_bullets)
            self.timer = time.get_ticks()

    def calculate_score(self, row):
        """
        Calcula a pontuação obtida ao destruir um inimigo.
        
        Parâmetros:
            row (int): Linha do inimigo destruído (determina a pontuação)
            
        Retorna:
            int: Pontuação obtida
        """
        scores = {0: 30,
                 1: 20,
                 2: 20,
                 5: choice([50, 100, 150, 300])  # Nave especial tem pontuação variável
                }

        score = scores[row]
        self.score += score
        return score

    def check_collisions(self):
        """Verifica e processa todas as colisões entre os elementos do jogo."""
        # Colisão entre tiros do jogador e inimigos
        sprite.groupcollide(self.bullets, self.enemy_bullets, True, True)

        # Jogador acertou inimigo comum
        for enemy in sprite.groupcollide(self.enemies, self.bullets, True, True).keys():
            self.sounds['invader_killed'].play()
            self.calculate_score(enemy.row)
            AlienExplosion(self, enemy, self.explosions_group)
            self.game_timer = time.get_ticks()

        # Jogador acertou nave especial
        for mystery in sprite.groupcollide(self.mystery_group, self.bullets, True, True).keys():
            mystery.sound.stop()
            self.sounds['mystery_killed'].play()
            score = self.calculate_score(mystery.row)
            MysteryExplosion(self, mystery, score, self.explosions_group)
            newShip = Mystery(self)          
            self.all_sprites.add(newShip)
            self.mystery_group.add(newShip)

        # Jogador foi atingido
        self._handle_player_hit()

        # Verifica se inimigos chegaram muito perto da base
        self._check_enemy_invasion()

        # Colisões com as barreiras de proteção
        sprite.groupcollide(self.bullets, self.all_blockers, True, True)
        sprite.groupcollide(self.enemy_bullets, self.all_blockers, True, True)
        if self.enemies.bottom >= constants.BLOCKERS_POSITION:
            sprite.groupcollide(self.enemies, self.all_blockers, False, True)

    def _handle_player_hit(self):
        """Processa quando o jogador é atingido por um tiro inimigo."""
        for player in sprite.groupcollide(self.player_group, self.enemy_bullets, True, True).keys():
            # Remove uma vida na sequência (da direita para esquerda)
            if self.life4.alive():
                self.life4.kill()
            elif self.life3.alive():
                self.life3.kill()
            elif self.life2.alive():
                self.life2.kill()
            elif self.life1.alive():
                self.life1.kill()           
            else:
                self.game_over = True
                self.start_game = False
                
            self.sounds['ship_explosion'].play()
            ShipExplosion(self, player, self.explosions_group)
            self.make_new_ship = True
            self.shipTimer = time.get_ticks()
            self.ship_alive = False

    def _check_enemy_invasion(self):
        """Verifica se os inimigos invadiram a área do jogador."""
        if self.enemies.bottom >= 540:
            sprite.groupcollide(self.enemies, self.player_group, True, True)
            if not self.player.alive() or self.enemies.bottom >= 600:
                self.game_over = True
                self.start_game = False

    def create_new_ship(self, createShip, current_time):
        """
        Cria uma nova nave para o jogador após ser destruída.
        
        Parâmetros:
            createShip (bool): Flag indicando se deve criar nova nave
            current_time (int): Tempo atual do jogo em milissegundos
        """
        if createShip and (current_time - self.shipTimer > 900):
            self.player = Ship(self)
            self.all_sprites.add(self.player)
            self.player_group.add(self.player)
            self.make_new_ship = False
            self.ship_alive = True

    def create_game_over(self, current_time):
        """
        Mostra a tela de game over com efeito de piscar.
        
        Parâmetros:
            current_time (int): Tempo atual do jogo em milissegundos
        """
        self.screen.blit(self.background, (0, 0))
        passed = current_time - self.timer
        
        # Efeito de piscar do texto "Game Over"
        if passed < 750:
            self.game_over_text.draw(self.screen)
        elif 750 < passed < 1500:
            self.screen.blit(self.background, (0, 0))
        elif 1500 < passed < 2250:
            self.game_over_text.draw(self.screen)
        elif 2250 < passed < 2750:
            self.screen.blit(self.background, (0, 0))
        elif passed > 3000:
            self.main_screen = True

        for e in event.get():
            if self.should_exit(e):
                sys.exit()

    def run(self):
        """Loop principal do jogo."""
        while True:
            if self.main_screen:
                self._show_main_menu()
            elif self.start_game:
                self._run_game_logic()
            elif self.game_over:
                self._handle_game_over()
                
            display.update()
            self.clock.tick(60)

    def _show_main_menu(self):
        """Exibe a tela principal do menu."""
        self.screen.blit(self.welcome_screen, (0, 0))
        self.welcome_text.draw(self.screen)               
        self.title_text2.draw(self.screen)
        
        for e in event.get():
            if self.should_exit(e):
                sys.exit()
            if e.type == KEYUP:
                # Cria as barreiras apenas em um novo jogo (não em nova rodada)
                self.all_blockers = sprite.Group(self.make_blockers(0),
                                              self.make_blockers(1),
                                              self.make_blockers(2),
                                              self.make_blockers(3))
                self.lives_group.add(self.life1, self.life2, self.life3, self.life4)
                self.reset(0)
                self.start_game = True
                self.main_screen = False

    def _run_game_logic(self):
        """Executa a lógica principal do jogo."""
        if not self.enemies and not self.explosions_group:
            # Fase concluída - prepara próxima rodada
            current_time = time.get_ticks()
            if current_time - self.game_timer < 3000:
                self._display_round_transition(current_time)
            if current_time - self.game_timer > 3000:
                # Move os inimigos mais para baixo na próxima rodada
                self.enemy_position += constants.ENEMY_MOVE_DOWN
                self.reset(self.score)
                self.game_timer += 3000
        else:
            # Jogo em andamento
            current_time = time.get_ticks()
            self.play_main_music(current_time)
            self.screen.blit(self.background, (0, 0))
            self._update_game_elements(current_time)

    def _display_round_transition(self, current_time):
        """Mostra a tela de transição entre rodadas."""
        self.screen.blit(self.background, (0, 0))
        self.score_text2 = Text(constants.FONT, 20, str(self.score),
                             constants.GREEN_COLOR, 85, 5)
        self.score_text.draw(self.screen)
        self.score_text2.draw(self.screen)
        self.next_round_text.draw(self.screen)
        self.lives_text.draw(self.screen)
        self.lives_group.update()
        self.check_input()

    def _update_game_elements(self, current_time):
        """Atualiza todos os elementos do jogo durante a partida."""
        self.all_blockers.update(self.screen)
        self.score_text2 = Text(constants.FONT, 20, str(self.score), constants.GREEN_COLOR,
                             85, 5)
        self.score_text.draw(self.screen)
        self.score_text2.draw(self.screen)
        self.lives_text.draw(self.screen)
        self.check_input()
        self.enemies.update(current_time)
        self.all_sprites.update(self.keys, current_time)
        self.explosions_group.update(current_time)
        self.check_collisions()
        self.create_new_ship(self.make_new_ship, current_time)
        self.make_enemies_shoot()

    def _handle_game_over(self):
        """Lida com a lógica de fim de jogo."""
        current_time = time.get_ticks()
        # Reseta a posição inicial dos inimigos
        self.enemy_position = constants.ENEMY_DEFAULT_POSITION
        self.create_game_over(current_time)


if __name__ == '__main__':
    # Inicializa o jogo com configurações de áudio padrão
    game = SpaceInvaders(44100, -16, 1, 4096)
    game.run()