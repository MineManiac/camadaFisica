#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import peakutils
import LPF from funcoes_LPF

#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def generateCarrier(freq, amplitude, x, fs):
    s = amplitude*np.sin(freq*x*2*np.pi)
    return (x, s)

def main():
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    signal = signalMeu()
    
    freqDeAmostragem = 44100
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = freqDeAmostragem#taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
   

    # faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    print("-"*10)
    print("A CAPTAÇÃO COMEÇARÁ EM 5")
    print("-"*10)
    time.sleep(1)
    print("4")
    print("-"*10)
    time.sleep(1)
    print("3")
    print("-"*10)
    time.sleep(1)
    print("2")
    print("-"*10)
    time.sleep(1)
    print("1")
    print("-"*10)
    time.sleep(1)
   
   #faca um print informando que a gravacao foi inicializada
    print("A gravação foi iniciada")
    print("-"*10)
    
   #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
   #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
   
    duration = 168729/freqDeAmostragem #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    numAmostras = freqDeAmostragem * duration
    
    
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    dados = []
    
    for i in audio:
        dados.append(i[0])
        
    

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    numPontos = len(dados)
    inicio = 0
    fim = duration
    
    t = np.linspace(inicio,fim,numPontos)
 
    ## Calcula Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(dados, freqDeAmostragem)
    
    ## Exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    plt.figure("Fourier Audio Recebido")
    plt.plot(xf,yf)
    plt.grid()
    plt.ylabel("Amplitude")
    plt.xlabel("Frequência(Hz)")
    plt.title('Fourier Audio Recebido')
    plt.savefig('fourierAudio.png')

    carrier = generateCarrier(13000,1,duration, freqDeAmostragem)
    
    
    #CALCULO DEMODULADO
    demodulado = np.array(dados) * np.array(carrier)
    xf, yf = signal.calcFFT(demodulado, freqDeAmostragem)
    
    ## Exibe o Fourier do sinal Demodulado. como saida tem-se a amplitude e as frequencias
    plt.figure("Fourier Audio Demodulado")
    plt.plot(xf,yf)
    plt.grid()
    plt.ylabel("Amplitude")
    plt.xlabel("Frequência(Hz)")
    plt.title('Fourier Audio Demodulado')
    plt.savefig('fourierDemodulado.png')
    
    
    #CALCULO FILTRADO
    filtrado = LPF(demodulado, 2500, freqDeAmostragem)
    xf, yf = signal.calcFFT(filtrado, freqDeAmostragem)
    
    sd.play(demodulado)
    
    
    ## Exibe o Fourier do sinal audio Filtrado. como saida tem-se a amplitude e as frequencias
    plt.figure("Fourier Audio Filtrado")
    plt.plot(xf,yf)
    plt.grid()
    plt.ylabel("Amplitude")
    plt.xlabel("Frequência(Hz)")
    plt.title('Fourier Audio Filtrado')
    plt.savefig('fourierFiltrado.png')
    
    sd.play(filtrado)
    
        
    # plot do grafico  áudio vs tempo!   
# =============================================================================
#     plt.figure("A(t)")
#     plt.plot(t,audio)
#     plt.grid()
#     plt.xlabel("Tempo")
#     plt.ylabel("Áudio")
#     plt.title('Audio no Tempo (tecla {})'.format(tecla))
# =============================================================================
    # plt.savefig('audio.png')
    
    
    

    
    
    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()
