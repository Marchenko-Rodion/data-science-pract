from bokeh.layouts import layout, column, row
from bokeh.models.widgets import Slider, CheckboxButtonGroup, Button, Select
from bokeh.models import HoverTool
from bokeh.plotting import figure, curdoc
import numpy
import math
import scipy.signal

xAxis = None
yAxis = None
NoiseYAxis = None
ShowNoiseBit = True
ShowFilterBit = False

#Marchenko rodion Data Analysis prakt №5.2

#УВАГА!!! Дана програма розрахована на запуск з допомогою локального сервера Вokeh!
#Для старту, зі встановленою на ПК бібліотекою Вokeh введіть у терміналі 'bokeh serve --show DS-lab5.2.py'


#Створюємо обʼєкт графіка
plot = figure(title="Exploring harmonic functions", x_axis_label="2π", y_axis_label="Aмплітуда", width=750, sizing_mode="scale_height")

#Налаштовуємо зовнішній вигляд графіка
plot.title.text_font = "times"
plot.title.text_font_style = "italic"
plot.title.text_font_size = "25pt"
plot.background_fill_color = "#272E33"
plot.axis.axis_label_text_font_style = "bold"
plot.axis.axis_label_text_font_size = "15pt"
plot.min_border_left = 80
plot.min_border_right = 40
plot.min_border_top = 80
plot.min_border_bottom = 80

#Додаємо вспилваючу підказку з координатами на графік
hover = HoverTool()
hover.tooltips = [('X', '@x'), ('Y', '@y')]  #Визначення формату підказки




#Дана функція очищає графік:
def clear_plot(plot):
    plot.renderers = []


#Дана функція друкує на екран гармонічну функцію з заданими параметрами, додаванням шуму та застосуванням фільтра:
def harmonic_with_noise(plot, Amplitude, Frequency, Phase, NoiseMean, NoiseCovariance, ShowNoise, ShowFilter, RedrawSine, RedrawNoise):
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
    
    clear_plot(plot)
    line1 = plot.line(xAxis/numpy.pi, yAxis, line_width=2, line_color="darkred", legend_label="Чиста гармоніка")
    hover.renderers = [line1]
    
    if ShowNoise == True:
        if (RedrawNoise == True):
            NoiseYAxis = numpy.random.normal(NoiseMean, NoiseCovariance, len(xAxis/numpy.pi))
        line2 = plot.line(xAxis/numpy.pi, NoiseYAxis+yAxis, line_width=2, line_color="darkred", line_alpha=0.5, legend_label="Зашумлена гармоніка")
        hover.renderers.append(line2)
        
    if ShowFilter == True:
        FilterNoise(plot, NoiseYAxis+yAxis, xAxis, FilterSL.value, Frequency, SelectFilter.value)
        

#Дана функція фільтрує зашумлений вхідний сигнал низькочастотним фільтром scipy.signal на вибір:
def FilterNoise(plot, yRaw, xRaw, FilterOrder, Frequency, FilterType):
    if ShowFilterBit == True:
        if (FilterType == "butter") or (FilterType == "bessel"):
            b, a = scipy.signal.iirfilter(math.ceil(FilterOrder), Wn=Frequency*2.5, fs=1500, btype="low", ftype=FilterType)
        elif (FilterType == "cheby1") or (FilterType == "cheby2"):
            b, a = scipy.signal.iirfilter(math.ceil(FilterOrder), Wn=Frequency*2.5, rp=RpSL.value, rs=RsSL.value, fs=1500, btype="low", ftype=FilterType)
        elif FilterType == "ellip":
            b, a = scipy.signal.iirfilter(math.ceil(FilterOrder), Wn=Frequency*2.5, rp=RpSL.value, rs=RsSL.value, fs=1500, btype="low", ftype=FilterType)
        y_lfilter = scipy.signal.lfilter(b, a, yRaw)
        line3 = plot.line(xAxis/numpy.pi, y_lfilter, line_width=2, line_color="#4E92B8", legend_label="Відфільтрована гармоніка")
        hover.renderers.append(line3)




