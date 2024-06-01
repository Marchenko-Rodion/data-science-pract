import numpy
import math
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider,Button,CheckButtons
import scipy.signal

BOLD = '\033[1m'
END = '\033[0m'

xAxis = None
yAxis = None
NoiseYAxis = None
ShowNoiseBit = True
ShowFilterBit = False

#Marchenko rodion Data Analysis prakt №5.1


#Дана функція або робить невидимою рамку навколо обʼєкта, або лише частину для імітації тіней
def DisableOutline(ax, Shadow):
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    if Shadow == False:
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)


#Дана функція виводить декоративний прямокутник на екран за координатами 0.245, 0.117 від розміру вікна
def RenderBoundBox():
    ax = plt.axes([0.245, 0.117, 0.65, 0.07])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.set_facecolor("#D3D3D3")


#Дана функція друкує на екран гармонічну функцію з заданими параметрами, додаванням шуму та застосуванням фільтра:
def harmonic_with_noise(ax, Amplitude, Frequency, Phase, NoiseMean, NoiseCovariance, ShowNoise, ShowFilter, RedrawSine, RedrawNoise):
    global xAxis
    global yAxis
    global NoiseYAxis
    
    if Amplitude < 0:
        Amplitude = 0
    if Frequency <= 0:
        Frequency = 0.1
    
    if (RedrawSine == True) or (xAxis is None):
        xAxis = numpy.linspace(0, 2*numpy.pi, 1500)
        yAxis = Amplitude * numpy.sin((xAxis * Frequency) + Phase)
    
    ax.cla()#Clearing the plot before redrawing
    ax.plot(xAxis/numpy.pi, yAxis, color="#6A0202")
    ax.grid(linestyle=':', linewidth=1)
    ax.set_ylabel("Aмплітуда", fontsize="12", fontweight="bold", rotation="vertical")
    ax.set_xlabel("2π", fontsize="12", fontweight="bold", rotation="horizontal")
    
    if ShowNoise == True:
        if (RedrawNoise == True):
            NoiseYAxis = numpy.random.normal(NoiseMean, NoiseCovariance, len(xAxis/numpy.pi))
        ax.plot(xAxis/numpy.pi, NoiseYAxis+yAxis, color="darkred", alpha=0.8)
    else:
        ax.plot(xAxis/numpy.pi, yAxis, color="darkred", alpha=0.8)
        
    if ShowFilter == True:
        FilterNoise(ax, NoiseYAxis+yAxis, xAxis, FilterSL.val, FreqSL.val)


#Дана функція фільтрує зашумлений вхідний сигнал низькочастотним фільтром scipy.signal Butterworth:
def FilterNoise(ax, yRaw, xRaw, FilterOrder, Frequency):
    if ShowFilterBit == True:
        b, a = scipy.signal.iirfilter(math.ceil(FilterOrder), Wn=Frequency*2.5, fs=1500, btype="low", ftype="butter")
        y_lfilter = scipy.signal.lfilter(b, a, yRaw)
        ax.plot(xRaw/numpy.pi, y_lfilter, color="#4E92B8")
    



# Функції для оновления графіка на основі значення слайдера (Callback)
def updateHarmonic(val):
    harmonic_with_noise(ax, AmpSL.val, FreqSL.val, 0, NoiseMeanSL.val, NoiseCovarianceSL.val, ShowNoiseBit, ShowFilterBit, True, False) #Replotting

    
def updateNoise(val):
    harmonic_with_noise(ax, AmpSL.val, FreqSL.val, 0, NoiseMeanSL.val, NoiseCovarianceSL.val, ShowNoiseBit, ShowFilterBit, False, True) #Replotting


def resetPlot(val):
    if NoiseButton.get_status()[0] == False:
        NoiseButton.set_active(0)
    if FilterButton.get_status()[0] == True:
        FilterButton.set_active(0)
    
    FreqSL.set_val(15)
    AmpSL.set_val(5)
    NoiseMeanSL.set_val(0.6)
    NoiseCovarianceSL.set_val(1.8)
    FilterSL.set_val(4)
    
    
def toggleNoise(label):
    global ShowNoiseBit
    if label == "Шум":
        ShowNoiseBit = not ShowNoiseBit
        harmonic_with_noise(ax, AmpSL.val, FreqSL.val, 0, NoiseMeanSL.val, NoiseCovarianceSL.val, ShowNoiseBit, ShowFilterBit, False, False) #Replotting
        plt.draw()


