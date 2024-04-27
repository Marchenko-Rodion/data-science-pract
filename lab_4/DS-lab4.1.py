import pandas
import numpy
import os
import math
import urllib.request
import zipfile
import timeit
import copy
from datetime import datetime

BOLD = '\033[1m'
END = '\033[0m'
BROWN = "\033[0;33m"
BROWN2 = "\x1b[38;5;3m"

#Marchenko rodion Data Analysis prakt №4

print(BOLD+"MARCHENKO RODION FB-23 PRAKT №4.1 \"Using Pandas and Numpy for numerical data Analysis\"")
print("="*86+END)


#This function loads the initial dataset files from the Internet as a zip archive and decompresses it to the computer, if not already present
def InitializeLoad():
	#Creating temporary directory if it does not exist
	CurrentDirectory = os.getcwd()
	if (os.getcwd()[-13:] != "/DataLab4-tmp"):
		try:
			os.chdir(CurrentDirectory+"/DataLab4-tmp")
		except:
			try:
				os.makedirs(CurrentDirectory+"/DataLab4-tmp")
				print("»» Created tmp directory /DataLab4-tmp.")
			except FileExistsError:
				# directory already exists
				pass
			os.chdir(CurrentDirectory+"/DataLab4-tmp") #GO TO DATASET DIRECTORY!!!

	print("»» The current working directory is: "+os.getcwd()+".\n")


	#Loading data, unzipping and renaming the CSV
	CWD = os.getcwd()
	AvailableFiles = os.listdir(CWD)
	CurrentTime = datetime.now().strftime("%d-%m-%y-%H-%M-%S")

	Filename = CWD+"/Household-electric-power-consumption--"+CurrentTime+".zip"
	UnzippedFileName = "household_power_consumption"
	URL = "https://archive.ics.uci.edu/static/public/235/individual+household+electric+power+consumption.zip"

	if any(UnzippedFileName+".csv" in path for path in AvailableFiles):
		pass
	else:
		try:
			urllib.request.urlretrieve(URL,Filename)
			with zipfile.ZipFile(Filename, 'r') as zip_ref:
				zip_ref.extractall(CWD)
			os.rename(CWD+"/"+UnzippedFileName+".txt", CWD+"/"+UnzippedFileName+".csv")

			print("\t» Downloaded Household electric power consumption dataset from the internet.")
		except:
			print("\t» ERROR: Failed to load the dataset.")
	return CWD


#This function reads datasets as pandas frame and numpy array
def ReadDatasetFromCSV(WorkDir):
	headers = ['Date', 'Time', 'GlobalActivePower', 'GlobalReactivePower', 'Voltage', 'GlobalIntensity', 'SubMetering1', 'SubMetering2', 'SubMetering3'] #CSV table headers
	print("»» "+BOLD+"Loading data from file:"+END)
	for path in os.listdir(WorkDir):
		FullPath = os.path.join(WorkDir, path)
		if (os.path.isfile(FullPath) and path[-4:] == ".csv"): #Find the first existing CSV file
			print(path)
			df = pandas.read_csv(FullPath, header = 1, names = headers, delimiter = ";")
			nparray = df.to_numpy()
			break

	return [df,nparray]






CWD = InitializeLoad()
FullDataSet = ReadDatasetFromCSV(CWD)

PdDataSet = FullDataSet[0] #PANDAS DATAFRAME VERSION OF THE DATASET
NpDataSet = FullDataSet[1] #NUMPY ARRAY VERSION OF THE DATASET

TstPdDataSet = copy.copy(PdDataSet) #PANDAS DATAFRAME VERSION OF THE DATASET FOR TIME PROFILING
TstNpDataSet = copy.copy(NpDataSet) #NUMPY ARRAY VERSION OF THE DATASET FOR TIME PROFILING

#This function performs some preprocessing on Pandas Dataframe
def PandasPrepareData(Dataset):
	Dataset = Dataset.dropna(axis=0) #Drop empty rows
	Dataset.insert(2, "DateTime", Dataset["Date"]+" "+Dataset["Time"]) #Insert a numpy-compatible date-time column
	Dataset["DateTime"] = pandas.to_datetime(Dataset["DateTime"], format="%d/%m/%Y %H:%M:%S") #Cast column to datetime64
	Dataset = Dataset.reset_index(drop=True) #Reset global index without preserving the old one
	Dataset = Dataset.astype({"GlobalActivePower":"float32", "GlobalReactivePower":"float32", "Voltage":"float32", "GlobalIntensity":"float32", "SubMetering1":"float32", "SubMetering2":"float32", "SubMetering3":"float32"}) #Convert columns to floats for further use in conditions
	return Dataset

