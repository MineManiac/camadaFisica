#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


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