def toggleFilter(label):
    global ShowFilterBit
    global NoiseYAxis
    global yAxis
    if label == "Фільтр":
        ShowFilterBit = not ShowFilterBit
        harmonic_with_noise(ax, AmpSL.val, FreqSL.val, 0, NoiseMeanSL.val, NoiseCovarianceSL.val, ShowNoiseBit, ShowFilterBit, False, False) #Replotting
        plt.draw()


def updateFilterOrder(val):
    harmonic_with_noise(ax, AmpSL.val, FreqSL.val, 0, NoiseMeanSL.val, NoiseCovarianceSL.val, ShowNoiseBit, ShowFilterBit, False, False) #Replotting




fig, ax = plt.subplots(figsize=(6.7, 5.5)) #Створюємо обʼєкт графіка
plt.subplots_adjust(bottom=0.49)

harmonic_with_noise(ax, 5, 15, 0, 0.6, 1.4, True, False, True, True) #Стартовий графік


# Додавання елементів керування (слайдерів, кнопок та чекбоксів)
axFreqSL = plt.axes([0.245, 0.35, 0.65, 0.03])
FreqSL = Slider(ax=axFreqSL, label="Частота, Гц", valmin=0.0, valmax=100.0, valinit=15, initcolor="none", color="darkred")
axAmpSL = plt.axes([0.935, 0.49, 0.028, 0.39])
AmpSL = Slider(ax=axAmpSL, label="Aмпл.", valmin=0.0, valmax=60.0, valinit=5, initcolor="none", color="darkred", orientation="vertical")

axNoiseMeanSL = plt.axes([0.245, 0.29, 0.65, 0.03])
NoiseMeanSL = Slider(ax=axNoiseMeanSL, label="Aмплітуда шуму", valmin=0.0, valmax=15.0, valinit= 0.6, initcolor="none", color="#B45C5C")
axNoiseCovarianceSL = plt.axes([0.245, 0.23, 0.65, 0.03])
NoiseCovarianceSL = Slider(ax=axNoiseCovarianceSL, label="Дисперсія шуму", valmin=0.0, valmax=23.0, valinit=1.8, initcolor="none", color="#B45C5C")

RenderBoundBox()
axNoiseButton = plt.axes([0.265, 0.138, 0.15, 0.03])
NoiseButton = CheckButtons(ax=axNoiseButton, labels=["Шум"], actives=["true"], label_props={"fontsize":[13], "fontweight":["semibold"], "fontstyle":["italic"]}, check_props={"linewidths":[2], "facecolors":["darkred"]}, frame_props={"edgecolor":["none"]})
DisableOutline(axNoiseButton, False)
axNoiseButton.set_facecolor("#D3D3D3")
axResetButton = plt.axes([0.7, 0.127, 0.173, 0.05])
ResetButton = Button(axResetButton, "Скинути", color="darkred", hovercolor="#B45C5C")
ResetButton.label.set_fontsize(14)
ResetButton.label.set_fontweight("semibold")
ResetButton.label.set_fontstyle("italic")
DisableOutline(axResetButton, True)

axFilterSL = plt.axes([0.245, 0.05, 0.65, 0.03])
FilterSL = Slider(ax=axFilterSL, label="Порядок фільтра", valmin=0.0, valmax=10.0, valinit=4, valstep=1, initcolor="none", color="#4E92B8", orientation="horizontal")
axFilterButton = plt.axes([0.4, 0.138, 0.15, 0.03])
FilterButton = CheckButtons(ax=axFilterButton, labels=["Фільтр"], actives=["true"], label_props={"fontsize":[13], "fontweight":["semibold"], "fontstyle":["italic"]}, check_props={"linewidths":[2], "facecolors":["#4E92B8"]}, frame_props={"edgecolor":["none"]})
DisableOutline(axFilterButton, False)
FilterButton.set_active(0)
axFilterButton.set_facecolor("#D3D3D3")


# Прив'язка функцій оновления до відповідних елементів керування
FreqSL.on_changed(updateHarmonic)
AmpSL.on_changed(updateHarmonic)
NoiseMeanSL.on_changed(updateNoise)
NoiseCovarianceSL.on_changed(updateNoise)
ResetButton.on_clicked(resetPlot)
NoiseButton.on_clicked(toggleNoise)
FilterButton.on_clicked(toggleFilter)
FilterSL.on_changed(updateFilterOrder)


#Встановлення назви вікна
plt.get_current_fig_manager().set_window_title("Exploring harmonic functions (using Python matplotlib)") #Set the window name
#Запуск
plt.show()


