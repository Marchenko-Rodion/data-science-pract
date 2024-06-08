import numpy
import math
import matplotlib
import matplotlib.pyplot as plt
import time

BOLD = '\033[1m'
END = '\033[0m'

#Marchenko rodion Data Analysis prakt №6.1

#Дана функція або робить невидимою рамку навколо обʼєкта, або лише частину 
def DisableOutline(ax, partial):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if partial == False:
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        plt.axis('off')


#Дана функція наносить масив випадкових по осі Y точок та їх осьову пряму на графік
def PlotRandPoints(ax, rawX, rawY, randY):
    #ax.scatter(rawX, rawY, color="#DC5200", alpha=0.1)
    ax.plot(rawX, rawY, color="#F1AD30", linewidth=2.5, alpha=0.8, linestyle='--', label="Початкова пряма")
    ax.scatter(rawX, randY, color="orange", alpha=0.3)
    ax.grid(linestyle=':', linewidth=1)
    ax.set_ylabel("Y", fontsize="12", fontweight="bold", rotation="vertical")
    ax.set_xlabel("X", fontsize="12", fontweight="bold", rotation="horizontal")
    ax.set_title("Лін. регресія даних методом найменших квадратів:", fontsize="15", fontstyle="italic", rotation="horizontal")
    DisableOutline(ax, True)


#Дана функція реалізує лінійну регресію методом найменших квадратів на основі двох формул на вибір
def SmallestSquareMethodRegression(rawX, randY, RegressionType):
    if RegressionType == 2: #Алгоритм 1 (тягне пряму через найбільші скупчення випадкових точок, не дуже точний на випадковій множині)
        SumX = numpy.sum(rawX)
        Sum2X = numpy.sum(rawX**2)
        SumY = numpy.sum(randY)
        SumXY = numpy.sum(rawX*randY)
        n = SumX.size
        
        K = (n*SumXY - SumX*SumY) / (n*Sum2X - SumX**2)
        B = (n*SumY - K*SumX) / n
        return [K, B]
    
    elif RegressionType == 1: #Алгоритм 2 (ближче до початкової прямої)
        Xavg = numpy.mean(rawX)
        Yavg = numpy.mean(randY)
        
        K1 = numpy.sum((rawX - Xavg) * (randY - Yavg))
        K2 = numpy.sum((rawX - Xavg)**2)
        K = K1 / K2
        
        B = Yavg - K*Xavg
        return [K, B]

    

## ЗМІННІ ПАРАМЕТРІВ ГРАФІКА ##
NumberOfPoints = 12 # К-ть точок на графіку *10.
RandomDistRange = 0.3 # Максимальне відхилення випадкових значень від осьової прямої kx+b.
k = 2 # Коефіцієнт k прямої.
b = 3 # Коефіцієнт b прямої.



fig, ax = plt.subplots(figsize=(10.4, 7.5)) #Створюємо обʼєкт графіка
plt.subplots_adjust(left=0.1, bottom = 0.2)


xArray = numpy.arange(0,NumberOfPoints,0.1) #Вісь Х

yArray = (xArray*k)+b
yRandArray = numpy.random.randint(low=-100*numpy.max(yArray)*RandomDistRange, high=100*numpy.max(yArray)*RandomDistRange, size=NumberOfPoints*10)/100
yRandArray = yArray+(yRandArray/1.5)
PlotRandPoints(ax, xArray, yArray, yRandArray) #Виводимо графік випадкових точок та їх осьового графіка kx+b


NpRegKoef = numpy.polyfit(xArray,yRandArray,1) #ЗНАХОДИМО КОЕФІЦІЄНТИ ЛІНІЙНОЇ РЕГРЕСІЇ МЕТОДАМИ NUMPY
print("\nNumPy regression algorithm: [K,B] =",NpRegKoef)

yPolifitArray = xArray*NpRegKoef[0] + NpRegKoef[1]
#Виводимо регресійну пряму Numpy
ax.plot(xArray, yPolifitArray, color="#9A1300", linewidth=2.5, alpha=0.9, linestyle=':', label="Регресія NumPy") 


yMyApproxKoef1 = SmallestSquareMethodRegression(xArray,yRandArray, 1) #ЗНАХОДИМО КОЕФІЦІЄНТИ ЛІНІЙНОЇ РЕГРЕСІЇ 1
print("my regression algorithm 1: [K,B] =", yMyApproxKoef1)

yMyApproxArray1 = xArray*yMyApproxKoef1[0] + yMyApproxKoef1[1]
#Виводимо
ax.plot(xArray, yMyApproxArray1, color="#488CEF", linewidth=2.5, alpha=0.4, label="Моя регресія 1") 


yMyApproxKoef2 = SmallestSquareMethodRegression(xArray,yRandArray, 2) #ЗНАХОДИМО КОЕФІЦІЄНТИ ЛІНІЙНОЇ РЕГРЕСІЇ 2
print("my regression algorithm 2: [K,B] =", yMyApproxKoef2)

yMyApproxArray2 = xArray*yMyApproxKoef2[0] + yMyApproxKoef2[1]
#Виводимо
ax.plot(xArray, yMyApproxArray2, color="#729F3A", linewidth=2.5, alpha=0.5, label="Моя регресія 2") 


ax.legend(loc="lower right") 

#Шукаємо і знаходимо абсолютні й відносні відхилення:
KnpErr = round(k - NpRegKoef[0], 3)
BnpErr = round(b - NpRegKoef[1], 3)
KnpRelErr = round(KnpErr/NpRegKoef[0], 3)
BnpRelErr = round(BnpErr/NpRegKoef[1], 3)

MyK1Err = round(k - yMyApproxKoef1[0], 3)
MyB1Err = round(b - yMyApproxKoef1[1], 3)
MyK1RelErr = round(MyK1Err/yMyApproxKoef1[0], 3)
MyB1RelErr = round(MyB1Err/yMyApproxKoef1[1], 3)

MyK2Err = round(k - yMyApproxKoef2[0], 3)
MyB2Err = round(b - yMyApproxKoef2[1], 3)
MyK2RelErr = round(MyK2Err/yMyApproxKoef2[0], 3)
MyB2RelErr = round(MyB2Err/yMyApproxKoef2[1], 3)

#Виводимо інформацію про відхилення:
axTxt = plt.axes([0.1, 0.035, 0.75, 0.045])
axTxt.text(-0.049, 0.14, "»» K = "+str(k)+",  B = "+str(b), fontsize = 15, fontweight="bold", fontstyle="italic")
axTxt.text(-0.049, 0.07, "»» Лінійна регресія NumPy:   ΔК = "+str(KnpErr)+" ("+str(KnpRelErr)+"%),  ΔВ = "+str(BnpErr)+" ("+str(BnpRelErr)+"%)", fontsize = 15)
axTxt.text(-0.049, 0, "»» Лінійна регресія №1:         ΔК = "+str(MyK1Err)+" ("+str(MyK1RelErr)+"%),  ΔВ = "+str(MyB1Err)+" ("+str(MyB1RelErr)+"%)", fontsize = 15)
axTxt.text(-0.049, -0.07, "»» Лінійна регресія №2:         ΔК = "+str(MyK2Err)+" ("+str(MyK2RelErr)+"%),  ΔВ = "+str(MyB2Err)+" ("+str(MyB2RelErr)+"%)", fontsize = 15)
DisableOutline(axTxt, False)


#Запуск
plt.autoscale(tight=True)
plt.get_current_fig_manager().set_window_title("Linear-regression Data Science pract №6") #Set the window name
plt.show() 