#This function performs some preprocessing on Numpy Array
def NumpyPrepareData(Array):
	Array = numpy.where(Array == '?',numpy.nan, Array) #replace dataset`s empty markers with numpy.nan
	NumSubArray = Array[:,2:].astype("float32") #Number only subarray, because you can`t compare string to NaN
	Array = Array[~numpy.isnan(NumSubArray).any(axis=1)] #Drop empty rows

	#CONVERSION TO STRUCTURED ARRAY:
	dtype = numpy.dtype([("Date","object"),("Time","object"),("GlobalActivePower","float32"),("GlobalReactivePower","float32"),("Voltage","float32"),("GlobalIntensity","float32"),("SubMetering1","float32"),("SubMetering2","float32"),("SubMetering3","float32")]) #Define the NumPy data type of each column
	tuples = numpy.rec.fromarrays(Array.transpose(), dtype=dtype) #Turn the original np.array into a set of tuples, representing each row of the array
	SArray = numpy.array(tuples, dtype=dtype) #Convert to NumPy structured array

	return SArray



PdDataSet = PandasPrepareData(PdDataSet)
t1 =  timeit.timeit(stmt="PandasPrepareData(TstPdDataSet)", number=3, globals=globals())
print("\n"+"="*84)
print(PdDataSet)
print(BROWN+BOLD+"Сер. Час підготовки даних з допомогою Pandas: "+END+str(t1)+END,"\n")

NpDataSet = NumpyPrepareData(NpDataSet)
t2 =  timeit.timeit(stmt="NumpyPrepareData(TstNpDataSet)", number=3, globals=globals())
print("\n"+"="*84)
print(NpDataSet)
print(NpDataSet.shape)
print(BROWN+BOLD+"Сер. Час підготовки даних з допомогою NumPy: "+END+str(t2)+END,"\n")

print("\n"+"="*84)



#SELECTIONS:

#1.
print(BOLD+"\nВсі домогосподарства, у яких загальна активна споживана потужність перевищує 5 кВт:"+END)

PdActivePower = PdDataSet[PdDataSet["GlobalActivePower"] > 5]
#Pandas
t1 =  timeit.timeit(stmt="PdDataSet[PdDataSet['GlobalActivePower'] > 5]", number=9, globals=globals())
#Profiling

print(BROWN+"Pandas:\n"+END,PdActivePower)
print(BROWN+BOLD+"Сер. Час виконання: "+END+str(t1)+END,"\n")


NpActivePower = NpDataSet[numpy.where(NpDataSet["GlobalActivePower"] > 5)]
#NumPy
t2 =  timeit.timeit(stmt="NpDataSet[numpy.where(NpDataSet['GlobalActivePower'] > 5)]", number=9, globals=globals())
#Profiling

print(BROWN+"NumPy:\n"+END,NpActivePower,"\n")
print(NpActivePower.shape,"rows.")
print(BROWN+BOLD+"Сер. Час виконання: "+END+str(t2)+END)



#2.
print(BOLD+"\n\nВсі домогосподарства, у яких вольтаж перевищує 235 В:"+END)

PdVoltage = PdDataSet[PdDataSet["Voltage"] > 235]
#Pandas
t1 =  timeit.timeit(stmt="PdDataSet[PdDataSet['Voltage'] > 235]", number=9, globals=globals())
#Profiling

print(BROWN+"Pandas:\n"+END,PdVoltage)
print(BROWN+BOLD+"Сер. Час виконання: "+END+str(t1)+END,"\n")


NpVoltage = NpDataSet[numpy.where(NpDataSet["Voltage"] > 235)]
#NumPy
t2 =  timeit.timeit(stmt="NpDataSet[numpy.where(NpDataSet['Voltage'] > 235)]", number=9, globals=globals())
#Profiling

print(BROWN+"NumPy:\n"+END,NpVoltage,"\n")
print(NpVoltage.shape,"rows.")
print(BROWN+BOLD+"Сер. Час виконання: "+END+str(t2)+END)



