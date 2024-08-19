import socket
import threading
import time

fila = []
saldo = [10000]  # Lista que armazenará o saldo
address = "127.0.0.1"  # Digitar o IP da máquina que será usada como servidor e uma porta que ela não esteja usando.
port = 8080
contador = [0]  # Inicializa o contador dentro de uma lista

lock_saldo = threading.Lock()
def handle_client(client_socket):
    global contador  # Permite a modificação da variável global

    client_socket.send(str("[Conectado ao servidor]").encode('utf-8'))
    # Recebe o PID do cliente
    pid = client_socket.recv(1024).decode() # Recv 1(pid)
    print(f"Conexão com o cliente de Nº[{pid}] estabelecida...")

    val = client_socket.recv(1024).decode() # Recv 2(valor de saque)
    val = int(val)

    def sacar(valor, saldo):
        with lock_saldo:  # Zona Critica
            if saldo[0] == 0 or saldo[0] - valor < 0:
                print("Saldo insuficiente ou operação inválida. Saque cancelado.")
                msg_insulf = f"Cliente [{pid}] sua operação foi rejeitada."
                valor_saldo = client_socket.send(str(msg_insulf).encode('utf-8'))
                return saldo[0]
            else:
                saldo[0] -= valor
            print(f"Valor desejado de saque: {valor}R$, Saldo restante: {saldo[0]}R$")
            return saldo[0]

    def main():

        global contador  # Permite a modificação da variável global

        contador[0] += 1  # Incrementa o contador a cada saque
        valor_saque = val
        novo_saldo = sacar(valor_saque, saldo)

        mensagem_saldo = f"Saldo atual após saque de Nº[{contador[0]}]: {saldo[0]}R$"
        valor_saldo = client_socket.send(str(mensagem_saldo).encode('utf-8'))
        print('-' * 30)
        time.sleep(1)

    main()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((address, port))
server_socket.listen(5)

print(f"Servidor aguardando conexões...")

while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
