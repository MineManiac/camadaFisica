#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################

'''DATAGRAMA

h0 – tipo de mensagem
h1 – livre
h2 – livre
h3 – número total de pacotes do arquivo
h4 – número do pacote sendo enviado
h5 – se tipo for handshake:id do arquivo
h5 – se tipo for dados: tamanho do payload
h6 – pacote solicitado para recomeço quando a erro no envio.
h7 – último pacote recebido com sucesso.
h8 – h9 – CRC
PAYLOAD – variável entre 0 e 114 bytes. Reservado à transmissão dos arquivos.
EOP – 4 bytes: 0xAA 0xBB 0xCC 0xDD


TIPO 1 - HANDSHAKE h0 CLIENTE SERVIDOR- 1, IDENTIFICADOR DO SERVIDOR A GENTE ESCOLHE PODE SER 1, PRECISA CONTER O NUMERO TOTAL DE PACOTES 
TIPO 2 - RESPOSTA DO SERVIDOR CLIENTE h0 - 2, id tipo 1 deve ser correto
TIPO 3 - MANDAR DADOS CLIENTE SERVIDOR h0 - 3, Payload, numero do pacote, numero total de pacotes
TIPO 4 - CHECANDO DADOS PARA VER SE ESTÁ CERTO SERVIDOR CLIENTE h0 - 4 - verificar pacote, 
checar eop para ver se está no lugar certo. Enviar para o cliente o numero do pacote checado.

TIPO 5 - Mensagem de Timeout q é enviado, ambos os lados h0 - 5, é enviado quando excede o tempo encerrando a comunicação

TIPO 6 - Mensagem de erro SERVIDOR CLIENTE h0 - 6, tipo 3 inválida, bytes faltando, fora do formato, pacote errado esperado pelo servidor.
Contém o número correto do pacote esperado pelo servidor h6, orientando o cliente para o reenvio. 


'''

#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 

from enlace import *
import time
import numpy as np
import sys


# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)


def decifra_head(head):
    lista_head = list(head)
    
    tipo_mensagem = lista_head[0]
    numero_total_pacotes = lista_head[3]
    numero_pacote = lista_head[4]
    tamanho_payload = lista_head[5]
    # O lista_head[6], é o número do pacote que o Server está solicitando para mandar novamente
    pacote_solicitado = lista_head[6]
    # O lista_head[7], é o número do último pacote recebido com sucesso pelo Server
    ultimo_pacote = lista_head[7]
    # Os elementos de lista_head[8] e lista_head[9] são os CRC
    crc_bytes = b''
    for i in lista_head[8:]:
        crc_bytes += bytes([i])     
        
    crc = int.from_bytes(crc_bytes, byteorder='big')
    
    return(tipo_mensagem, numero_total_pacotes, numero_pacote, tamanho_payload, pacote_solicitado, ultimo_pacote, crc)

def datagram_head(tipo, total_pacotes, n_pacote, tamanho_payload, pacote_erro, pacote_sucesso):
    
    h0 = tipo.to_bytes(1, byteorder='big')#tipo mensagem
    h1 = b'\x00'
    h2 = b'\x00'
    h3 = total_pacotes.to_bytes(1,byteorder='big')
    h4 = n_pacote.to_bytes(1,byteorder='big')
    h5 = tamanho_payload.to_bytes(1,byteorder='big')
    h6 = pacote_erro.to_bytes(1,byteorder='big')#pacote solicitado para reenvio caso erro
    h7 = pacote_sucesso.to_bytes(1,byteorder='big')
    h8 = b'\x00'
    h9 = b'\x00'
    
    
    
    head = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9
   
    return head 

def datagram_payload(lista_bytes_envio):
    payload = b''
    tamanho_payload = len(lista_bytes_envio)
    for b in lista_bytes_envio:
        payload += b.to_bytes(1, byteorder='big')
        
    return payload, tamanho_payload

def datagram_eop():
    
    eop = b'\xAA\xBB\xCC\xDD'
    
    return eop

def decifra_head(head):
    lista_head = list(head)
    
    tipo_mensagem = lista_head[0]
    numero_total_pacotes = lista_head[3]
    numero_pacote = lista_head[4]
    tamanho_payload = lista_head[5]
    # O lista_head[6], é o número do pacote que o Server está solicitando para mandar novamente
    pacote_solicitado = lista_head[6]
    # O lista_head[7], é o número do último pacote recebido com sucesso pelo Server
    ultimo_pacote = lista_head[7]
    # Os elementos de lista_head[8] e lista_head[9] são os CRC
    crc = lista_head[8:10]
    
    return(tipo_mensagem, numero_total_pacotes, numero_pacote, tamanho_payload, pacote_solicitado, ultimo_pacote, crc)

def checa_eop(eop):
    lista_eop = list(eop)
    eop_int_correto = [170, 187, 204, 221]
    
    byte1_int = int.from_bytes(lista_eop[0], byteorder='big')
    byte2_int = int.from_bytes(lista_eop[1], byteorder='big')
    byte3_int = int.from_bytes(lista_eop[2], byteorder='big')
    byte4_int = int.from_bytes(lista_eop[3], byteorder='big')
    
    if (eop_int_correto[0] == byte1_int) and (eop_int_correto[1] == byte2_int) and (eop_int_correto[2] == byte3_int) and (eop_int_correto[3] == byte4_int):
        return True
    else:
        return False
    


