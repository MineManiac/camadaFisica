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
serialName = "COM4"                  # Windows(variacao de)


def decifra_head(head):
    print(head)
    lista = []
    
    for b in head:
        lista.append(b)
    
    n_pacote = lista[:2]
    #print(n_pacote)
    total_pacotes = lista[2:4]
    #print(total_pacotes)
    tamanho_payload = lista[4:6]
    #print(tamanho_payload)
        
    decifrado_n_pacote = int.from_bytes(n_pacote, byteorder='big')
    decifrado_total_pacotes = int.from_bytes(total_pacotes, byteorder='big')
    #print('{} NUMERO PACOTE / {} TOTAL DE PACOTES'.format(decifrado_n_pacote, decifrado_total_pacotes))
    #print('----------------')
    decifrado_tamanho_payload = int.from_bytes(tamanho_payload, byteorder='big')
   # print('Bytes do Payload {}'.format(decifrado_tamanho_payload))
    
    
   
    
    
    
    return(decifrado_tamanho_payload, decifrado_n_pacote, decifrado_total_pacotes)

def datagram_head(tipo, total_pacotes, n_pacote, ,tamanho_payload, pacote_erro, pacote_sucesso):
    
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
        com1 = enlace('COM4')
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        time.sleep(.2)
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print(com1)
                
        
        print("A Recepção do Handshake vai comecar")
        print("-"*30)
        
        #time.sleep(30)
        
        # Recebe Handshake do cliente
        handshake_rxBuffer_head,_ = com1.getData(10)
        print(handshake_rxBuffer_head)
        
        # Decifra o head para saber se é handshake ou n
        decifrado_tamanho_payload, decifrado_n_pacote, decifrado_total_pacotes = decifra_head(handshake_rxBuffer_head)
        
        # Tamanho do payload, ja que no handshake o valor é 0, não precisa de get data
        handshake_rxBuffer_payload = decifrado_tamanho_payload
        
        #EOP do handshake
        handshake_rxBuffer_eop = com1.getData(4)
        
        if handshake_rxBuffer_payload == 0:
            #Resposta para o cliente, enviando Head 10 bytes, Payload 0 bytes, EOP 4 bytes
             print("A transmissao Handshake vai comecar vai comecar")
             print("-"*30)
             head = bytes([0]) * 10
             
             com1.sendData(head)
             time.sleep(.01)
             
             eop = bytes([0]) * 4
             com1.sendData(eop)
             time.sleep(.01)
             com1.rx.clearBuffer()
             
             
             
             
             
        else:
            com1.disable()
            sys.exit()
        
        
        #Pós HANDSHAKE
        
        #RICKROLL EM BYTES
        imagem_recebida = b''
        
        print("A Recepção do Arquivo vai comecar")
        print("-"*30)
        
        #LOOP PEGANDO OS DADOS RECEBIDOS
        while decifrado_n_pacote < decifrado_total_pacotes:
            com1.rx.clearBuffer()
            time.sleep(0.01)
         
            
            rx_buffer_head,_= com1.getData(10)
            
            n_pacote_anterior = decifrado_n_pacote
            print("pacote anterior {}".format(n_pacote_anterior))
            
            decifrado_tamanho_payload, decifrado_n_pacote, decifrado_total_pacotes = decifra_head(rx_buffer_head)
            print("pacote de agora {}".format(decifrado_n_pacote))
            
            rx_buffer_payload, size_payload = com1.getData(decifrado_tamanho_payload)
            
            #caso o envio do pacote seja fora de ordem
            if (n_pacote_anterior - (decifrado_n_pacote - 1)) < 0:
                print("ERRO!!! ENVIO DO PACOTE ESTÁ  FORA DE ORDEM - ENCERRANDO COMUNICACAO")
                print("-"*30)
                
                x= 0
                #Mandando Datagrama Falando que o payload está errado
                head = bytes([0]) * 4 + x.to_bytes(2, byteorder='big') + bytes([0]) * 4
                
                com1.sendData(head)
                time.sleep(.1)
                
                eop = bytes([0]) * 4
                com1.sendData(eop)
                time.sleep(.1)
                
                com1.disable()
                sys.exit()
                
            
            
            
            # Caso o tamanho do payload do head for diferente do payload recebido
            elif size_payload != decifrado_tamanho_payload:
                print("ERRO!!! ENVIO O TAMANHO DO PAYLOAD RECEBIDO ESTÁ DIFERENTE DO QUE FOI MANDADO NO HEAD")
                print("-"*30)
                x= 0
                #Mandando Datagrama Falando que o payload está errado
                head = bytes([0]) * 4 + x.to_bytes(2, byteorder='big') + bytes([0]) * 4
                com1.sendData(head)
                
                time.sleep(.1)
                
                eop = bytes([0]) * 4
                com1.sendData(eop)
                time.sleep(.1)
                
                com1.disable()
                sys.exit()
                
                
            elif decifrado_n_pacote >= decifrado_total_pacotes:
                #Mandando Pacote falando que chegou no fim
                x = 2
                head = bytes([0]) * 4 + x.to_bytes(2, byteorder='big') + bytes([0]) * 4
                
                com1.sendData(head)
                time.sleep(.01)
                
                eop = bytes([0]) * 4
                com1.sendData(eop)
                time.sleep(.01)
                imagem_recebida += rx_buffer_payload
                
                break
        
        
            else:
                #Mandando Datagrama Falando que o payload está certo
                x = 1
                head = bytes([0]) * 4 + x.to_bytes(2, byteorder='big') + bytes([0]) * 4
                
                com1.sendData(head)
                time.sleep(.1)
                
                eop = bytes([0]) * 4
                com1.sendData(eop)
                time.sleep(.01)
            
            
                #concatenando bytes do payload para a imagem
                imagem_recebida += rx_buffer_payload
   
            
            
            print("NUMERO PACOTE {} / TOTAL DE PACOTE {}".format(decifrado_n_pacote, decifrado_total_pacotes))
            print("-"*30)
            
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