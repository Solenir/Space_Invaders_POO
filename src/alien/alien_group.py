from pygame import sprite, time
from random import choice
from helpers import constants

class AliensGroup(sprite.Group):
    """
    Classe que gerencia um grupo de alienígenas no jogo.
    Herda de sprite.Group para permitir funcionalidades básicas de grupo de sprites.
    Essa classe controla movimentação, formação e comportamento dos alienígenas.
    """
    
    def __init__(self, columns, rows, game):
        """
        Inicializa o grupo de alienígenas.
        
        Args:
            columns (int): Número de colunas na formação de alienígenas
            rows (int): Número de linhas na formação
            game (object): Referência ao objeto do jogo principal
        """
        super().__init__()
        
        # Configuração da formação
        self.rows = rows
        self.columns = columns
        # Matriz que armazena referências a todos os alienígenas
        self.aliens = [[None for _ in range(columns)] for _ in range(rows)]
        
        # Controle de movimentação
        self.direction = 1  # 1=direita, -1=esquerda
        self.left_moves = 30  # Limite de movimentos para esquerda
        self.right_moves = 30  # Limite de movimentos para direita
        self.left_add_move = 0  # Movimentos extras para esquerda
        self.right_add_move = 0  # Movimentos extras para direita
        self.move_number = 15  # Contador de movimentos atuais
        self.move_time = 600  # Intervalo entre movimentos (ms)
        
        # Controle de tempo e posição
        self.timer = time.get_ticks()  # Último momento de movimento
        # Calcula a posição Y mais baixa da formação
        self.bottom = game.enemy_position + ((rows - 1) * 45) + 35
        
        # Controle de colunas ativas
        self.alive_columns = list(range(columns))  # Índices das colunas com aliens
        self.leftmost_alive_column = 0  # Coluna viva mais à esquerda
        self.rightmost_alive_column = columns - 1  # Coluna viva mais à direita

    def update(self, current_time):
        """
        Atualiza a posição dos alienígenas baseado no tempo.
        
        Args:
            current_time (int): Tempo atual do jogo em milissegundos
        """
        if current_time - self.timer > self.move_time:
            # Calcula o máximo de movimentos na direção atual
            max_move = (
                self.right_moves + self.right_add_move if self.direction == 1
                else self.left_moves + self.left_add_move
            )

            if self.move_number >= max_move:
                # Inverte direção e desce
                self._reverse_direction()
                self._move_down()
            else:
                # Move lateralmente
                self._move_laterally()

            self.timer += self.move_time  # Atualiza o tempo do último movimento

    def _reverse_direction(self):
        """Inverte a direção do movimento da frota."""
        self.direction *= -1
        self.move_number = 0
        # Ajusta os limites de movimento após inversão
        adjustment = self.right_add_move if self.direction == 1 else self.left_add_move
        self.left_moves = 30 + adjustment
        self.right_moves = 30 + adjustment

    def _move_down(self):
        """Move toda a frota para baixo e atualiza a posição inferior."""
        self.bottom = 0  # Reseta para recalcular
        for alien in self:
            alien.rect.y += constants.ENEMY_MOVE_DOWN
            alien._toggle_image()  # Animação do sprite
            # Atualiza a posição mais baixa da frota
            self.bottom = max(self.bottom, alien.rect.y + 35)

    def _move_laterally(self):
        """Move a frota na direção horizontal atual."""
        shift = 10 * self.direction  # Calcula deslocamento
        for alien in self:
            alien.rect.x += shift
            alien._toggle_image()  # Animação do sprite
        self.move_number += 1

    def add_internal(self, *sprites):
        """
        Adiciona alienígenas ao grupo e à matriz de controle.
        
        Args:
            *sprites: Um ou mais sprites de alienígenas para adicionar
        """
        super().add_internal(*sprites)
        for sprite in sprites:
            # Armazena referência na posição correta da matriz
            self.aliens[sprite.row][sprite.column] = sprite

    def remove_internal(self, *sprites):
        """
        Remove alienígenas do grupo e da matriz de controle.
        
        Args:
            *sprites: Um ou mais sprites de alienígenas para remover
        """
        super().remove_internal(*sprites)
        for sprite in sprites:
            self.kill(sprite)
        self.update_speed()  # Ajusta velocidade após remoção

    def is_column_dead(self, column):
        """
        Verifica se uma coluna está completamente vazia.
        
        Args:
            column (int): Índice da coluna a verificar
            
        Returns:
            bool: True se a coluna estiver vazia, False caso contrário
        """
        return not any(self.aliens[row][column] for row in range(self.rows))

    def random_bottom_alien(self):
        """
        Seleciona aleatoriamente um alienígena na base de uma coluna viva.
        
        Returns:
            object: O alienígena selecionado ou None se não houver aliens
        """
        if not self.alive_columns:
            return None
            
        column = choice(self.alive_columns)  # Escolhe coluna aleatória
        # Procura de baixo para cima na coluna
        for row in range(self.rows - 1, -1, -1):
            alien = self.aliens[row][column]
            if alien is not None:
                return alien
        return None

    def update_speed(self):
        """Ajusta a velocidade das naves baseado no número de aliens restantes."""
        aliens_count = len(self)
        if aliens_count == 1:
            self.move_time = 200  # Máxima velocidade
        elif aliens_count <= 10:
            self.move_time = 400  # Velocidade intermediária

    def kill(self, alien):
        """
        Remove um alienígena da matriz e atualiza os controles de formação.
        
        Args:
            alien (object): O alienígena a ser removido
        """
        self.aliens[alien.row][alien.column] = None  # Limpa a posição

        if self.is_column_dead(alien.column):
            self.alive_columns.remove(alien.column)  # Remove coluna das ativas

        # Ajusta extremos se necessário
        if alien.column == self.rightmost_alive_column:
            self._adjust_rightmost_column()
        elif alien.column == self.leftmost_alive_column:
            self._adjust_leftmost_column()

    def _adjust_rightmost_column(self):
        """Ajusta a coluna mais à direita após morte de alienígena."""
        while (self.rightmost_alive_column > 0 and 
               self.is_column_dead(self.rightmost_alive_column)):
            self.rightmost_alive_column -= 1
            self.right_add_move += 5  # Permite mais movimentos para direita

    def _adjust_leftmost_column(self):
        """Ajusta a coluna mais à esquerda após morte do alienígena."""
        while (self.leftmost_alive_column < self.columns and 
               self.is_column_dead(self.leftmost_alive_column)):
            self.leftmost_alive_column += 1
            self.left_add_move += 5  # Permite mais movimentos para esquerda