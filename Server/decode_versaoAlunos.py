#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import peakutils

#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


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
   
    duration = 5 #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
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
    fim = 5
    
    t = np.linspace(inicio,fim,numPontos)

    # plot do grafico  áudio vs tempo!   
    plt.figure("A(t)")
    plt.plot(t,audio)
    plt.grid()
    plt.title('Audio no Tempo')
    
    
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(dados, freqDeAmostragem)
    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
    

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
   
    index = peakutils.indexes(yf, thres=0.25, min_dist=500)
    
    
    #printe os picos encontrados!
    #print(index)
    
    frequencias = []
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    for i in index:
        frequencia = int(xf[i])
        frequencias.append(frequencia)
        
        print("frequencia = {}".format(int(xf[i])))
    
    #print(frequencias)
    
    #print a tecla.
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
    
    for i in tecla_para_frequencias.keys():
        if tecla_para_frequencias[i] == frequencias:
            print(i)
        
    
    

    
  
    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()
