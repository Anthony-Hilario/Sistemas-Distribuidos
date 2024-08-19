import socket
import random
import time
import threading


def start_client(pid):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8080))  # Use o mesmo IP e porta que no servidor
    # Envia o PID para o servidor.
    client_socket.send(str(pid).encode('utf-8')) # Send 1(pid)

    resposta = client_socket.recv(1024).decode('utf-8') # Confirmação do servidor.
    print(resposta)

    # Inserir os numeros aleatorios e os manda para o servidor
    val = random.randint(10,90)
    client_socket.send(str(val).encode('utf-8')) # Send 2(valor de saque)
    print(f"Conta Nº[{pid}] \n"
          f"Valor a retirar: {val}R$")

    print('-' * 30)
    data_str = client_socket.recv(1024).decode('utf-8')
    print(data_str)
    print('-' * 30)

    # Fecha a conexão com o servidor
    time.sleep(7)
    client_socket.close()
    print(f"Conexão entre o servidor e a conta [{pid}] foi encerrada!")
    print('-' * 30)


threads = []
while True:
    pid = 98503
    thread = threading.Thread(target=start_client, args=(pid,))
    threads.append(thread)
    thread.start()
    time.sleep(5)  # Tempo de inicialização de cada thread