#3.
print(BOLD+"\n\nВсі домогосподарства, у яких сила струму лежить в межах 19-20 та у яких пральна машина та холодильних споживають більше, ніж бойлер та кондиціонер:"+END)

PdCurrentAndPower = PdDataSet[(PdDataSet["GlobalIntensity"] <= 20) & (PdDataSet["GlobalIntensity"] >= 19) & (PdDataSet["SubMetering2"] > PdDataSet["SubMetering3"])]
#Pandas
t1 =  timeit.timeit(stmt="PdDataSet[(PdDataSet['GlobalIntensity'] <= 20) & (PdDataSet['GlobalIntensity'] >= 19) & (PdDataSet['SubMetering2'] > PdDataSet['SubMetering3'])]", number=9, globals=globals())
#Profiling

print(BROWN+"Pandas:\n"+END,PdCurrentAndPower)
print(BROWN+BOLD+"Сер. Час виконання: "+END+str(t1)+END,"\n")


NpCurrentAndPower = NpDataSet[numpy.where((NpDataSet["GlobalIntensity"] <= 20) & (NpDataSet["GlobalIntensity"] >= 19) & (NpDataSet["SubMetering2"] > NpDataSet["SubMetering3"]))]
#NumPy
t2 =  timeit.timeit(stmt="NpDataSet[numpy.where((NpDataSet['GlobalIntensity'] <= 20) & (NpDataSet['GlobalIntensity'] >= 19) & (NpDataSet['SubMetering2'] > NpDataSet['SubMetering3']))]", number=9, globals=globals())

print(BROWN+"NumPy:\n"+END,NpCurrentAndPower,"\n")
print(NpCurrentAndPower.shape,"rows.")
print(BROWN+BOLD+"Сер. Час виконання: "+END+str(t2)+END)



#4.
print(BOLD+"\n\nСередні величини усіх 3-х груп споживання електричної енергії для 500000 випадкових домогосподарств (без повторів елементів вибірки):"+END)

NumberOfRows = PdDataSet.shape[0]
RandomRows = numpy.random.choice(NumberOfRows, replace=True, size=500000) #Select random indexes

def PdMeans(RandomRows, DataSet):
	PdRandoms = DataSet.iloc[RandomRows]
	SubMetering1Mean = PdRandoms["SubMetering1"].mean()
	SubMetering2Mean = PdRandoms["SubMetering2"].mean()
	SubMetering3Mean = PdRandoms["SubMetering3"].mean()
	return [SubMetering1Mean, SubMetering2Mean, SubMetering3Mean]

means = PdMeans(RandomRows, PdDataSet)
#Pandas
t1 = timeit.timeit(stmt="PdMeans(RandomRows, PdDataSet)", number=9, globals=globals())
#Profiling

print(BROWN+"\nPandas:"+END)
print("Середні значення для трьох груп споживання: "+BOLD+str(means[0])+", "+str(means[1])+", "+str(means[2])+END)
print(BROWN+BOLD+"Сер. Час виконання: "+END+str(t1)+END,"\n")


def NpMeans(RandomRows, DataSet):
	NpRandoms = DataSet[RandomRows]
	SubMetering1Mean = NpRandoms["SubMetering1"].mean()
	SubMetering2Mean = NpRandoms["SubMetering2"].mean()
	SubMetering3Mean = NpRandoms["SubMetering3"].mean()
	return [SubMetering1Mean, SubMetering2Mean, SubMetering3Mean]

means = NpMeans(RandomRows, NpDataSet)
#NumPy
t2 = timeit.timeit(stmt="NpMeans(RandomRows, NpDataSet)", number=9, globals=globals())
#Profiling

print(BROWN+"NumPy:"+END)
print("Середні значення для трьох груп споживання: "+BOLD+str(means[0])+", "+str(means[1])+", "+str(means[2])+END)
print(BROWN+BOLD+"Сер. Час виконання: "+END+str(t2)+END,"\n")



#5.
print(BOLD+"\n\nДомогосподарства, які після 18-00 споживають понад 6 кВт за хвилину в середньому, у яких основне споживання електроенергії припадає на пральну машину, сушарку, холодильник та освітлення:"+END)

