from pygame import sprite, time
from random import choice
from helpers import constants

 '''
 Classe responsável por inicializar grupos de alienígenas. 
 '''
class AliensGroup(sprite.Group):
    def __init__(self, columns, rows, game):
        super().__init__()  # Inicializa a classe base (sprite.Group)

        # Configurações iniciais
        self.rows = rows
        self.columns = columns
        self.aliens = [[None for _ in range(columns)] for _ in range(rows)]  # Matriz de alienígenas

        # Controle de movimentação
        self.direction = 1  # 1 para direita, -1 para esquerda
        self.left_moves = 30  # Movimentos restantes para a esquerda
        self.right_moves = 30  # Movimentos restantes para a direita
        self.left_add_move = 0  # Movimentos adicionais à esquerda
        self.right_add_move = 0  # Movimentos adicionais à direita
        self.move_number = 15  # Contador de movimentos realizados
        self.move_time = 600  # Tempo entre movimentos (em milissegundos)

        # Controle de tempo e posição
        self.timer = time.get_ticks()  # Tempo do último movimento
        self.bottom = game.enemyPosition + ((rows - 1) * 45) + 35  # Posição mais baixa dos alienígenas

        # Controle de colunas vivas
        self.alive_columns = list(range(columns))  # Lista de colunas com alienígenas vivos
        self.leftmost_alive_column = 0  # Coluna mais à esquerda com alienígenas vivos
        self.rightmost_alive_column = columns - 1  # Coluna mais à direita com alienígenas vivos

    def update(self, current_time):
        """
        Atualiza a posição dos alienígenas com base no tempo atual.
        
        :param current_time: Tempo atual do jogo (em milissegundos).
        """
        if current_time - self.timer > self.move_time:
            max_move = (
                self.right_moves + self.right_add_move if self.direction == 1
                else self.left_moves + self.left_add_move
            )

            if self.move_number >= max_move:
                # Inverte a direção e move os alienígenas para baixo
                self._reverse_direction()
                self._move_down()
            else:
                # Move os alienígenas lateralmente
                self._move_laterally()

            self.timer += self.move_time  # Atualiza o tempo do último movimento

    def _reverse_direction(self):
        """Inverte a direção do movimento dos alienígenas."""
        self.direction *= -1
        self.move_number = 0
        self.left_moves = 30 + (self.right_add_move if self.direction == 1 else self.left_add_move)
        self.right_moves = 30 + (self.right_add_move if self.direction == 1 else self.left_add_move)

    def _move_down(self):
        """Move todos os alienígenas para baixo e atualiza a posição mais baixa."""
        self.bottom = 0
        for alien in self:
            alien.rect.y += constants.ENEMY_MOVE_DOWN
            alien._toggle_image()  # Alterna a imagem para animação
            self.bottom = max(self.bottom, alien.rect.y + 35)

    def _move_laterally(self):
        """Move os alienígenas para a esquerda ou direita com base na direção atual."""
        shift = 10 * self.direction
        for alien in self:
            alien.rect.x += shift
            alien._toggle_image()  # Alterna a imagem para animação
        self.move_number += 1

    def add_internal(self, *sprites):
        """
        Adiciona alienígenas ao grupo e à matriz.
        
        :param sprites: Alienígenas a serem adicionados.
        """
        super().add_internal(*sprites)
        for sprite in sprites:
            self.aliens[sprite.row][sprite.column] = sprite

    def remove_internal(self, *sprites):
        """
        Remove alienígenas do grupo e da matriz.
        
        :param sprites: Alienígenas a serem removidos.
        """
        super().remove_internal(*sprites)
        for sprite in sprites:
            self.kill(sprite)
        self.update_speed()

    def is_column_dead(self, column):
        """
        Verifica se uma coluna está sem alienígenas vivos.
        
        :param column: Índice da coluna a ser verificada.
        :return: True se a coluna estiver vazia, False caso contrário.
        """
        return not any(self.aliens[row][column] for row in range(self.rows))

    def random_bottom_alien(self):
        """
        Seleciona aleatoriamente um alienígena da parte inferior de uma coluna viva.
        
        :return: O alienígena selecionado ou None se não houver alienígenas vivos.
        """
        column = choice(self.alive_columns)  # Escolhe uma coluna ativa aleatória
        for row in range(self.rows - 1, -1, -1):  # Itera da parte inferior para cima
            alien = self.aliens[row][column]
            if alien is not None:
                return alien
        return None

    def update_speed(self):
        """Ajusta a velocidade dos alienígenas com base no número de alienígenas restantes."""
        if len(self) == 1:
            self.move_time = 200  # Aumenta a velocidade se houver apenas um alienígena
        elif len(self) <= 10:
            self.move_time = 400  # Aumenta a velocidade se houver 10 ou menos alienígenas

    def kill(self, alien):
        """
        Remove um alienígena da matriz e atualiza as colunas vivas.
        
        :param alien: Alienígena a ser removido.
        """
        self.aliens[alien.row][alien.column] = None  # Remove o alienígena da matriz

        if self.is_column_dead(alien.column):
            self.alive_columns.remove(alien.column)  # Remove a coluna da lista de colunas vivas

        # Ajusta as colunas mais à esquerda e à direita, se necessário
        if alien.column == self.rightmost_alive_column:
            self._adjust_rightmost_column()
        elif alien.column == self.leftmost_alive_column:
            self._adjust_leftmost_column()

    def _adjust_rightmost_column(self):
        """Ajusta a coluna mais à direita após a remoção de um alienígena."""
        while self.rightmost_alive_column > 0 and self.is_column_dead(self.rightmost_alive_column):
            self.rightmost_alive_column -= 1
            self.right_add_move += 5

    def _adjust_leftmost_column(self):
        """Ajusta a coluna mais à esquerda após a remoção de um alienígena."""
        while self.leftmost_alive_column < self.columns and self.is_column_dead(self.leftmost_alive_column):
            self.leftmost_alive_column += 1
            self.left_add_move += 5