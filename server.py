from socket import *
import random

def criar_campo(tamanho=5, num_minas=5):
    campo = [[' ' for _ in range(tamanho)] for _ in range(tamanho)]
    minas = set()
    while len(minas) < num_minas:
        linha = random.randint(0, tamanho-1)
        coluna = random.randint(0, tamanho-1)
        minas.add((linha, coluna))
    return campo, minas

serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(1)

print("🚀 Servidor Campo Minado pronto para conexões...")

campo, minas = criar_campo()
descobertas = set()
total_seguro = 25 - len(minas)

while True:
    connectionSocket, addr = serverSocket.accept()
    print("🧑‍💻 Cliente conectado:", addr)
    while True:
        pos = connectionSocket.recv(1024).decode()
        if not pos:
            break

        try:
            linha, coluna = map(int, pos.strip().split(','))
        except:
            connectionSocket.send("❌ Entrada inválida. Use formato: linha,coluna".encode())
            continue

        if (linha, coluna) in minas:
            connectionSocket.send("💥 BOOM! Você perdeu.".encode())
            break
        elif (linha, coluna) in descobertas:
            connectionSocket.send("⚠️ Já escolhido. Tente outro.".encode())
        else:
            descobertas.add((linha, coluna))
            if len(descobertas) == total_seguro:
                connectionSocket.send("🎉 Parabéns! Você venceu.".encode())
                break
            else:
                connectionSocket.send("✅ Vazio. Continue jogando.".encode())

    connectionSocket.close()
    print("🔌 Cliente desconectado.")
