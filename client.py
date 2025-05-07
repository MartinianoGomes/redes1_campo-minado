import socket
import json

def exibir_campo(campo):
    """Exibe o campo minado com formato simplificado"""
    print("\n   0 1 2 3 4")
    print("  ----------")
    for i, linha in enumerate(campo):
        linha_str = f"{i} | "
        for celula in linha:
            # Substitui os símbolos existentes por mais simples
            if celula == "■":
                linha_str += "■ "
            elif celula == "✓":
                linha_str += "X "
            elif celula == "💣":
                linha_str += "💣 "
            else:
                linha_str += celula + " "
        print(linha_str)
    print()

def main():
    # Criar socket do cliente
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conectar ao servidor
    endereco_servidor = ('localhost', 12001)
    print("Conectando ao servidor...")
    
    try:
        cliente_socket.connect(endereco_servidor)
        print("Conectado ao servidor de Campo Minado!")
        print("\n=== CAMPO MINADO ===")
        print("Informe posições no formato linha,coluna (valores de 0 a 4)")
        print("Exemplo: 2,3")
        print("===================\n")
        
        # Receber mensagem inicial e exibir campo
        resposta_inicial = cliente_socket.recv(1024).decode()
        dados = json.loads(resposta_inicial)
        print(dados["mensagem"])
        exibir_campo(dados["campo"])
        
        # Loop principal do jogo
        while True:
            # Obter jogada do usuário
            jogada = input("Digite a posição (linha,coluna): ")
            
            # Enviar jogada ao servidor
            cliente_socket.send(jogada.encode())
            
            # Receber resposta do servidor
            resposta = cliente_socket.recv(1024).decode()
            dados = json.loads(resposta)
            
            # Exibir mensagem e campo atualizado
            print(dados["mensagem"])
            exibir_campo(dados["campo"])
            
            # Verificar se o jogo acabou
            if dados.get("fim_jogo", False):
                print("\nFim de jogo!")
                break
    
    except ConnectionRefusedError:
        print("Não foi possível conectar ao servidor. Verifique se o servidor está em execução.")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        # Fechar conexão
        cliente_socket.close()
        print("Conexão encerrada.")

if __name__ == "__main__":
    main()