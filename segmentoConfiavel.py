def make(seq_num, data):
    '''Cria o package a ser enviado com o seq_num e os dados informados'''
    seq_bytes = seq_num.to_bytes(4, byteorder = 'little', signed = True)
    return seq_bytes + data

def extract(package):
    '''Retorna o seq_num e os dados do package recebidos'''
    seq_num = int.from_bytes(package[0:4], byteorder = 'little', signed = True)
    return seq_num, package[4:]