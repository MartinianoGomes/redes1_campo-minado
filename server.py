import socket
import random
import json

def criar_campo():
    # Criar um campo vazio 5x5
    campo = [[0 for _ in range(5)] for _ in range(5)]
    
    # Posicionar 5 minas aleatoriamente
    minas = set()
    while len(minas) < 5:
        linha = random.randint(0, 4)
        coluna = random.randint(0, 4)
        minas.add((linha, coluna))
    
    return campo, minas

def gerar_visualizacao_campo(minas, descobertas, perdeu=False):
    """Gera uma representação visual do campo como matriz"""
    visualizacao = []
    for i in range(5):
        linha = []
        for j in range(5):
            if perdeu and (i, j) in minas:
                # Mostrar minas quando o jogador perde
                linha.append("💣")
            elif (i, j) in descobertas:
                # Posição já descoberta
                linha.append("✓")
            else:
                # Posição ainda não revelada
                linha.append("■")
        visualizacao.append(linha)
    return visualizacao

def main():
    # Criar socket do servidor
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Vincula o socket à porta 12001
    endereco_servidor = ('localhost', 12001)
    servidor_socket.bind(endereco_servidor)
    
    # Aguarda conexões
    servidor_socket.listen(1)
    print("Servidor de Campo Minado iniciado. Aguardando conexões...")
    
    while True:
        # Aceita conexão do cliente
        conexao_cliente, endereco_cliente = servidor_socket.accept()
        print(f"Cliente conectado: {endereco_cliente}")
        
        # Inicializar novo jogo
        campo, minas = criar_campo()
        descobertas = set()
        
        # Enviar campo inicial
        visualizacao = gerar_visualizacao_campo(minas, descobertas)
        resposta_inicial = {
            "mensagem": "Bem-vindo ao Campo Minado! Faça sua primeira jogada.",
            "campo": visualizacao
        }
        conexao_cliente.send(json.dumps(resposta_inicial).encode())
        
        try:
            while True:
                # Receber jogada do cliente
                jogada = conexao_cliente.recv(1024).decode()
                
                if not jogada:
                    break
                
                print(f"Jogada recebida: {jogada}")
                
                # Validar formato da jogada
                try:
                    linha, coluna = map(int, jogada.split(','))
                    if linha < 0 or linha > 4 or coluna < 0 or coluna > 4:
                        resposta = {
                            "mensagem": "⚠️ Posição inválida. Use valores entre 0 e 4.",
                            "campo": gerar_visualizacao_campo(minas, descobertas)
                        }
                        conexao_cliente.send(json.dumps(resposta).encode())
                        continue
                except:
                    resposta = {
                        "mensagem": "⚠️ Formato inválido. Use linha,coluna (ex: 2,3)",
                        "campo": gerar_visualizacao_campo(minas, descobertas)
                    }
                    conexao_cliente.send(json.dumps(resposta).encode())
                    continue
                
                # Verificar se acertou uma mina
                if (linha, coluna) in minas:
                    resposta = {
                        "mensagem": "💥 BOOM! Você perdeu.",
                        "campo": gerar_visualizacao_campo(minas, descobertas, perdeu=True),
                        "fim_jogo": True
                    }
                    conexao_cliente.send(json.dumps(resposta).encode())
                    break
                
                # Verificar se a posição já foi escolhida
                if (linha, coluna) in descobertas:
                    resposta = {
                        "mensagem": "⚠️ Já escolhido. Tente outro.",
                        "campo": gerar_visualizacao_campo(minas, descobertas)
                    }
                    conexao_cliente.send(json.dumps(resposta).encode())
                    continue
                
                # Posição segura
                descobertas.add((linha, coluna))
                
                # Verificar se ganhou (todas as posições seguras descobertas)
                total_posicoes = 25  # 5x5
                if len(descobertas) == total_posicoes - len(minas):
                    resposta = {
                        "mensagem": "🎉 Parabéns! Você venceu!",
                        "campo": gerar_visualizacao_campo(minas, descobertas),
                        "fim_jogo": True
                    }
                    conexao_cliente.send(json.dumps(resposta).encode())
                    break
                
                # Enviar resposta de jogada bem-sucedida
                resposta = {
                    "mensagem": f"✓ Posição ({linha},{coluna}) segura! Continue jogando.",
                    "campo": gerar_visualizacao_campo(minas, descobertas)
                }
                conexao_cliente.send(json.dumps(resposta).encode())
        
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            # Encerrar conexão com o cliente
            conexao_cliente.close()
            print(f"Cliente desconectado: {endereco_cliente}")

if __name__ == "__main__":
    main()