#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2020
# Aplicação
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

# Esta é a camada superior, de aplicação do seu software de comunicação serial UART.
# para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
#import numpy as np
import sys

# Voce deverá descomentar e configurar a porta com através da qual ira fazer comunicação.
# Para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# Se estiver usando windows, o gerenciador de dispositivos informa a porta.

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)

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
    
    if len(lista_head) != 0:
    
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
    
    else:
        return (0, 0, 0, 0, 0, 0, 0)
  
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
        # Declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # para declarar esse objeto é o nome da porta.
        com1 = enlace('COM4')
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        # Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print(f'com1 = {com1}')
        print("-"*30)
        
        # Aqui você deverá gerar os dados a serem transmitidos. 
        # Seus dados a serem transmitidos são uma lista de bytes a serem transmitidos.
        
        # Carregando dados para transmissão
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
    
        print("Preparando lista com listas de payloads para serem enviados")
        print("-"*30)
        
        i_lista_inicial = 0
        lista_payloads = []
        # PAYLOAD - de 0 a 114 bytes
        for i in range(total_pacotes):
            if i < total_pacotes-1:
                i_lista_final = i_lista_inicial + tamanho_max_payload
                lista_bytes_envio = img_bytes_lista[i_lista_inicial:i_lista_final]
                i_lista_inicial = i_lista_final
                lista_payloads.append(lista_bytes_envio)
            elif cont == total_pacotes-1:
                lista_bytes_envio = img_bytes_lista[i_lista_inicial:]
                lista_payloads.append(lista_bytes_envio)
            
        # Iniciando comunicação com Server
        print("Iniciando comunicação")
        print("-"*30)
        inicia = False
        while not inicia:
            print("Tentando enviar handshake para o Server")
            print("-"*30)
            # Handshake
            # O Client precisa mandar um handshake para saber se o Server está online
            # Criando head e eop do pacote Handshake (sem payload)
            handshake = datagram_head(1, total_pacotes, 0, 0, 0, 0) + datagram_eop()
            com1.sendData(handshake)
            time.sleep(0.01)
            time.sleep(5)
            
            rxBuffer_head = com1.getData(10)
            
            head_recebido = decifra_head(rxBuffer_head)
            
            if head_recebido[0] == 2:
                break
            else:
                pass
        
        cont = 1
        #cont_anterior = 0
        print("A transmissão vai começar")   
        print("-"*30)
        while cont <= total_pacotes:
            print(f"Número do pacote atual: {cont}")
            print("-"*30)
                
            '''DATAGRAMA
            
            HEAD - 10 bytes
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
            # PAYLOAD - 0 a 114 bytes
            # Array de bytes que compõem a imagem que está sendo enviada
            txBuffer_payload, tamanho_payload = datagram_payload(lista_payloads[cont-1])
                
            # HEAD - 10 bytes
            txBuffer_head = datagram_head(3, total_pacotes, cont, tamanho_payload, 0, 0)

            # EOP - 4 bytes
            txBuffer_eop = datagram_eop()
            
            # Enviando datagrama completo
            print("Transmitindo Datagrama")
            print("-"*30)
            txBuffer = txBuffer_head + txBuffer_payload + txBuffer_eop
            com1.sendData(txBuffer)
            time.sleep(0.01)
            
            # Tentativa de receber a mensagem de feedback do Server
            momento_inicial_1 = time.perf_counter()
            momento_inicial_2 = momento_inicial_1
            recebeu_mensagem = False
            while not recebeu_mensagem:
                # Tenta receber mensagem do tipo 4
                rxBuffer_head, nRx = com1.getData(10)
                time.sleep(0.01)
                
                if nRx == 0:
                    # Quer dizer que não recebeu mensagem
                    momento_final_1 = time.perf_counter()
                    timer_1 = momento_final_1 - momento_inicial_1
                    print("Não recebeu mensagem")
                    if timer_1 > 5:
                        print("Transmitindo novamente o Datagrama")
                        print("-"*30)
                        com1.sendData(txBuffer)
                        time.sleep(0.01)
                        momento_inicial_1 = time.perf_counter()
                      
                    momento_final_2 = time.perf_counter()
                    timer_2 = momento_final_2 - momento_inicial_2
                    if timer_2 > 20:
                        print("Time Out")
                        # Envia mensagem de time out
                        txBuffer_timeout_head = datagram_head(5, 0, 0, 0, 0, 0)
                        txBuffer_timeout_eop = datagram_eop()
                        txBuffer = txBuffer_timeout_head + txBuffer_timeout_eop
                        com1.sendData(txBuffer)
                        time.sleep(0.01)
                        print("Encerrando comunicação :-(")
                        com1.disable()
                        sys.exit()
                    
                    else:
                        # Tenta captar mensagem de erro do Server
                        rxBuffer_head, nRx = com1.getData(10)
                        time.sleep(0.01)
                        if nRx == 0:
                            pass
                        else:
                            head_decifrado = decifra_head(rxBuffer_head)                        
                            rxBuffer_payload = com1.getData(head_decifrado[3])
                            rxBuffer_eop, nRx = com1.getData(4)
                            if head_decifrado[0] == 6:
                                cont = head_decifrado[4]
                                print("Transmitindo o Datagrama solicitado")
                                print("-"*30)
                                
                                # PAYLOAD - 0 a 114 bytes
                                # Array de bytes que compõem a imagem que está sendo enviada
                                txBuffer_payload, tamanho_payload = datagram_payload(lista_payloads[cont-1])
                                    
                                # HEAD - 10 bytes
                                txBuffer_head = datagram_head(3, total_pacotes, cont, tamanho_payload, 0, 0)

                                # EOP - 4 bytes
                                txBuffer_eop = datagram_eop()
                                
                                # Enviando datagrama completo
                                print("Transmitindo Datagrama")
                                print("-"*30)
                                txBuffer = txBuffer_head + txBuffer_payload + txBuffer_eop
                                com1.sendData(txBuffer)
                                time.sleep(0.01)
                                
                                # Resetando timers
                                momento_inicial_1 = time.perf_counter()
                                momento_inicial_2 = momento_inicial_1
                    
                else:
                    # Quer dizer que recebeu mensagem
                    # Continua captando os dados da mensagem
                    head_decifrado = decifra_head(rxBuffer_head)                        
                    time.sleep(0.01)
                    rxBuffer_payload = com1.getData(head_decifrado[3])
                    time.sleep(0.01)
                    rxBuffer_eop, nRx = com1.getData(4)
                    time.sleep(0.01)
                    cont += 1   
                    
            
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
