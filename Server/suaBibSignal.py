
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window



class signalMeu:
    def __init__(self):
        self.init = 0

    def generateSin(self, freq, amplitude, x, fs):
        # fs é a frequência de amostragem
        s = amplitude*np.sin(freq*x*2*np.pi)
        return s
    
    def calcFFT(self, signal, fs):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        N  = len(signal)
        W = window.hamming(N)
        T  = 1/fs
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(signal*W)
        return(xf, np.abs(yf[0:N//2]))

    def plotFFT(self, sinal, fs, nome):
        x,y = self.calcFFT(sinal, fs)
        plt.figure(f"{nome} - Fourier")
        plt.plot(x, np.abs(y))
        plt.title(f"{nome} - Fourier")
        plt.grid()
        plt.xlabel("Frequência (Hz)")
        plt.ylabel("Magnitude")
        # Magnitude é a intensidade do som 
        plt.savefig(f"{nome}.png")
        plt.show()
