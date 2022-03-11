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
serialName = "COM3"                  # Windows(variacao de)

def datagram_head(n_pacote, total_pacotes, tamanho_payload):
    
    head = n_pacote.to_bytes(2, byteorder='big') + total_pacotes.to_bytes(2, byteorder='big') + tamanho_payload.to_bytes(2, byteorder='big') + (6 * bytes([0]))
   
    return head 

def datagram_payload(lista_bytes_envio):
    payload = b''
    tamanho_payload = len(lista_bytes_envio)
    for b in lista_bytes_envio:
        payload += b.to_bytes(1, byteorder='big')
        
    return payload, tamanho_payload

def datagram_eop():
    
    eop = (4 * bytes([11]))
    
    return eop
    
def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace('COM3')
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print(com1)
        
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        print("-"*30)
        print("Carregando dados para transmissão:")
        print("-"*30)
        
        imageR = "img/naorickroll.jpg"
        with open(imageR, 'rb') as file:
            img_bytes = file.read()
        img_bytes_lista = []
        for b in img_bytes:
            img_bytes_lista.append(b)
            
        img_bytes_len = len(img_bytes_lista)
        
        quantidade, resto = divmod(img_bytes_len, 114)
        
        print(quantidade, resto)
        
        total_pacotes = quantidade
        if resto > 0:
            total_pacotes += 1
                
        tentando = True
        while tentando:
            print("entrou no loop")
            print("-"*30)
            # Handshake
            # Primeiro o Client manda um handshake para saber se o Server está online
            handshake_head = datagram_head(0, total_pacotes, 0)
            handshake_eop = datagram_eop()
            # Primeiro manda o head
            handshake_head_txBuffer = handshake_head
            com1.sendData(handshake_head_txBuffer)
            time.sleep(0.01)
            # Depois manda o eop
            handshake_eop_txBuffer = handshake_eop
            com1.sendData(handshake_eop_txBuffer)
            time.sleep(0.01)
            
            # Agora o Client espera uma resposta do Server por 5 segundos
            handshake_rxBuffer_head, nRx = com1.getData(10)            
            
            if nRx == 0:
                resposta = input("Servidor inativo. Tentar novamente? S/N  ")
                print("-"*30)
                if resposta.lower() == 's':
                    pass
                else:    
                    print("Encerrando comunicação")
                    com1.disable()
                    sys.exit()
            else:
                tentando = False          
                handshake_rxBuffer_eop, nRx = com1.getData(4)
                
        
        n_pacote = 1
        i_lista_inicial = 0
        while n_pacote <= total_pacotes:  
            print("entrou no segundo loop")
            print(n_pacote)
            # PAYLOAD - de 0 a 114 bytes
            if n_pacote < total_pacotes:
                tamanho_payload = 114
            elif n_pacote == total_pacotes:
                tamanho_payload = resto+1
            
            i_lista_final = i_lista_inicial + tamanho_payload
            lista_bytes_envio = img_bytes_lista[i_lista_inicial:i_lista_final]
            i_lista_inicial = i_lista_final
            
            payload, tamanho_payload = datagram_payload(lista_bytes_envio)
                
            # HEAD - 10 bytes
            # Número do pacote 
            # Número total de pacotes que serão transmitidos
            # Tamanho do Payload desse pacote
            
            head = datagram_head(n_pacote, total_pacotes, tamanho_payload)

            # EOP - 4 bytes
            
            eop = datagram_eop()
            
            # Criação do pacote que vai ser enviado
            print("manda head")
            txBuffer_head = head
            com1.sendData(txBuffer_head)
            time.sleep(.01)
            
            print("manda payload")
            txBuffer_payload = payload
            com1.sendData(txBuffer_payload)
            time.sleep(.01)
            
            print("manda eop")
            txBuffer_eop = eop
            com1.sendData(txBuffer_eop)
            time.sleep(.01)
            
            n_pacote += 1
        
        
        """
        #print("txBuffer = {}".format(txBuffer))
        print("txBufferLen = {}".format(len(txBuffer)))
        print("-"*30)
        #finalmente vamos transmitir os dados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!
          
        print("A transmissão vai começar")   
        print("-"*30)
        time.sleep(1)
        
        # Nosso handshake será um array com 1 byte referente ao tamanho do próximo array a ser enviado
        txBufferLen = bytes([len(txBuffer)])
        print("Handshake = {}".format(txBufferLen))
        print("-"*30)
        print("Transmitindo handshake")
        print("-"*30)
        com1.sendData(np.asarray(txBufferLen))
        # Faz uma pausa para deixar o outro computador receber 
        time.sleep(1)
        print("Transmitindo mensagem")
        print("-"*30)
        # Transmitindo a mensagem que desejamos
        com1.sendData(np.asarray(txBuffer))
              
        
        print("A Recepção vai comecar")
        print("-"*30)
        #acesso aos bytes recebidos
        rxBuffer, nRx = com1.getData(1)
        
        if nRx == 0:
            print("Timeout de 10 segundos")
            print("-"*30)
            com1.disable()
        
        else:
            print("Recebeu RxBuffer")
            print("-"*30)
            
            # Transformando byte recebido no rxBuffer para int
            n_rxBuffer = int.from_bytes(rxBuffer, byteorder='big')
            print("Quantidade de bytes recebidos pelo Server = {}".format(n_rxBuffer))
            print("-"*30)
            print("Quantidade de bytes enviados pelo Client = {}".format(quant))
            print("-"*30)
            
            if n_rxBuffer == quant:
                print("Sucesso! O servidor recebeu os comandos enviados")
                print("-"*30)
            else:
                print("Falhou")
                print("-"*30)
                
            """
        # Encerra comunicação
        print("Comunicação encerrada")
        print("-"*30)
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
