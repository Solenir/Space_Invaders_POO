# 🎮 Space Invaders

## 🕹️ Sobre o Jogo

Space Invaders é um jogo de arcade clássico lançado em 1978 pela Taito e se tornou um dos jogos mais icônicos da história dos videogames. O objetivo do jogo é controlar uma nave espacial e eliminar ondas de alienígenas que descem progressivamente em direção à nave do jogador. Cada inimigo destruído concede pontos, e o desafio aumenta conforme o jogador avança.

Este projeto é uma recriação do Space Invaders utilizando Python e a biblioteca Pygame.

## 🚀 Como Jogar

### 🖥️ Executando o Arquivo Executável (.exe)
Se você não tiver o Python ou o Pygame instalado, basta clicar duas vezes no arquivo `.exe` para iniciar o jogo.

**Nota:** Certifique-se de que o arquivo `.exe` esteja no mesmo diretório que as pastas `sounds`, `images` e `fonts`, pois elas contêm os recursos necessários para o jogo funcionar corretamente.

### 🐍 Executando pelo Python
Caso tenha a versão correta do Python e do Pygame instalada, você pode executar o jogo diretamente pelo terminal ou prompt de comando:

```sh
cd src
python space_invaders.py
```

### 🎮 Controles do Jogo
- **⬅️ Seta Esquerda:** Move a nave para a esquerda.
- **➡️ Seta Direita:** Move a nave para a direita.
- **🔫 Barra de Espaço:** Dispara tiros para eliminar os inimigos.
- **❌ Tecla ESC:** Encerra o Jogo.

## ⚙️ Requisitos
- Python 3.x
- Biblioteca Pygame

Para instalar o Pygame, execute o seguinte comando:
```sh
pip install pygame
```

## 🛠️ Recursos do Jogo
- 🎨 Gráficos inspirados no jogo original, com sprites para naves e alienígenas.
- 🔊 Sons e efeitos para tiros e explosões.
- 📊 Contagem de pontuação e níveis progressivos de dificuldade.
- 🖥️ Interface simples e intuitiva para os jogadores.

## 📂 Estrutura do Projeto
A estrutura do diretório do projeto é organizada da seguinte forma:
```
src/
│── space_invaders.py   # Arquivo principal do jogo
│── space_invaders.exe  # Arquivo executável do jogo
│── alien/
│   ├── alien.py            # Arquivo que representa o alienígena
│   ├── alien_explosion.py  # Arquivo que representa a explosão de um alienígena
│   ├── alien_group.py      # Arquivo que representa o conjunto de alienígenas
│── mystery/
│   ├── mystery.py            # Arquivo que representa a nave que aparece de tempo em tempo
│   ├── mystery_explosion.py  # Arquivo que representa a explosão da nave que ocasionalmente aparece
│── ship/
│   ├── ship.py            # Arquivo que representa a nave amiga
│   ├── ship_explosion.py  # Arquivo que representa a explosão da nave amiga
│── helpers/
│   ├── blocker.py   # Arquivo que representa os blocos de proteção da nave amiga
│   ├── bullet.py    # Arquivo que representa o projétil utilizado no jogo
│   ├── life.py      # Arquivo que representa as vidas do jogo
│   ├── text.py      # Arquivo que representa textos utilizados no jogo
│   ├── constants.py # Arquivo que armazena as constantes utilizadas pelo jogo
assets/
│   ├── images/       # Sprites e gráficos do jogo
│   ├── sounds/       # Efeitos sonoros
│   ├── fonts/        # Fontes utilizadas no jogo
README.md             # Documentação do projeto
```
## Principais Telas do Jogo

![Tela Inicial](https://github.com/user-attachments/assets/d5055d0d-055b-4d5b-8bb6-8d5abcd86d0e)
![Tela do Jogo](https://github.com/user-attachments/assets/a305d43c-10e4-4ec0-9023-1b56988fe390)

## 🤝 Contribuição
Se quiser contribuir para melhorias no jogo, sinta-se à vontade para criar um *fork* do repositório, realizar suas alterações e abrir um *pull request*.

---
Divirta-se jogando Space Invaders! 🚀👾
