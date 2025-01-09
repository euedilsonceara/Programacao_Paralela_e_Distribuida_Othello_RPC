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

        return peca, "Aguardando outro jogador." if len(self.jogadores) < 2 else "O jogo começou!"

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

    def realizar_jogada(self, peca, linha, coluna):
        if self.finalizado:
            return "O jogo já foi finalizado."

        if str(self.vez) != str(peca[0]):
            return f"vez{self.vez} peca{peca} Não é sua vez."

        if not (0 <= linha < 8 and 0 <= coluna < 8) or self.tabuleiro[linha][coluna] != "❌":
            return "Jogada inválida. Tente novamente."

        self.tabuleiro[linha][coluna] = peca
        self.vez = "⚪" if peca == "⚫" else "⚫"

        # Notifica ambos os jogadores sobre o tabuleiro atualizado
        for jogador in self.jogadores:
            # A função abaixo é fictícia, aqui você poderia fazer algo mais complexo
            # para enviar o tabuleiro para os jogadores.
            print(f"Tabuleiro atualizado para {jogador[0]}.")

        return "Jogada realizada com sucesso."
    
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