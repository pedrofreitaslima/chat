import threading
from socket import socket, AF_INET, SOCK_STREAM
import logging
import sys

# Constantes
HOSPEDEIRO = 'localhost'
PORTA = 5500
ENDERECO = (HOSPEDEIRO, PORTA)
QUANTIDADE_USUARIOS = 10
TAMANHO_BUFFER = 1024
TIPO_CODIFICACAO = 'utf-8'
FORMATO_LOGGER = '%(asctime)s - [%(module)s] %(message)s'

# Variaveis
SERVICO = socket(AF_INET, SOCK_STREAM)
SERVICO.bind(ENDERECO)
mensagens = []
usuarios = []

def iniciar():
    logging.debug(f'Servidor iniciado em {HOSPEDEIRO}:{PORTA}')
    SERVICO.listen(QUANTIDADE_USUARIOS)
    logging.debug(f'Servidor ouvindo até {QUANTIDADE_USUARIOS} clientes')
    thread_novos_usuarios = threading.Thread(target=aceitar_novos_usuarios)
    thread_novos_usuarios.start()

def aceitar_novos_usuarios():
    logging.debug(f'Aguandando uma nova conexão de cliente')
    while True:
        servico, endereco = SERVICO.accept()
        if servico:
            logging.debug(f'Cliente {endereco} conectado no servidor')
            novo_usuario = {
                'servico': servico,
                'endereco': endereco,
                'nome': '',
                'ultima_mensagem': 0
            }
            usuarios.append(novo_usuario)
            thread_receber = threading.Thread(target=receber_mensagens, args=(servico,endereco))
            enviar_mensagem_sincronizar(servico, endereco[1])
            thread_receber.start()

def receber_mensagens(servico, endereco):
    logging.info(f'Aguadando novas mensagens de {endereco}')
    while True:
        mensagem = servico.recv(TAMANHO_BUFFER).decode(TIPO_CODIFICACAO)
        if not mensagem: break
        elif mensagem.startswith('NOME'):
            msg = mensagem.split('=')
            for usuario in usuarios:
                endereco_usr = usuario['endereco']
                if  endereco_usr[0] == endereco[0] \
                        and endereco_usr[1] == endereco[1]:
                    usuario['nome'] = msg[1]
                    logging.debug(f'Nome do usuario alterado {msg[1]}')
                    mensagem_fmtd = {
                        'endereco': endereco,
                        'mensagem': f'{msg[1]} entrou no chat'
                    }
                    mensagens.append(mensagem_fmtd)
                    enviar_mensagem(endereco, mensagem_fmtd['mensagem'])
        elif mensagem.startswith('MSG'):
            msg = mensagem.split('=')
            mensagem_fmtd = {
                'endereco': endereco,
                'mensagem': criar_padrao_mensagem_envio(endereco[1], msg[1])
            }
            logging.debug(f'Mensagem recebida de {endereco}')
            mensagens.append(mensagem_fmtd)
            enviar_mensagem(endereco[1], mensagem_fmtd['mensagem'])
        else:
            logging.debug(f'Finalizando conexão do cliente {endereco}')
            enviar_mensagem(endereco, f'Usuario deixou o chat')
            servico.close()
            sys.exit(0)
            break


def enviar_mensagem(endereco, mensagem):
    for usuario in usuarios:
        endereco_usr = usuario['endereco']
        if endereco_usr[1] != endereco:
            servico_usr = usuario['servico']
            servico_usr.send(mensagem.encode())


def enviar_mensagem_sincronizar(servico, endereco):
    for mensagem in mensagens:
        endereco_msg = mensagem['endereco']
        if endereco_msg[1] != endereco:
            msg = mensagem['mensagem'] + '\n'
            servico.send(msg.encode())


def criar_padrao_mensagem_envio(endereco, mensagem):
    for usuario in usuarios:
        endereco_usr = usuario['endereco']
        if endereco_usr[1] == endereco:
            nome_usr = usuario['nome']
    msg = f'{nome_usr} -> {mensagem}\n'
    return msg

if __name__ == '__main__':
    logging.basicConfig(format=FORMATO_LOGGER, level=logging.DEBUG, datefmt='%d/%m/%y %H:%m:%S')
    iniciar()
