
#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from time import sleep


#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    
   
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # se voce quiser, pode usar a funcao de construção de senoides existente na biblioteca de apoio cedida. Para isso, você terá que entender como ela funciona e o que são os argumentos.
    # essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # o tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Seja razoável.
    # some as senoides. A soma será o sinal a ser emitido.
    # utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    
    
    print("Inicializando encoder")
    signal = signalMeu()
    # Amplitude do sinal
    amplitude = 1
    # Tempo de duração do sinal em segundos
    time = 5
    # Sample rate padrão
    fs = 44100
    # Você importou a bilioteca sounddevice como sd. 
    # Então os seguintes parâmetros devem ser setados:
    sd.default.samplerate = fs # Taxa de amostragem
    sd.default.channels = 2  # Você pode ter que alterar isso dependendo da sua placa
    #sd.default.device = 'digital output'
    
    print("Gerando Tons base")
    # Criando dicionário que relaciona teclas de 0 à 9 à listas com duas frequências (em Hertz) cada, referentes à tabela
    tecla_para_frequencias = {
        "0": [941, 1339],
        "1": [697, 1206],
        "2": [697, 1339],
        "3": [697, 1477],
        "4": [770, 1206],
        "5": [770, 1339],
        "6": [770, 1477],
        "7": [852, 1206],
        "8": [852, 1339],
        "9": [852, 1477]
        }
    
    tocar = True
    while tocar:
        
        print("Aguardando usuário")
        tecla_pressionada = input(f"Qual tecla deseja tocar? (Escolha valores de 1 à 9) ")
        #tecla_pressionada = "1"
        if tecla_pressionada == "10":
            tocar = False
            # Dá pra tentar colocar um sys.exit() ou semelhante...
            # Mas como tá funfando bunitinho, deixa do jeito que tá e dane-se
            
        else:
            # Vai selecionar a tecla no dicionário, obter as frequências 
            # que compõem o sinal a ser enviado e somar as senoides de cada frequência
            # para obter o tom que será tocado
        
            frequencias = tecla_para_frequencias[tecla_pressionada]
            x, seno1 = signal.generateSin(frequencias[0], amplitude, time, fs)
            x, seno2 = signal.generateSin(frequencias[1], amplitude, time, fs)
            sinal = seno1 + seno2                
            
            print(f"Executando as senoides (emitindo o som referente à tecla {tecla_pressionada})")
            # Toca áudio
            sd.play(sinal, fs)
            
            # Aguarda fim do áudio
            sd.wait()
            
            # Exibe gráficos do sinal das senóides somadas e da transformada de fourier
            
            # Plot sinal
            signal.plotSinais(sinal, x, tecla_pressionada)
            
            # Plot Fourier
            signal.plotFFT(sinal, fs, tecla_pressionada)
    

if __name__ == "__main__":
    main()
