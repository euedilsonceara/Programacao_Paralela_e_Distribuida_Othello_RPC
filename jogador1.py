# CÓDIGO DESENVOLVIDO DURANTE A DISCIPLINA DE PROGRAMAÇÃO PARALELA E DISTRIBUÍDA (PPD)
# UNIVERSIDADE: INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DO CEARÁ (IFCE) - CAMPUS FORTALEZA
# CURSO: ENGENHARIA DA COMPUTAÇÃO
# DATA: 09/01/2025
# DENSENVOLVEDOR: JOSÉ EDILSON CEARÁ GOMES FILHO

# INSTRUÇÕES
# 1. EXECUTE PRIMEIRAMENTE O ARQUIVO servidor.py
# 2. EM SEGUIDA EXECUTE O ARQUIVO jogador1.py EM UM TERMINAL DEDICADO
# 3. FINALIZE EXECUTANDO O ARQUIVO jogador2.py EM UM OUTRO TERMINAL
# 4. PRONTO! AGORA JOGUE E DESFRUTE DO JOGO OTHELLO (REVERSI), SEMPRE ACOMPANHANDO AS MENSAGENS E OPÇÕES NO TERMINAL!

##################################################################################################################

# Importação da biblioteca
import xmlrpc.client
class Jogador:
    def __init__(self, nome, peca, servidor):
        self.nome = nome
        self.peca = peca
        self.servidor = servidor

    def jogar(self):
        while True:

            if self.servidor.obter_tabuleiro() is None:
                print("Aguardando o outro jogador se conectar...")
                continue

            # Verifica se o jogo foi finalizado
            if self.servidor.verificar_finalizacao():
                print("Jogo finalizado!")
                print(self.servidor.determinar_vencedor())
                break

            # Exibe "Sua vez de jogar" e o tabuleiro atualizado, somente quando for a vez do jogador
            if self.servidor.obter_vez() == self.peca:
                print("\nSua vez de jogar")

                # Verifica se há mensagens para o jogador
                mensagens = self.servidor.obter_mensagem(self.nome)
                if mensagens != "Nenhuma nova mensagem.":
                    print(f'Mensagem do adversário: {mensagens}')

                # Exibe o tabuleiro mais atualizado
                print("\nTabuleiro atual:")
                for linha in self.servidor.obter_tabuleiro():
                    print(" ".join(linha))

                # Exibe o menu
                print("\nMenu:")
                print("1️⃣  - Realizar Jogada")
                print("2️⃣  - Contar Peças")
                print("3️⃣  - Enviar Mensagem")
                print("4️⃣  - Desistir")
                opcao = input("Escolha uma opção: ")

                if opcao == "1":
                    linha = input("Informe a linha (0-7): ")
                    coluna = input("Informe a coluna (0-7): ")
                    resposta = self.servidor.realizar_jogada(self.peca, int(linha), int(coluna))
                    print(resposta)

                    # Aguardar a resposta e garantir que o tabuleiro seja atualizado
                    if "Jogada realizada com sucesso" in resposta:
                        # Sempre que uma jogada for realizada com sucesso, obtemos o tabuleiro atualizado
                        print("\nTabuleiro atualizado após sua jogada:")
                        for linha in self.servidor.obter_tabuleiro():
                            print(" ".join(linha))

                elif opcao == "2":
                    print("Contando peças no tabuleiro...")
                    contagem_preto = sum(linha.count("⚫") for linha in self.servidor.obter_tabuleiro())
                    contagem_branco = sum(linha.count("⚪") for linha in self.servidor.obter_tabuleiro())
                    print(f"⚫: {contagem_preto}, ⚪: {contagem_branco}")
                elif opcao == "3":
                    mensagem = input("Digite sua mensagem: ")
                    resposta = self.servidor.enviar_mensagem(self.nome, mensagem)
                    print(resposta)
                elif opcao == "4":
                    print(self.servidor.desistir(self.peca))
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            else:
                print("\nAguarde seu oponente jogar")
                continue

def main():
    servidor = xmlrpc.client.ServerProxy("http://localhost:8000/RPC2", allow_none=True)
    
    nome = input("Digite seu nome: ")
    peca, mensagem = servidor.entrar_jogo(nome)
    print(f"Bem-vindo, {nome}! Você jogará com a peça: {peca}.")
    print(mensagem)

    jogador = Jogador(nome, peca, servidor)
    jogador.jogar()

if __name__ == "__main__":
    main()