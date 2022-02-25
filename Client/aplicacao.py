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
from random import randint

comando_1 = b'\x00\xFF\x00\xFF'
comando_2 = b'\x00\xFF\xFF\x00'
comando_3 = b'\xFF'
comando_4 = b'\x00'
comando_5 = b'\xFF\x00'
comando_6 = b'\x00\xFF'

lista_bytes = [comando_1,comando_2,comando_3,comando_4,comando_5,comando_6]

# Funções para sortear um número de bytes que serão enviados
def quantidade_de_comandos():
    n = randint(10,30)
    return n

# Função que cria uma lista com N comandos e adicionados de forma aleatória
def cria_lista_comandos(n):
    lista_envio = []
    for i in range(n):
        j = randint(0,5)
        lista_envio.append(lista_bytes[j])
    
    return lista_envio

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace('COM4')
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print(com1)
        
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        print("Carregando comandos para transmissão:")
        print("-"*30)
        
        txBuffer = b''
        # Estamos usando o valor 5 em hexadecimal para representar quando um novo comando começa
        protocolo = b'\x05' 
        quant = quantidade_de_comandos()
        lista_comandos = cria_lista_comandos(n)
        for c in lista_comandos:
            n_bytes_comando = bytes([len(c)])
            # Envia mensagem composta por: PROTOCOLO + Número de bytes no comando em seguida + Comando
            txBuffer += protocolo + n_bytes_comando + c
            
        #finalmente vamos transmitir os dados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!
          
        print("A transmissao vai comecar")   
        print("-"*30)
        
        print("Transmitindo handshake")
        # Nosso handshake será um array com 1 byte referente ao tamanho do próximo array a ser enviado
        txBufferLen = bytes([len(txBuffer)])
        com1.sendData(np.asarray(txBufferLen)) 
        print("-"*30)
        # Faz uma pausa para deixar o outro computador receber 
        time.sleep(2)
        print("Transmitindo mensagem")
        # Transmitindo a mensagem que desejamos
        com1.sendData(np.asarray(txBuffer))
        
        
        
        print("A Recepção vai comecar")
        print("-"*30)
        #acesso aos bytes recebidos
        rxBuffer, nRx = com1.getData(1)
        
        print("recebeu RxBuffer")
        print("-"*30)
        
        # Transformando byte recebido no rxBuffer para int
        n_rxbuffer = int.from_bytes(rxBuffer, byteorder='big')
        
        if n_rxBuffer == quant:
            print("Sucesso! O servidor recebeu os comandos enviados")
        else:
            print("Falhou")
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
