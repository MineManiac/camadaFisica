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
#import numpy as np
import sys

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)

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
    crc_bytes = b''
    for i in lista_head[8:]:
        crc_bytes += bytes([i])     
        
    crc = int.from_bytes(crc_bytes, byteorder='big')
    
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
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print(f'com1 = {com1}')
        print("-"*30)
        
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmiti3os. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        print("Carregando dados para transmissão:")
        print("-"*30)
        
        imageR = "img/naorickroll.jpg"
        with open(imageR, 'rb') as file:
            img_bytes = file.read()
        img_bytes_lista = []
        for b in img_bytes:
            img_bytes_lista.append(b)
            
        img_bytes_len = len(img_bytes_lista)
        
        tamanho_max_payload = 114
        
        quantidade, resto = divmod(img_bytes_len, tamanho_max_payload)
       
        total_pacotes = quantidade
        if resto > 0:
            total_pacotes += 1
            
        print(f"Tamanho máximo de payload: {tamanho_max_payload}")
        print("-"*30)
        print(f"Quantidade de pacotes: {total_pacotes}")
        print("-"*30)
        print(f"Resto de Bytes para o último pacote: {resto}")
        print("-"*30)
        
        # Handshake
        # O Client precisa mandar um handshake para saber se o Server está online
        # Criando head e eop do pacote Handshake (sem payload)
        handshake_head = datagram_head(0, total_pacotes, 0)
        handshake_eop = datagram_eop()
        print("Entrou no loop para tentar conectar ao Server")
        print("-"*30)
        tentando = True
        while tentando:
            # Primeiro manda o head
            print("Transmitindo Head")
            print("-"*30)
            com1.sendData(handshake_head)
            time.sleep(0.01)
            # O Handshake não possui payload
            # Depois manda o eop
            print("Transmitindo EOP")
            print("-"*30)
            com1.sendData(handshake_eop)
            time.sleep(0.01)
            
            # Agora o Client espera uma resposta do Server por 5 segundos
            print("Esperando resposta do Server")
            print("-"*30)
            
            handshake_rxBuffer_head, nRx = com1.getData(10)   
            print(f"Handshake Head recebido: {handshake_rxBuffer_head}")
            print("-"*30)
            
            
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
                time.sleep(.01)
                print(f"Handshake EOP recebido: {handshake_rxBuffer_eop}")
                print("-"*30)
                
                
        # Se deu tudo certo na conexão com o Server, a transmissão se inicia
        print("A transmissão vai começar")   
        print("-"*30)
        time.sleep(1)
        
        print("Entrou no loop de envio dos pacotes com bytes da imagem. ")
        print("-"*30)
        n_pacote = 1
        i_lista_inicial = 0
        enviando = True        
        while enviando:
            print(f"Número do pacote atual: {n_pacote}")
            print("-"*30)
            # PAYLOAD - de 0 a 114 bytes
            if n_pacote < total_pacotes:
                i_lista_final = i_lista_inicial + tamanho_max_payload
                lista_bytes_envio = img_bytes_lista[i_lista_inicial:i_lista_final]
                i_lista_inicial = i_lista_final
            elif n_pacote == total_pacotes:
                print("Último pacote")
                print("-"*30)
                lista_bytes_envio = img_bytes_lista[i_lista_inicial:]
                
            # PAYLOAD
            # Array de bytes que compõem a imagem que está sendo enviada
            txBuffer_payload, tamanho_payload = datagram_payload(lista_bytes_envio)
                
            # HEAD - 10 bytes
            # Número do pacote 
            # Número total de pacotes que serão transmitidos
            # Tamanho do Payload desse pacote
            txBuffer_head = datagram_head(n_pacote, total_pacotes, tamanho_payload)

            # EOP - 4 bytes
            txBuffer_eop = datagram_eop()
            
            # Enviando pacote por partes
            print("Transmitindo Head")
            print("-"*30)
            com1.sendData(txBuffer_head)
            time.sleep(0.1)
            
            print("Transmitindo Payload")
            print("-"*30)
            com1.sendData(txBuffer_payload)
            time.sleep(0.01)
            
            print("Transmitindo EOP")
            print("-"*30)
            com1.sendData(txBuffer_eop)
            time.sleep(0.01)
            
            # Depois de mandar o pacote, o Client precisa receber um feedback do Server
            
            rxBuffer_head, nRx_h = com1.getData(10)
            print("Head recebido")
            print("-"*30)
            time.sleep(0.01)
            feedback_server = decifra_head(rxBuffer_head)
            time.sleep(0.01)
            print(f"feedback server = {feedback_server}")
            print("-"*30)
            
            """
            rxBuffer_payload, nRx_p = com1.getData(10)
            print("Payload recebido")
            print("-"*30)
            time.sleep(0.05)
            """
            rxBuffer_eop, nRx_e = com1.getData(4)
            print("EOP recebido")
            print("-"*30)
            time.sleep(0.01)
            
            # Se estiver tudo ok, o Server vai retornar no payload um byte com valor 1.
            # Dessa forma, o Client pode prosseguir para o próximo pacote.
            # Se algo estiver errado, o Server vai retornar no payload um byte com valor 0.
            # Dessa forma, o Client deve reenviar o pacote.
            # Quando o Server receber o último pacote, ele vai retornar no payload um byte com valor 2.
            # Dessa forma, o Client pode parar de enviar pacotes e ambos podem encerrar a transmissão.
            
            
            """
            if feedback_server == 1:
                n_pacote += 1
                
            elif feedback_server == 0:
                pass
            
            elif feedback_server == 2:
                enviando = False
            """
            
            if feedback_server == 1:
                print("Tudo ok, pode proseeguir com o envio do pacote")
                n_pacote += 1
            elif feedback_server == 0:
                print("Algo deu errado, precisa reenviar o pacote")
                enviando = False
            
            elif feedback_server == 2:
                print("Último pacote recebido")
                enviando = False
                
            print("-"*30)
            
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
