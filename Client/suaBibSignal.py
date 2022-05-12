
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window



class signalMeu:
    def __init__(self):
        self.init = 0

    def generateSin(self, freq, amplitude, time, fs):
        # fs é a frequência de amostragem
        n = time*fs
        x = np.linspace(0.0, time, n)
        s = amplitude*np.sin(freq*x*2*np.pi)
        return (x, s)

    def calcFFT(self, signal, fs):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        N  = len(signal)
        W = window.hamming(N)
        T  = 1/fs
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(signal*W)
        return(xf, np.abs(yf[0:N//2]))

    def plotFFT(self, signal, fs, tecla_pressionada):
        x,y = self.calcFFT(signal, fs)
        plt.figure("Fourier")
        plt.plot(x, np.abs(y))
        plt.title(f"Fourier (tecla {tecla_pressionada})")
        plt.grid()
        plt.xlabel("Frequência (Hz)")
        plt.ylabel("Magnitude")
        # Magnitude é a intensidade do som 
        plt.savefig("Fourier.png")
        plt.show()
        
    def plotSinais(self, signal, x_axis, tecla_pressionada):
        plt.figure("Sinais Somados")
        plt.plot(x_axis, signal)
        plt.title(f"Sinais Somados (tecla {tecla_pressionada})")
        plt.grid()
        plt.xlabel("Tempo (s)")
        plt.ylabel("Amplitude")
        plt.xlim(0,0.02)
        plt.savefig("SinaisSomados.png")
        plt.show()
