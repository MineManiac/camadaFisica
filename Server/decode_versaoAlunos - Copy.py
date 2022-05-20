#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import peakutils
from funcoes_LPF import LPF
import time
import soundfile as sf

#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def generateCarrier(freq, amplitude, x, fs):
    s = amplitude*np.sin(freq*x*2*np.pi)
    return s

def main():
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    signal = signalMeu()
    
    freqDeAmostragem = 44100
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = freqDeAmostragem#taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
   

    duration = 168729/freqDeAmostragem #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    #numAmostras = freqDeAmostragem * duration
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)


    dados, _ = sf.read("nevergonna.wav")
        
    

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    numPontos = len(dados)
    inicio = 0
    fim = duration
    
    t = np.linspace(inicio,fim,numPontos)
 
    ## Calcula Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    carrier = signal.generateSin(13000, 1, t, freqDeAmostragem)
    
    demodulado = np.array(dados) * np.array(carrier)
    
    xf, yf = signal.calcFFT(demodulado, freqDeAmostragem)
    
    ## Exibe o Fourier do sinal Demodulado. como saida tem-se a amplitude e as frequencias
    plt.figure("Fourier Audio Demodulado Arquivo")
    plt.plot(xf,yf)
    plt.grid()
    plt.ylabel("Amplitude")
    plt.xlabel("Frequência(Hz)")
    plt.title('Fourier Audio Demodulado')
    plt.savefig('fourierDemoduladoArquivo.png')
    
    LPF(demodulado, 2500, freqDeAmostragem)
    
    #CALCULO FILTRADO
    filtrado = LPF(demodulado, 2500, freqDeAmostragem)
    xf, yf = signal.calcFFT(filtrado, freqDeAmostragem)
    

    ## Exibe o Fourier do sinal audio Filtrado. como saida tem-se a amplitude e as frequencias
    plt.figure("Fourier Audio Filtrado Arquivo")
    plt.plot(xf,yf)
    plt.grid()
    plt.ylabel("Amplitude")
    plt.xlabel("Frequência(Hz)")
    plt.title('Fourier Audio Filtrado')
    plt.savefig('fourierFiltradoArquivo.png')
    
    print("tocando audio")
    sd.play(filtrado, freqDeAmostragem)
    sd.wait()
    
    
    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()