def main():
    try:
        
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace('COM3')
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        time.sleep(.2)
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print(com1)
        
        
        print("A Recepção do Handshake vai comecar")
        print("-"*30)
        
        
        
        #time.sleep(30)
        
        
        
        ocioso = True
        
        while ocioso:
        print("Está OCIOSO")
        print("-"*30)
        
        # Recebe Handshake do cliente
        tipo1_head,_ = com1.getData(10)
        print(tipo1_head)
        
        # Decifra o head para saber se é handshake ou n
        tipo_mensagem, numero_total_pacotes, numero_pacote, tamanho_payload, pacote_solicitado, ultimo_pacote, crc = decifra_head(tipo1_head)
        
        if tipo_mensagem == 1:
            #EOP do handshake
            tipo1_eop,_= com1.getData(4)
            checa = checa_eop(tipo1_eop)
            
            if checa_eop == True:
                ocioso = False
                time.sleep(1)
            else:
                pass
        else:
            time.sleep(1)
            pass
        
        #Pós conferir HANDSHAKE        
        
        
        print("Mandando Mensagem tipo 2")
        print("-"*30)
        mensagem_tipo2 = datagram_head(2, numero_total_pacotes, 0, tamanho_payload, 0, 0) + datagram_eop()
        com1.sendData(mensagem_tipo2)
        time.sleep(.01)
        
        
        
        
        print("A Recepção do Arquivo vai comecar")
        print("-"*30)
        
        
        
        #RICKROLL EM BYTES
        imagem_recebida = b''
        
        cont = 1

        #LOOP PEGANDO OS DADOS RECEBIDOS
        while contador <= numero_total_pacotes:
            
            print("NUMERO PACOTE {} / TOTAL DE PACOTE {}".format(cont, numero_total_pacotes))
            print("-"*30)
            
            
            timer1 = time.perf_counter()
            timer2 = time.perf_counter()
            
            pegou_dados = False
            
            while not pegou_dados:
                head,size= com1.getData(10)
                
                if (head == b'\00') and (size == 1):
                    print('Entrou no caso de Passar 2 segundos')
                    print('-'*30)
                    
                    mensagem_tipo4 = datagram_head(4, 0, 0, 0, 0, cont-1) + datagram_eop()
                    com1.sendData(mensagem_tipo4)
                    time.sleep(0.01)
                
                elif (head == b'\FF') and (size == 1):
                    print('Entrou no caso de Passar 20 segundos')
                    print('-'*30)
                    
                    ocioso = True
                    mensagem_tipo5 = datagram_head(5, 0, 0, 0, 0, 0) + datagram_eop()
                    com1.sendData(mensagem_tipo5)
                    time.sleep(0.01)
                    com1.disable()
                    sys.exit()
                    
                    
                elif (size == 10):
                    print('PEGOU DADOS TRUE')
                    print('-'*30)
                    pegou_dados = True
            
            
            tipo, numero_total_pacotes, numero_pacote, payload, pacote_solicitado, ultimo_pacote, crc = decifra_head(head)
            
            if numero_pacote == cont:
                if tipo == 3:
                    print('É TIPO 3')
                    print('-'*30)
                    
                    payload_tipo3,_= com1.getData(payload)
                    
                    eop,_ = com1.getData(4)
                    
                    eop_correto = checa_eop(eop)
                    
                    #bytes faltando, fora do formato, pacote errado esperado pelo servidor.
                    if eop_correto == True:
                        print('EOP ESTÁ CORRETO')
                        print('-'*30)
                        imagem_recebida += payload_tipo3
                        
                        mensagem_tipo4 = datagram_head(4, 0, 0, 0, 0, cont) + datagram_eop()
                        com1.sendData(mensagem_tipo4)
                        time.sleep(0.01)
                        
                        cont += 1
                        
                    if eop_correto == False:
                        print('EOP ESTÁ ERRADO, FORA DE FORMATO, PODE HAVER BYTES FALTANDO')
                        print('-'*30)
                        
                        mensagem_tipo6 = datagram_head(6, 0, 0, 0, cont, 0) + datagram_eop()
                        com1.sendData(mensagem_tipo6)
                        time.sleep(0.01)
                        
                        com1.rx.clearBuffer()
                        time.sleep(0.01)
                        
                if tipo == 5:
                    print('É TIPO 5')
                    print('TIMEOUT CLIENT')
                    print('-'*30)
                    
                    time.sleep(0.01)
                    com1.disable()
                    sys.exit()
                
                else:
                    print('TIPO DA MENSAGEM ESTÁ ERRADA : {}'.format(tipo))
                    print('-'*30)
                    time.sleep(0.01)
                    com1.disable()
                    sys.exit()
            else:
                print("Numero do PACOTE Está ERRADO")
                print('-'*30)
                
                mensagem_tipo6 = datagram_head(6, 0, 0, 0, cont, 0) + datagram_eop()
                com1.sendData(mensagem_tipo6)
                time.sleep(0.01)
                
                com1.rx.clearBuffer()
                time.sleep(0.01)
                
                

            
            
            
        #Quando chegar no ultimo pacote sai do while                     
            
        #print(int.from_bytes(imagem_recebida, byteorder='big'))
        write_image = "imgs/naorickrollcopia.jpg"
        f = open(write_image, "wb")
        f.write(imagem_recebida)
        f.close()
        
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()