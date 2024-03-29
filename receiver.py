import socket
import segmentoConfiavel

host = 'localhost'
portaServidor = 9000

servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor_socket.bind((host, portaServidor))
servidor_socket.settimeout(20)

expected_seq_num = 0
MensagemFinal = b""

while True:

    try:
        print("Aguardando conexão")
        dados, endereco_cliente = servidor_socket.recvfrom(1024)

        seq_num, data = segmentoConfiavel.extract(dados)

        print(f"{endereco_cliente} - Dados recebido: {seq_num}-{data.decode('utf-8')}")

        # Enviar uma resposta para o sender caso o package esteja em ordem ou fora de ordem
        if seq_num != expected_seq_num:
            print(f"{endereco_cliente} - Mensagem id {seq_num} recebida fora de ordem, ainda esperando o identificador {expected_seq_num}")
            mensagem = b"package fora de ordem"
            package = segmentoConfiavel.make(expected_seq_num, mensagem)

            servidor_socket.sendto(package, (endereco_cliente[0], endereco_cliente[1]))
            print(f"{endereco_cliente} - ACK {expected_seq_num} enviado")
        else:
            print(f"{endereco_cliente} - Mensagem id {seq_num} recebida na ordem, entregando para a camada de aplicação")
            mensagem = b"Ok"
            package = segmentoConfiavel.make(seq_num + 1, mensagem)
            expected_seq_num = seq_num + 1
            MensagemFinal += data

            servidor_socket.sendto(package, (endereco_cliente[0], endereco_cliente[1]))
            print(f"{endereco_cliente} - ACK {seq_num + 1} enviado")
    except socket.timeout:
        break

print(f"Mensagem final: ", MensagemFinal.decode('utf-8'))
