 # Cliente HTTP

# Importanto os modulos necessarios
import socket
import sys  

#O endereco do servidor sera informado como argumento no terminal
servidor = sys.argv[1]
porta = 8090  # Porta em que o servidor HTTP responde

# Printando a criacao do socket
print('# Criando o socket')

# Criando o socket. Caso tenha problema printa uma mensagem ao usuario
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('A criacao do socket falhou')
    sys.exit()

# Conectando ao servidor HTTP. Printando essa informacao
print('# Conectando ao servidor, ' + servidor + ' (' + servidor + ')')
s.connect((servidor , porta))

# Enviando uma requisicao GET ao servidor HTTP
print('# Enviando a requisicao')

# Envio do segundo argumento no terminal como parte do endereco da pagina (arquivo requisitado)
requisicao_usuario = sys.argv[2]

# Requisicao GET do arquivo solicitado utilizando o protocolo HTTP versao 1.1
requisicao = 'GET ' +str(requisicao_usuario)+ ' HTTP/1.1\r\n\r\n'

# Codificando a requisicao
requisicao_encode = requisicao.encode('utf-8')

# Envio da requisicao ja codificada. Caso nao seja possivel eh dado a mensagem que falhou o envio
try:
    s.sendall(requisicao_encode)
except socket.error:
    print ('Envio falhou!!')
    sys.exit()

# Recebimento dos dados solicitados, decodificando a mensagem. Printando essa informacao
print('# Recebido os dados do servidor')
mensagem_resposta = s.recv(1024).decode('utf-8')

# Printando a mensagem em tela
print(mensagem_resposta)


