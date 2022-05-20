
import numpy as np
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

    def calcFFT(self, sinal, fs):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        N  = len(sinal)
        W = window.hamming(N)
        T  = 1/fs
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(sinal*W)
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
        
    def plotSinal(self, sinal, x_axis, nome):
        plt.figure(f"{nome} - Sinal no Tempo")
        plt.plot(x_axis, sinal)
        plt.title(f"{nome} - Sinal no Tempo")
        plt.grid()
        plt.xlabel("Tempo (s)")
        plt.ylabel("Amplitude")
        plt.savefig(f"{nome}.png")
        plt.show()
        
# =============================================================================
#     def filtro(self, y, samplerate, cutoff_hz):
#       # https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html
#         nyq_rate = samplerate/2
#         width = 5.0/nyq_rate
#         ripple_db = 60.0 #dB
#         N , beta = window.kaiserord(ripple_db, width)
#         taps = window.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
#         yFiltrado = window.lfilter(taps, 1.0, y)
#         return yFiltrado
# =============================================================================

    def LPF(self, sinal, cutoff_hz, fs):
        #####################
        # Filtro passa-baixas (Low-pass filter)
        #####################
        # https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html
        nyq_rate = fs/2
        width = 5.0/nyq_rate
        ripple_db = 60.0 #dB
        N , beta = window.kaiserord(ripple_db, width)
        taps = window.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
        return( window.lfilter(taps, 1.0, sinal))
        
# =============================================================================
#     # Função que pode ser útil
#     def signal_handler(self, sinal, frame):
#             print('You pressed Ctrl+C!')
#             sys.exit(0)
# =============================================================================

    # Converte intensidade em Db
    def todB(self, s):
        sdB = 10*np.log10(s)
        return(sdB)
