import random
import time
import json
import os

def make(seq_num, data):
    '''Cria o package a ser enviado com o seq_num e os dados informados'''
    seq_bytes = seq_num.to_bytes(4, byteorder = 'little', signed = True)
    return seq_bytes + data

def extract(package):
    '''Retorna o seq_num e os dados do package recebidos'''
    seq_num = int.from_bytes(package[0:4], byteorder = 'little', signed = True)
    return seq_num, package[4:]

# 4 - Parametrizar CONFIG - Ler o arquivo JSON
caminho_arquivo = "config.json"
if os.path.exists(caminho_arquivo):
    with open(os.getcwd() + "/" + caminho_arquivo) as arquivo:
        dados_config = json.load(arquivo)

        # Obter valores do arquivo de configuração
        prob_eliminar_package = dados_config['Probabilidades']['eliminar_package']
        prob_duplicar_package = dados_config['Probabilidades']['duplicar_package']
        prob_atrasar_package = dados_config['Probabilidades']['atrasar_package']
        prop_milesegundos_delay = dados_config['Tempo']['delay']
        prop_timeout_sender = dados_config['Timeout']['sender']
else:
    print(f'O arquivo {caminho_arquivo} não foi encontrado.')

class Canal:
    def __init__(self):
        self.__packagesTotal = 0
        self.__packagesEliminadas = 0
        self.__packagesAtrasadas = 0
        self.__packagesDuplicadas = 0
        self.__mensagens = []

    def sendPackage(self, servidor_socket, receiver_address, package):
        
        self.__packagesTotal += 1
        seq_num, data = extract(package)

        eliminar = self._eliminarPackage(prob_eliminar_package)
        if eliminar:
            self.__mensagens.append(f"Eliminado")
        else:
            
            atrasar = self.__atrasarPackage(prob_atrasar_package, prop_milesegundos_delay)
            duplicar = self.__duplicarPackage(prob_duplicar_package)

            if atrasar:
                self.__mensagens.append(f"Atrasado")
            
            if duplicar:
                self.__mensagens.append(f"Duplicado")
                servidor_socket.sendto(package, receiver_address)

            servidor_socket.sendto(package, receiver_address)

        self._exibirErros(seq_num, receiver_address)
    
    def _eliminarPackage(self, probabilidade):

        resultado = random.uniform(0, 1)
        
        if resultado <= (probabilidade/100):

            self.__packagesEliminadas += 1

            return True
        
        return False
    
    def __atrasarPackage(self, probabilidade, mile):
            
        resultado = random.uniform(0, 1)

        if resultado <= (probabilidade/1000): 
            
            time.sleep(mile/1000)
            self.__packagesAtrasadas += 1

            return True

        return False
    
    def __duplicarPackage(self, probabilidade):

        resultado = random.uniform(0, 1)
        
        if resultado <= (probabilidade/100):
            
            self.__packagesDuplicadas += 1

            return True
        
        return False
    
    def _exibirErros(self, seq_num, address: tuple):
        print(f'''{address} - Erros adicionados no envio do package {seq_num}: [{self.Cor.VERMELHO}{", ".join(self.__mensagens)}{self.Cor.RESET}]''')
        self.__mensagens = []

    def ImprimirErros(self):
        print( "\n" + "---" * 5 + " Consolidação de erros " + "---" * 5)
        print(f'''
        Total de packages enviadas: {self.__packagesTotal}
        Total de packages eliminadas: {self.__packagesEliminadas}
        Total de packages atrasadas: {self.__packagesAtrasadas}
        Total de packages duplicadas: {self.__packagesDuplicadas}
        ''')
        print("---" * 18)
    
    class Cor:
            RESET = '\033[0m'
            VERMELHO = '\033[91m'
            VERDE = '\033[92m'
            AMARELO = '\033[93m'
            AZUL = '\033[94m'
            ROXO = '\033[95m'
            CIANO = '\033[96m'
            BRANCO = '\033[97m'