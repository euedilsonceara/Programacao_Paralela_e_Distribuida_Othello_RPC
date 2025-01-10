# --- Servidor ---
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class ServidorOthello:
    def __init__(self):
        self.tabuleiro = [["❌" for _ in range(8)] for _ in range(8)]
        self.tabuleiro[3][3] = "⚪"
        self.tabuleiro[3][4] = "⚫"
        self.tabuleiro[4][3] = "⚫"
        self.tabuleiro[4][4] = "⚪"
        self.jogadores = []
        self.chat = []
        self.vez = None
        self.finalizado = False
        self.vencedor = None

    def entrar_jogo(self, nome):
        if len(self.jogadores) >= 2:
            return None, "O jogo já está cheio."

        peca = "⚫" if not self.jogadores else "⚪"
        self.jogadores.append((nome, peca))

        if len(self.jogadores) == 2:
            self.vez = "⚫"

        return peca, "Aguardando o outro jogador se conectar." if len(self.jogadores) < 2 else "O jogo começou!"

    def obter_tabuleiro(self):
        if len(self.jogadores) < 2:
            return None
        return self.tabuleiro

    def verificar_finalizacao(self):
        return self.finalizado

    def determinar_vencedor(self):
        if self.vencedor:
            return self.vencedor
        
        contagem_preto = sum(linha.count("⚫") for linha in self.tabuleiro)
        contagem_branco = sum(linha.count("⚪") for linha in self.tabuleiro)

        if contagem_preto > contagem_branco:
            return "⚫ venceu com {} peças contra {} peças de ⚪.".format(contagem_preto, contagem_branco)
        elif contagem_branco > contagem_preto:
            return "⚪ venceu com {} peças contra {} peças de ⚫.".format(contagem_branco, contagem_preto)
        else:
            return "O jogo terminou empatado com {} peças para cada lado.".format(contagem_preto)

    def jogada_valida(self, peca, linha, coluna):
        """Verifica se a jogada é válida, de acordo com as regras do Othello."""
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        oponente = "⚫" if peca == "⚪" else "⚪"
        jogadas_possiveis = []

        for dx, dy in direcoes:
            x, y = linha + dx, coluna + dy
            encontrou_oponente = False

            while 0 <= x < 8 and 0 <= y < 8 and self.tabuleiro[x][y] == oponente:
                encontrou_oponente = True
                x += dx
                y += dy

            if encontrou_oponente and 0 <= x < 8 and 0 <= y < 8 and self.tabuleiro[x][y] == peca:
                jogadas_possiveis.append((dx, dy))

        return jogadas_possiveis

    def aplicar_jogada(self,peca, linha, coluna, direcoes):
        """Aplica a jogada e atualiza o tabuleiro."""
        oponente = "⚫" if peca == "⚪" else "⚪"
        self.tabuleiro[linha][coluna] = peca

        for dx, dy in direcoes:
            x, y = linha + dx, coluna + dy
            while self.tabuleiro[x][y] == oponente:
                self.tabuleiro[x][y] = peca
                x += dx
                y += dy

    def realizar_jogada(self, peca, linha, coluna):
        """Valida e aplica a jogada no servidor."""
        if self.finalizado:
            return "O jogo já foi finalizado."

        if str(self.vez) != str(peca):
            return f"Não é sua vez. É a vez de {self.vez}."

        if not (0 <= linha < 8 and 0 <= coluna < 8) or self.tabuleiro[linha][coluna] != "❌":
            return "Jogada inválida. Posição ocupada ou fora do tabuleiro."

        direcoes_validas = self.jogada_valida(peca, linha, coluna)
        if not direcoes_validas:
            return "Jogada inválida. Não há peças adversárias para capturar."

        self.aplicar_jogada(peca, linha, coluna, direcoes_validas)
        self.vez = "⚪" if peca == "⚫" else "⚫"

        # Verifica se ainda há jogadas possíveis para os jogadores
        if not self.verificar_jogadas_disponiveis():
            self.finalizado = True
            return self.determinar_vencedor()

        return "Jogada realizada com sucesso."

    def verificar_jogadas_disponiveis(self):
        """Verifica se há jogadas possíveis para ambos os jogadores."""
        for peca in ["⚫", "⚪"]:
            for linha in range(8):
                for coluna in range(8):
                    if self.tabuleiro[linha][coluna] == "❌" and self.jogada_valida(peca, linha, coluna):
                        return True
        return False

    
    def enviar_mensagem(self, nome, mensagem):
        # Adiciona a mensagem ao chat
        self.chat.append(f"{nome}: {mensagem}")
        
        # Envia a mensagem para o adversário
        for jogador in self.jogadores:
            if jogador[0] != nome:  # Enviar para o adversário
                # Aqui deve ser feita uma ação para transmitir a mensagem de volta ao adversário.
                # No caso, o envio de uma mensagem é mostrado no print para o jogador correspondente
                print(f"Mensagem do Oponente ({nome}): {mensagem}")
                return f"Mensagem para {jogador[0]} enviada."

    def obter_chat(self):
        return self.chat

    def desistir(self, peca):
        # Atualiza o status de finalização e define o vencedor
        self.finalizado = True
        if peca == "⚫":
            vencedor = "⚪"
        else:
            vencedor = "⚫"
        self.vencedor = f"{vencedor} venceu porque o adversário desistiu."

        # Notifica ambos os jogadores sobre a desistência
        for jogador in self.jogadores:
            print(f"{jogador[0]} foi notificado que {vencedor} venceu.")
        
        return f"{peca} desistiu. O jogo terminou. {vencedor} venceu."

    def obter_vez(self):
        return self.vez

# Configuração do servidor
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)

servidor = ServidorOthello()

with SimpleXMLRPCServer(("localhost", 8000), requestHandler=RequestHandler, allow_none=True) as server:
    server.register_instance(servidor)
    print("Servidor Othello rodando na porta 8000...")
    server.serve_forever()