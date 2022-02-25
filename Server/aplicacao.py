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
serialName = "COM5"                  # Windows(variacao de)


def main():
    try:
        
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace('COM5')
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print(com1)
                
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        print("A Recepção vai comecar")
        print("-"*30)
        # Nesse momento, desejamos receber apenas um byte, que é o handshake.
        
        rxBuffer,_ = com1.getData(1)
        print("o que recebeu {}".format(rxBuffer))
        # Número recebido pelo rxBuffer, que é o tamanho da próxima mensagem que receberemos
        tamanho_mensagem = int.from_bytes(rxBuffer, byteorder='big')
        print("Quantos comandos tem a próxima mensagem {}".format(tamanho_mensagem))
        
        rxBuffer,_ = com1.getData(tamanho_mensagem)
        print("mensagemLida {}".format(rxBuffer))
        sRxBuffer = str(rxBuffer)
        print("stringBuffer {}".format(sRxBuffer))
        quant_comandos_recebidos = len(sRxBuffer.split("\\x05")) - 1
        quant_comandos_recebidos += 1
        print("quantidade de comandos recebidos {}".format(quant_comandos_recebidos))

        #acesso aos bytes recebidos
       
        print("Carregando a quantidade de Bytes recebida para transmissão:")
        print("-"*30)
        
        txBuffer = quant_comandos_recebidos
         
        print("A transmissao vai comecar")
        #txBuffer = #dados
        txBuffer = bytes([txBuffer])
        com1.sendData(np.asarray(txBuffer))
        
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
