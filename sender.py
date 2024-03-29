import socket
import time
import _thread
import segmentoConfiavel 

host = 'localhost'
portaServidor = 9000
portaCliente = 8000

TIMEOUT = 10

class Sender():
    def __init__(self, receiver_address, window_size):
        self.receiver_address = receiver_address
        self.window_size = window_size
        self.base = 0
        self.next_seq_num = 0
        self.buffer = []
        self.servidor_socket = None
        self.running = False

    def start(self):
        '''Inicializa o socket do servidor'''
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.servidor_socket.bind(("0.0.0.0", portaCliente))

    def sendMensage(self, mensagem):
        '''Envia o pacote para o servidor'''
        self.servidor_socket.sendto(mensagem, self.receiver_address)

    # Receive thread
    def receive(self,sock):
        '''Recebe os ACK's dos pacotes enviados'''
        while True:
            pack, endereco_receiver = self.servidor_socket.recvfrom(1024)
            ack, package = segmentoConfiavel.extract(pack)
            print(f"{sender.receiver_address} - ACk recebido {ack}")
            if (ack >= self.base):
                self.base = ack

mensagem = input("Mensagem que vai ser enviada: ")
quantidade = int(input("Quantidade de vezes: "))

sender = Sender((host, portaServidor), 2)
sender.start()

for i in range(quantidade):
    sender.buffer.append(segmentoConfiavel.make(i, mensagem.encode()))

# Abre uma thread para receber os ACK's dos pacotes enviados
_thread.start_new_thread(sender.receive, (sender.servidor_socket,))

while sender.base < len(sender.buffer):

    # Envia os pacotes da janela
    while sender.next_seq_num < sender.base + sender.window_size and sender.next_seq_num < len(sender.buffer):
        print(f'{sender.receiver_address} - Enviando o pacote', sender.next_seq_num)
        sender.sendMensage(sender.buffer[sender.next_seq_num])
        sender.next_seq_num += 1

    # Inicia o time para timeout
    if not sender.running:
        duration = time.time()
        sender.running = True
    
    # verifica se ocorreu timeout para reenviar os pacotes da janela atual
    if time.time() - duration > TIMEOUT:
        print(10 * "--" + " Timeout " + 10 * "--")
        print(f"Reenviando os pacotes da janela {sender.base} Até {sender.base + sender.window_size - 1}")
        print(15 * "----")
        sender.running = False
        sender.next_seq_num = sender.base

    time.sleep(5)