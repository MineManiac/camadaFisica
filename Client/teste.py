# -*- coding: utf-8 -*-
"""
Created on Fri May  6 17:19:13 2022

@author: Renato
"""
import numpy as np
import soundfile as sf
from funcoes_LPF import *
import matplotlib.pyplot as plt

from scipy.fftpack import fft
from scipy import signal as window


import sounddevice as sd

import time


def calcFFT(signal, fs):
    # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
    N  = len(signal)
    W = window.hamming(N)
    T  = 1/fs
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    yf = fft(signal*W)
    return(xf, np.abs(yf[0:N//2]))

def plotFFT(signal, fs, nome):
    x,y = calcFFT(signal, fs)
    plt.figure(f"{nome}")
    plt.plot(x, np.abs(y))
    plt.title(f"Fourier")
    plt.grid()
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Magnitude")
    # Magnitude é a intensidade do som 
    #plt.savefig("Fourier.png")
    plt.show()
    
def generateSin(freq, amplitude, x, fs):
    # fs é a frequência de amostragem
    s = amplitude*np.sin(freq*x*2*np.pi)
    return s
    
    
data, samplerate = sf.read("RickRoll.wav")

n = len(data)

time = len(data)/samplerate

t = np.linspace(0, time, n)

print(samplerate)

data_filtrada = LPF(data, 2500, samplerate)

# =============================================================================
# 
# plotFFT(data, samplerate, "data")
# 
plotFFT(data_filtrada, samplerate, "data_filtrada")
# =============================================================================

# =============================================================================
# sd.play(data, samplerate)
# sd.wait()
# 
# time.sleep(1)
# 
# sd.play(data_filtrada, samplerate)
# sd.wait()
# =============================================================================

portadora = generateSin(13000, 1, t, samplerate)
plotFFT(portadora, samplerate, "portadora")
# =============================================================================
# plt.figure("Sinal portadora")
# plt.plot(x, portadora)
# plt.title(f"Sinal portadora")
# plt.grid()
# plt.xlabel("Tempo (s)")
# plt.ylabel("Amplitude")
# plt.xlim(0,0.002)
# #plt.savefig("SinaisSomados.png")
# plt.show()
# =============================================================================


modulado = np.array(data_filtrada) * np.array(portadora)
# =============================================================================
# 
# plt.figure("Sinal modulado")
# plt.plot(t, modulado)
# plt.title(f"Sinal modulado")
# plt.grid()
# plt.xlabel("Tempo (s)")
# plt.ylabel("Amplitude")
# 
# #plt.savefig("SinaisSomados.png")
# plt.show()
# =============================================================================


plotFFT(modulado, samplerate, "modulado")

# sd.play(modulado, samplerate)
# sd.wait()

maximo = 0
for p in modulado:
    p_modulo = abs(p)
    if p_modulo > maximo:
        maximo = p_modulo
        
normalizado = modulado/maximo
   
# =============================================================================
# plt.figure("Sinal normalizado")
# plt.plot(t, normalizado)
# plt.title(f"Sinal normalizado")
# plt.grid()
# plt.xlabel("Tempo (s)")
# plt.ylabel("Amplitude")
# plt.show() 
# =============================================================================
input("Aguardando:")
sd.play(normalizado, samplerate)
sd.wait()
