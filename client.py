from socket import *

serverName = 'localhost'  # Altere para o IP do servidor se necessário
serverPort = 12001

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

print("🎮 Bem-vindo ao Campo Minado!")
print("Digite uma posição no formato linha,coluna (ex: 2,3).")

while True:
    pos = input("➡️ Sua jogada: ")
    clientSocket.send(pos.encode())
    resposta = clientSocket.recv(1024).decode()
    print("📝 Resposta:", resposta)

    if "BOOM" in resposta or "Parabéns" in resposta:
        break

clientSocket.close()
print("👋 Fim do jogo.")