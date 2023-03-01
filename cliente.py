from socket import socket, AF_INET, SOCK_STREAM
import threading
import logging
import sys

# CONSTANTES
HOSPEDEIRO = 'localhost'
PORTA = 5500
ENDERECO = (HOSPEDEIRO, PORTA)
TAMANHO_BUFFER = 1024
TIPO_CODIFICACAO = 'utf-8'
FORMATO_LOGGER = '%(asctime)s - [%(module)s] %(message)s'

# VARIAVEIS
SERVICO = socket(AF_INET, SOCK_STREAM)


def iniciar():
    SERVICO.connect(ENDERECO)
    logging.debug('Cliente iniciada')
    print('Para sair digite [SAIR]')
    manipular_entradas()


def manipular_entradas():
    nome = input('Digite seu nome: ')
    if nome: mensagem = 'NOME=' + nome
    while mensagem:
        if mensagem != 'SAIR':
            thread_enviar = threading.Thread(target=enviar_mensagem, args=(mensagem,))
            thread_receber = threading.Thread(target=receber_mensagem)
            thread_enviar.start()
            thread_receber.start()
            msg = input('->')
            mensagem = 'MSG=' + msg
        else:
            SERVICO.close()
            sys.exit(0)


def enviar_mensagem(mensagem):
    SERVICO.send(mensagem.encode())


def receber_mensagem():
    while True:
        mensagem = SERVICO.recv(TAMANHO_BUFFER)
        if mensagem:
            print(mensagem.decode(TIPO_CODIFICACAO))


if __name__ == '__main__':
    logging.basicConfig(format=FORMATO_LOGGER, level=logging.DEBUG, datefmt='%d/%m/%y %H:%m:%S')
    iniciar()
