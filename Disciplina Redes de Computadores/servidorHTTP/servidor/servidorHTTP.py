#Servidor HTTP

# Importando o modulo socket = interface entre camada aplicacao e transporte
import socket

# Importando o modulo de tempo
import time

# Endereco do servidor (IP) e a porta em que irá responder requisicoes HTTP
ip_servidor = socket.gethostbyname(socket.gethostname())
porta_servidor = 8090

# Abre um socket IPv4 (AF_INET) e TCP (SOCK_STREAM)
servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Porta do servidor acessada varias vezes
servidor.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

# Informa ao socket seu endereco e porta
servidor.bind((ip_servidor,porta_servidor))

# Ouvir as requisicoes de clientes (ficar disponivel). Maximo 5 clientes
servidor.listen(5)

# Printando que o servidor esta ouvindo no porta tal
print('# Servidor HTTP disponivel no IP',ip_servidor,'e na porta', porta_servidor)

# Sempre pronto a receber requisicoes
while True:
    conexao,cliente = servidor.accept() # Aceitar mensagens
    requisicao = conexao.recv(1024).decode('utf-8') # Guardar 1024 bytes de mensagem na variavel
    requisicao_parcelada = requisicao.split(' ')     # Dividindo a mensagem em blocos com espacos

    if not requisicao_parcelada: # Aguardar um tempo para que a mensagem tenha mais dados
        time.sleep(1.0)
        
    method = requisicao_parcelada[0] # Guardar a primeira posicao da mensagem fragmentada
    arquivo_solicitado = requisicao_parcelada[1] # Guardar a segunda posicao da msg fragmentada = requisicao de arquivo

# Printando qual cliente pediu qual arquivo
    print('# Cliente', cliente[0], 'solicitou: ',arquivo_solicitado)

    arquivo = arquivo_solicitado.split('?')[0] # Qualquer caractere apos ? (se houve) na requisicao sera ignorado
    arquivo = arquivo.lstrip('/') # Retirado o / do nome do arquivo requisitado
    
    if(arquivo == ''): # Se o arquivo for vazio, carregue a pagina index.html (pagina principal do servidor)
        arquivo = 'index.html'

    try: #Ira tentar abrir o arquivo solicitado. Caso nao consiga ira apresentar uma mensagem de pagina nao encontrada (404)
        file = open(arquivo,'rb') # Abre o arquivo , r = ler , b = formato byte
        resposta = file.read() # Variavel Resposta recebe a requisicao, o arquivo aberto
        file.close() # Fecha o arquivo no servidor

        cabecalho = 'HTTP/1.1 200 OK\n' #cabecalho com informacoes do protocolo/versao e codigo de resposta sucesso.

        if(arquivo.endswith(".jpg")): #caso a extensao do arquivo seja JPG informe ao navegador que e uma imagem
            mimetype = 'image/jpg'
        elif(arquivo.endswith(".css")): #caso a extensao do arquivo seja CSS informe ao navegador que e um texto
            mimetype = 'text/css'
        elif(arquivo.endswith(".pdf")): #caso a extensao do arquivo seja PDF informe ao navegador que e um PDF e precisa-se de um app
            mimetype = 'application/pdf'
        elif(arquivo.endswith(".txt")): #caso a extensao do arquivo seja TXT informe ao navegador que e um texto e precisa-se de um app
            mimetype = 'application/txt'
        else:
            mimetype = 'text/html' #caso nao seja um dos informados anteriormente entao ele sera um HTML para o navegador intepretar

        cabecalho += 'Content-Type: '+str(mimetype)+'\n\n' #soma ao cabecalho as informacoes da extensao do arquivo (mimetype)

    except Exception as e: # Se ha requisicao de um arquivo nao existente sera apresentado o erro 404
        cabecalho = 'HTTP/1.1 404 Not Found\n\n'
        resposta = '<html><h2><strong>&gt;&gt;&gt; ERRO 404: ARQUIVO NAO ENCONTRADO!! &gt;&gt;&gt;</strong></h2><p>&nbsp;</p><p>&nbsp;</p><p>&nbsp;</p><p>&nbsp;</p><blockquote><p><span style="color: #ff0000;">Servidor HTTP - Disciplina de Redes de Computadores - UFSJ</span></p></blockquote><p>&nbsp;</p><p></p><p>&nbsp;</p></html>'.encode('utf-8')

        
    final_resposta = cabecalho.encode('utf-8')
    final_resposta += resposta
    conexao.send(final_resposta) # Envio da resposta final ao cliente
    
    conexao.close() # Fecha a conexao
