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


# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)


def decifra_head(head):
    lista = []
    
    for b in head:
        lista.append(b)
    
    n_pacote = lista[:2]
    total_pacotes = lista[2:4]
    tamanho_payload = lista[4:5]
    
    decifrado_n_pacote = int.from_bytes(n_pacote, byteorder='big')
    decifrado_total_pacotes = int.from_bytes(total_pacotes, byteorder='big')
    decifrado_tamanho_payload = int.from_bytes(tamanho_payload, byteorder='big')
    
    
    
    print('{} NUMERO PACOTE / {} TOTAL DE PACOTES'.format(decifrado_n_pacote, decifrado_total_pacotes))
    print('----------------')
    print('Bytes do Payload {}'.format(decifrado_tamanho_payload))
    
    return(decifrado_tamanho_payload, decifrado_n_pacote, decifrado_total_pacotes)

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
                
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        print("A Recepção vai comecar")
        print("-"*30)
        # Nesse momento, desejamos receber apenas um byte, que é o handshake.
        
        handshake_rxBuffer,_ = com1.getData(14)
        
        decifrado_tamanho_payload, decifrado_n_pacote, decifrado_total_pacotes = decifra_head(handshake_rxBuffer)
        
        resposta = input('Mandar resposta? S/N    ')
        
        if resposta.lower() == "s":
            
            head = bytes([0]) * 10
            eop = bytes([0]) * 4
            
            handshake_txBuffer = head + eop
            com1.sendData(handshake_txBuffer)
            
            
        else:
            print("resposta não enviada")
        
        
        
        #print(decifrado_tamanho_payload, decifrado_n_pacote, decifrado_total_pacotes)
        
        
        print("o que recebeu {}".format(rxBuffer))
        # Número recebido pelo rxBuffer, que é o tamanho da próxima mensagem que receberemos
        tamanho_mensagem = int.from_bytes(rxBuffer, byteorder='big')
        print("Quantos bytes tem a próxima mensagem {}".format(tamanho_mensagem))
        
        rxBuffer,_ = com1.getData(tamanho_mensagem)
        #print("mensagemLida {}".format(rxBuffer))
        sRxBuffer = str(rxBuffer)
        #print("stringBuffer {}".format(sRxBuffer))
        quant_comandos_recebidos = len(sRxBuffer.split("\\x05"))- 1

        print("quantidade de comandos recebidos {}".format(quant_comandos_recebidos))

        #acesso aos bytes recebidos
       
        print("Carregando a quantidade de Bytes recebida para transmissão:")
        print("-"*30)
        
        txBuffer = quant_comandos_recebidos
         
        print("A transmissao vai comecar")
        #txBuffer = #dados
        txBuffer = bytes([txBuffer])
        
        #print("conexao desligada - Teste timeout do cliente")
        #com1.disable()
        
        com1.sendData(np.asarray(txBuffer))
        time.sleep(1)
        
        print("-"*30)
    
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