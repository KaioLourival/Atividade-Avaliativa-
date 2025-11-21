# importa o módulo socket
from socket import *
import sys # necessário para encerrar o programa

# cria o socket TCP (orientado à conexão)
serverSocket = socket(AF_INET, SOCK_STREAM)

# prepara o socket do servidor
serverPort = 6789
serverSocket.bind(('', serverPort))


while True:
    # estabelece a conexão
    print('Ready to serve...')

    connectionSocket, addr = serverSocket.accept()

    try:
        # recebe a mensagem do cliente (requisição HTTP)
        message = connectionSocket.recv(1024).decode()

        filename = message.split()[1]
        f = open(filename[1:])

        outputdata = f.read()

        header = "HTTP/1.1 200 OK\r\n\r\n"
        connectionSocket.send(header.encode())

        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        # fecha a conexão com o cliente
        connectionSocket.close()

    except IOError:
        # envia mensagem de erro 404 se o arquivo não for encontrado
        header_404 = "HTTP/1.1 404 Not Found\r\n\r\n"
        connectionSocket.send(header_404.encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>".encode())

        # fecha o socket do cliente
        connectionSocket.close()

serverSocket.close()
sys.exit() # encerra o programa