PdAfter1800 = PdDataSet[(PdDataSet["DateTime"].dt.time >= pandas.Timestamp("18:00:00").time()) & (PdDataSet["SubMetering2"] > PdDataSet["SubMetering1"]) & (PdDataSet["SubMetering2"] > PdDataSet["SubMetering3"]) & ((PdDataSet["GlobalActivePower"]**2 + PdDataSet["GlobalReactivePower"]**2)**0.5 > 6)]
#Pandas
t1 =  timeit.timeit(stmt="PdDataSet[(PdDataSet['DateTime'].dt.time >= pandas.Timestamp('18:00:00').time()) & (NpDataSet['SubMetering2'] > NpDataSet['SubMetering1']) & (NpDataSet['SubMetering2'] > NpDataSet['SubMetering3']) & ((PdDataSet['GlobalActivePower']**2 + PdDataSet['GlobalReactivePower']**2)**0.5 > 6)]", number=9, globals=globals())
#Profiling

print(BROWN2+BOLD+"Pandas:\n"+END+END,PdAfter1800)
print(BROWN+BOLD+"Сер. Час виконання: "+END+str(t1)+END,"\n")

PdAfter1800FirstHalf = PdAfter1800.iloc[0:math.floor(PdAfter1800.shape[0]/2):3]
PdAfter1800SecondHalf = PdAfter1800.iloc[math.floor(PdAfter1800.shape[0]/2)::4]
#Pandas
t11 = timeit.timeit(stmt="PdAfter1800.iloc[0:math.floor(PdAfter1800.shape[0]/2):3]", number=9, globals=globals())
t12 = timeit.timeit(stmt="PdAfter1800.iloc[math.floor(PdAfter1800.shape[0]/2)::4]", number=9, globals=globals())
#Profiling

print(BROWN+"Кожен третій результат із першої половини:"+END)
print(PdAfter1800FirstHalf)
print(BROWN+BOLD+"Сер. Час виконання: "+END+str(t11)+END,"\n")
print(BROWN+"Кожен четвертий результат із другої половини:"+END)
print(PdAfter1800SecondHalf)
print(BROWN+BOLD+"Сер. Час виконання: "+END+str(t12)+END,"\n")


NpAfter1800 = NpDataSet[numpy.where((NpDataSet["SubMetering2"] > NpDataSet["SubMetering1"]) & (NpDataSet["SubMetering2"] > NpDataSet["SubMetering3"]) & ((NpDataSet["GlobalActivePower"]**2 + NpDataSet["GlobalReactivePower"]**2)**0.5 > 6) & (NpDataSet["Time"] >= "18:00:00"))]
#NumPy
t2 = timeit.timeit(stmt="NpDataSet[numpy.where((NpDataSet['SubMetering2'] > NpDataSet['SubMetering1']) & (NpDataSet['SubMetering2'] > NpDataSet['SubMetering3']) & ((NpDataSet['GlobalActivePower']**2 + NpDataSet['GlobalReactivePower']**2)**0.5 > 6) & (NpDataSet['Time'] >= '18:00:00'))]", number=9, globals=globals())
#Profiling

print(BROWN2+BOLD+"\nNumPy:\n"+END+END,NpAfter1800,"\n")
print(NpAfter1800.shape)
print(BROWN+BOLD+"Сер. Час виконання: "+END+str(t2)+END,"\n")

NpAfter1800FirstHalf = NpAfter1800[0:math.floor(NpAfter1800.shape[0]/2):3]
NpAfter1800SecondHalf = NpAfter1800[math.floor(NpAfter1800.shape[0]/2)::4]
#Pandas
t21 = timeit.timeit(stmt="NpAfter1800[0:math.floor(NpAfter1800.shape[0]/2):3]", number=9, globals=globals())
t22 = timeit.timeit(stmt="NpAfter1800[math.floor(NpAfter1800.shape[0]/2)::4]", number=9, globals=globals())
#Profiling

print(BROWN+"Кожен третій результат із першої половини:"+END)
print(NpAfter1800FirstHalf[:10])
print(NpAfter1800FirstHalf.shape)
print(BROWN+BOLD+"Сер. Час виконання: "+END+str(t21)+END,"\n")
print(BROWN+"Кожен четвертий результат із другої половини:"+END)
print(NpAfter1800SecondHalf[:10])
print(NpAfter1800SecondHalf.shape)
print(BROWN+BOLD+"Сер. Час виконання: "+END+str(t22)+END,"\n")







