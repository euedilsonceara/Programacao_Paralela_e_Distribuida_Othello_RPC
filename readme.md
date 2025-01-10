# Projeto Othello Multiplayer

Este é um projeto do jogo Othello (também conhecido como Reversi) implementado com um servidor e clientes em Python utilizando XML-RPC para comunicação entre o servidor e os jogadores. O servidor gerencia o estado do jogo, tabuleiro, jogadas e comunicação entre os jogadores, enquanto os clientes representam os jogadores conectados ao servidor.

## Requisitos

- Python 3.x
- Biblioteca `xmlrpc.client` (incluída no Python)
- Biblioteca `xmlrpc.server` (incluída no Python)

## Estrutura do Projeto

- **Servidor**: Responsável por gerenciar o estado do jogo, validar jogadas e interagir com os jogadores.
- **Jogadores**: Cada jogador se conecta ao servidor, interage com o tabuleiro, realiza jogadas, envia mensagens e pode desistir do jogo.

### Arquivos

- **servidor.py**: Código do servidor Othello, que gerencia o estado do jogo, as jogadas, a troca de mensagens e determina o vencedor.
- **jogador1.py**: Código para o jogador 1 que interage com o servidor, faz jogadas, envia mensagens e pode desistir do jogo.
- **jogador2.py**: Código para o jogador 2 que interage com o servidor, faz jogadas, envia mensagens e pode desistir do jogo.


## Como Rodar
- Execute o arquivo `servidor.py` para iniciar o servidor Othello:
- Execute o arquivo `jogador1.py` para conectar o jogador 1 e insira o nome do jogador logo em seguida
- Execute o arquivo `jogador2.py` para conectar o jogador 2 e insira o nome do jogador logo em seguida
- Siga as instruções e opções do terminal para jogar
