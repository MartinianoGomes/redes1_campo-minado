# Campo Minado - Redes 1

O código implementa um jogo de Campo Minado utilizando sockets para comunicação entre cliente e servidor. Aqui está o que acontece:

## Servidor (`server.py`)
1. **Configuração do servidor:**

    - O servidor é configurado para escutar conexões na porta `12001` no endereço `localhost`.
    - Ele utiliza o protocolo TCP (SOCK_STREAM).

2. **Criação do campo de jogo:**

    - A função criar_campo gera um campo de tamanho 5x5 com 5 minas posicionadas aleatoriamente.
    - O campo é representado como uma matriz (campo), e as minas são armazenadas em um conjunto (minas).

3. **Loop principal do servidor:**

    - O servidor aguarda conexões de clientes.
    - Quando um cliente se conecta, ele entra em um loop para processar as jogadas enviadas.

4. **Processamento das jogadas:**

    - O servidor recebe uma posição no formato linha,coluna enviada pelo cliente.
    - Ele verifica:
        - Se a entrada é válida: Caso contrário, envia uma mensagem de erro.
        - Se a posição contém uma mina: Envia "💥 BOOM! Você perdeu." e encerra o jogo para o cliente.
        - Se a posição já foi escolhida: Envia "⚠️ Já escolhido. Tente outro."
        - Se a posição é segura: Adiciona à lista de descobertas e verifica se o jogador venceu (descobriu todas as posições seguras).
    - O servidor responde ao cliente com mensagens apropriadas.

5. **Desconexão:**

    - Quando o cliente encerra a conexão ou o jogo termina, o servidor fecha o socket do cliente e volta a aguardar novas conexões.

## Cliente (`client.py`)

1. **Conexão ao servidor:**

    - O cliente se conecta ao servidor no endereço `localhost` e porta `12001`.

2. **Interação com o jogador:**

    - O cliente solicita ao jogador uma posição no formato linha,coluna.
    - A posição é enviada ao servidor via socket.

3. **Recebimento da resposta:**

    - O cliente recebe a resposta do servidor e a exibe para o jogador.
    - Se a resposta indicar "💥 BOOM!" ou "🎉 Parabéns!", o jogo termina.

4. **Encerramento:**

    - O cliente fecha a conexão com o servidor e exibe uma mensagem de fim de jogo.

## Fluxo de comunicação

1. O cliente envia uma posição ao servidor.
2. O servidor processa a jogada e responde com o resultado.
3. O cliente exibe a resposta ao jogador.
4. O processo continua até que o jogador vença ou perca.

## Resumo

- O **servidor** gerencia o estado do jogo (campo, minas, posições descobertas) e valida as jogadas.
- O **cliente** é responsável por interagir com o jogador e enviar as jogadas ao servidor.
- A comunicação entre cliente e servidor é feita via **sockets TCP**.