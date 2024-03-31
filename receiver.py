import socket
import segmentoConfiavel
from segmentoConfiavel import Canal

host = ''
portaServidor = 9000

expected_seq_num = 0
MensagemFinal = b""

canal = Canal()

portaServidor = int(input("Qual é a porta: "))

servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor_socket.bind((host, portaServidor))
servidor_socket.settimeout(20)

while True:

    try:
        print(f"Aguardando packages")
        pack, endereco_sender = servidor_socket.recvfrom(1024)

        seq_num, data = segmentoConfiavel.extract(pack)

        print(f"{endereco_sender} - Dados recebido: {seq_num}-{data.decode('utf-8')}")

        # Enviar uma resposta para o sender caso o package esteja em ordem ou fora de ordem
        if seq_num != expected_seq_num:
            print(f"{endereco_sender} - Mensagem id {seq_num} recebida fora de ordem, ainda esperando o identificador {expected_seq_num}")
            mensagem = b"package fora de ordem"
            package = segmentoConfiavel.make(expected_seq_num - 1, mensagem)

            #servidor_socket.sendto(package, (endereco_cliente[0], endereco_cliente[1]))
            canal.sendPackage(servidor_socket, (endereco_sender[0], endereco_sender[1]), package)
            print(f"{endereco_sender} - ACK {expected_seq_num - 1} enviado")
        else:
            print(f"{endereco_sender} - Mensagem id {seq_num} recebida na ordem, entregando para a camada de aplicação")
            mensagem = b"Ok"
            package = segmentoConfiavel.make(seq_num, mensagem)
            expected_seq_num = seq_num + 1
            MensagemFinal += data

            #servidor_socket.sendto(package, (endereco_cliente[0], endereco_cliente[1]))
            canal.sendPackage(servidor_socket, (endereco_sender[0], endereco_sender[1]), package)
            print(f"{endereco_sender} - ACK {seq_num} enviado")
    except socket.timeout:
        break

print("Servidor encerrado")
canal.ImprimirErros()
print(f"Mensagem final: ", MensagemFinal.decode('utf-8'))
print("---" * 18)