# Додавання елементів керування (слайдерів, кнопок, перемикачів та списків)
AmpSL = Slider(start=0, end=60, value=5, step=0.1, title="Aмплітуда", bar_color = "#15191C")
FreqSL = Slider(start=0, end=100, value=9, step=0.1, title="Частота, Гц", bar_color = "#15191C")
NoiseMeanSL = Slider(start=0, end=15, value=0.6, step=0.1, title="Aмплітуда шуму", bar_color = "#15191C")
NoiseCovarianceSL = Slider(start=0, end=23, value=1.8, step=0.1, title="Дисперсія шуму", bar_color = "#15191C")
FilterSL = Slider(start=0, end=10, value=4, step=1, title="Порядок фільтра", bar_color = "#4E92B8")
RsSL = Slider(start=0, end=10, value=3, step=1, title="Мінімальне затухання (rs)", bar_color = "#4E92B8")
RpSL = Slider(start=0, end=10, value=1, step=1, title="Нерівномірність затухання (rp)", bar_color = "#4E92B8")

SelectFilter = Select(title="Вид фільтра:", value="butter", options=["butter", "cheby1", "cheby2", "ellip", "bessel"], width=300)
CKBX = CheckboxButtonGroup(labels=["Шум","Фільтр"], active=[0], width=300)
RST = Button(label="RESET", button_type="danger", width=300)




# Функції для оновления графіка на основі значення слайдера (Callback)
def updateHarmonic(attr, old, new):
    harmonic_with_noise(plot, AmpSL.value, FreqSL.value, 0, NoiseMeanSL.value, NoiseCovarianceSL.value, ShowNoiseBit, ShowFilterBit, True, False) #Replotting


def updateNoise(attr, old, new):
    harmonic_with_noise(plot, AmpSL.value, FreqSL.value, 0, NoiseMeanSL.value, NoiseCovarianceSL.value, ShowNoiseBit, ShowFilterBit, False, True) #Replotting


def updateFilterOrder(attr, old, new):
    harmonic_with_noise(plot, AmpSL.value, FreqSL.value, 0, NoiseMeanSL.value, NoiseCovarianceSL.value, ShowNoiseBit, ShowFilterBit, False, False) #Replotting


def resetPlot(attr):
    CKBX.active = [0]
    
    FreqSL.update(value=9)
    AmpSL.update(value=5)
    NoiseMeanSL.update(value=0.6)
    NoiseCovarianceSL.update(value=1.8)
    FilterSL.update(value=4)
    SelectFilter.update(value="butter")
    RsSL.update(value=3)
    RpSL.update(value=1)


def toggle(atrr, old, new):
    global ShowNoiseBit
    global ShowFilterBit
    if 0 in CKBX.active:
        ShowNoiseBit = True
    else:
        ShowNoiseBit = False
        
    if 1 in CKBX.active:
        ShowFilterBit = True
    else:
        ShowFilterBit = False
    harmonic_with_noise(plot, AmpSL.value, FreqSL.value, 0, NoiseMeanSL.value, NoiseCovarianceSL.value, ShowNoiseBit, ShowFilterBit, False, False) #Replotting




# Прив'язка функцій оновления до відповідних елементів керування
AmpSL.on_change('value', updateHarmonic)
FreqSL.on_change('value', updateHarmonic)
NoiseMeanSL.on_change('value', updateNoise)
NoiseCovarianceSL.on_change('value', updateNoise)
FilterSL.on_change('value', updateFilterOrder)
RST.on_click(resetPlot)
CKBX.on_change("active", toggle)
SelectFilter.on_change("value", toggle)
RsSL.on_change('value', updateFilterOrder)
RpSL.on_change('value', updateFilterOrder)

# Створення початкового графіка
harmonic_with_noise(plot, 5, 9, 0, 0.6, 1.4, True, True, True, True) #First plot


# Створення комплексного дашборда (верстка сторінки, що буде відображатись у браузері)
plot.add_tools(hover)
dashboard = row(plot,column(row(), AmpSL, FreqSL, NoiseMeanSL, NoiseCovarianceSL, FilterSL, RsSL, RpSL,  SelectFilter, CKBX, RST, width=450), sizing_mode="stretch_both")

curdoc().theme = "dark_minimal" #Застосування декоративної теми
curdoc().title = "Exploring harmonic functions (using Python Bokeh library)" #Встановлення назви вкладки у браузері
curdoc().add_root(dashboard) #Запуск


