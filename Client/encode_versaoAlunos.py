
#importe as bibliotecas
from suaBibSignal import signalMeu
import numpy as np
import sounddevice as sd
import soundfile as sf


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
    meu_sinal = signalMeu()
    
    # Pegando áudio que será transmitido
    data, samplerate = sf.read("RickRoll.wav")
    # Quantidade de pontos
    n = len(data)
    # Amplitude do sinal
    amplitude = 1
    # Tempo de duração do sinal em segundos
    time = len(data)/samplerate
    # Você importou a bilioteca sounddevice como sd. 
    # Então os seguintes parâmetros devem ser setados:
    sd.default.samplerate = samplerate # Taxa de amostragem
    sd.default.channels = 2  # Você pode ter que alterar isso dependendo da sua placa
    #sd.default.device = 'digital output'
    
    # Dados do eixo x (tempo) para plotagem de gráficos
    t = np.linspace(0, time, n)
    
    # Gráfico 1: sinal do áudio original - domínio do tempo
    meu_sinal.plotSinal(data, t, "Gráfico 1")
    
    data_filtrada = meu_sinal.LPF(data, 2500, samplerate)
    
    # Trava o programa para tocar na hora certa
    _ = input("Pressione Enter para tocar o áudio filtrado: ")
    
    sd.play(data_filtrada, samplerate)
    sd.wait()
    
    # Gráfico 2: Sinal de áudio filtrado - domínio do tempo
    meu_sinal.plotSinal(data_filtrada, t, "Gráfico 2")
    
    # Gráfico 3: Sinal do áudio filtrado - domínio da frequência
    meu_sinal.plotFFT(data_filtrada, samplerate, "Gráfico 3")
    
    portadora = meu_sinal.generateSin(13000, amplitude, t, samplerate)
    
    modulado = np.array(data_filtrada) * np.array(portadora)
    
    # Gráfico 4: sinal de áudio modulado - domínio do tempo
    meu_sinal.plotSinal(modulado, t, "Gráfico 4")
    
    # Gráfico 5: sinal de áudio modulado - domínio da frequência
    meu_sinal.plotFFT(modulado, samplerate, "Gráfico 5")
    
    maximo = 0
    for p in modulado:
        p_modulo = abs(p)
        if p_modulo > maximo:
            maximo = p_modulo
            
    normalizado = modulado/maximo
    
    # Trava o programa para tocar na hora certa
    _ = input("Pressione Enter para tocar o áudio modulado: ")
    
    sd.play(normalizado, samplerate)
    sd.wait()

if __name__ == "__main__":
    main()
