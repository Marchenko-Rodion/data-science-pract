from spyre import server

import pandas
import numpy
import os
import math
import urllib
import matplotlib
from datetime import datetime

BOLD = '\033[1m'
END = '\033[0m'

#Marchenko rodion Data Analisys prakt №3


#Defining inputs and outputs for the web-app running on DataSpyre
#Spyre is a Web Application Framework for providing a simple user interface for Python data projects.
class StockExample(server.App):
    title = "База даних стану рослинності України \U0001f1fa\U0001f1e6 \U0001f343"

    #Here defined the needed inputs for selecting information samples
    inputs = [{     "type":'dropdown',
                    "label": 'Виберіть тип даних',
                    "options" : [ {"label": "VHI (Індекс здоровʼя рослинності)", "value":"VHI"},
                                  {"label": "VCI (Індекс посушливості)", "value":"VCI"},
                                  {"label": "TCI (Індекс температури)", "value":"TCI"}],
                    "key": 'Typ',
                    "action_id": "updateOut1"},
              
              {     "type":'dropdown',
                    "label": 'Виберіть область',
                    "options" : [ {"label": "Вінницька", "value":"Вінницька"},
                                  {"label": "Волинська", "value":"Волинська"},
                                  {"label": "Дніпропетровська", "value":"Дніпропетровська"},
                                  {"label": "Донецька", "value":"Донецька"},
                                  {"label": "Житомирська", "value":"Житомирська"},
                                  {"label": "Закарпатська", "value":"Закарпатська"},
                                  {"label": "Запорізька", "value":"Запорізька"},
                                  {"label": "Івано-Франківська", "value":"Івано-Франківська"},
                                  {"label": "Київська", "value":"Київська"},
                                  {"label": "Кіровоградська", "value":"Кіровоградська"},
                                  {"label": "Луганська", "value":"Луганська"},
                                  {"label": "Львівська", "value":"Львівська"},
                                  {"label": "Миколаївська", "value":"Миколаївська"},
                                  {"label": "Одеська", "value":"Одеська"},
                                  {"label": "Полтавська", "value":"Полтавська"},
                                  {"label": "Рівенська", "value":"Рівенська"},
                                  {"label": "Сумська", "value":"Сумська"},
                                  {"label": "Тернопільська", "value":"Тернопільська"},
                                  {"label": "Харківська", "value":"Харківська"},
                                  {"label": "Херсонська", "value":"Херсонська"},
                                  {"label": "Хмельницька", "value":"Хмельницька"},
                                  {"label": "Черкаська", "value":"Черкаська"},
                                  {"label": "Чернівецька", "value":"Чернівецька"},
                                  {"label": "Чернігівська", "value":"Чернігівська"},
                                  {"label": "Республіка Крим", "value":"Республіка Крим"},
                                  {"label": "м. Київ", "value":"м. Київ"},
                                  {"label": "м. Севастополь", "value":"м. Севастополь"}],
                    "key": 'Obl',
                    "action_id": "updateOut2"},
              
              {     "type":'text',
                    "label": 'Виберіть роки',
                    "value" : '2015',
                    "key": 'YearSelect',
                    "action_id" : "updateOut3", },
              
              {     "type":'text',
                    "label": 'Виберіть тижні року',
                    "value" : '1',
                    "key": 'WeekSelect',
                    "action_id" : "updateOut4", }]
    
    
    #Here defined the select controls (Enter button)
    controls = [{    "type" : "hidden",
                    "id" : "UpdateData"},
                {    "type" : "button",
                     "label": '\U000021B3 Ввід',
                    "id" : "UpdateData"}]
    
    #Here defined the displayed data tabs
    tabs = ["Графік", "Таблиця"]

    #Here defined the output positions and processing name methods
    outputs = [{"type" : 'html', "id" : 'updatePlotTabText',"control_id" : 'UpdateData', "tab" : "Графік"},
               {"type" : 'plot', "id" : 'updatePlot',"control_id" : 'UpdateData', "tab" : "Графік"}, 
               {"type" : 'html', "id" : 'updateTableTabText',"control_id" : 'UpdateData', "tab" : "Таблиця"},
               {"type" : "table","id" : "updateTable","control_id" : "UpdateData", "tab" : "Таблиця","on_page_load" : True }]



#DATA ANALYSING FUNCTIONS

    #This function loads dataset CSV table from the internet
    def LoadClimateDatasetAsCSV(self, WorkDir,RegionID,BeginYear,EndYear):
        url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?provinceID="+str(RegionID)+"&country=UKR&yearlyTag=Weekly&type=Mean&TagCropland=crop&year1="+str(BeginYear)+"&year2="+str(EndYear)
        CurrentTime = datetime.now().strftime("%d-%m-%y-%H-%M-%S")
        Filename = WorkDir+"/Vegetation-health-index-UKR-provinceNo"+str(RegionID)+"--"+CurrentTime+".csv"
        urllib.request.urlretrieve(url,Filename)
        print("\t» Downloaded: Vegetation-health-index-UKR-provinceNo"+str(RegionID)+"--"+CurrentTime+".csv")
        return Filename


    #This function reads datasets as pandas frames and performs some preprocessing
    def ReadDatasetToCSV(self, WorkDir):
        DataFrames = []
        headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty'] #CSV table headers
        print("\n»» "+BOLD+"Loading data from files:"+END)
        for path in os.listdir(WorkDir):
            FullPath = os.path.join(WorkDir, path)
            if (os.path.isfile(FullPath) and path[-4:] == ".csv"): # check if current path is a CSV file
                print(path)
                df = pandas.read_csv(FullPath, header = 1, names = headers)
                df = df.drop(df.loc[df["VHI"] == -1].index) #Drop empty value rows for VHI
                df = df.drop(labels="empty", axis=1) #Drop empty column
                df = df.drop(labels="SMN", axis=1) #Drop SMN column
                df = df.drop(labels="SMT", axis=1) #Drop SMT column
                df.loc[0, "Year"] = df["Year"][1] #Fix year value in first row (get rid of html tags)
                df = df.dropna(subset=["VHI"]) #Drop rows with NaN in for VHI
                df = df.astype({"Year": "int32"}) #Convert year column to integer for easy indexation

                pathNameArray = path.split("-")
                df["province"] = int(pathNameArray[4][10:]) #Extract province code from predetermined file name and add it as a column
                
                DataFrames.append(df)
        FullData = pandas.concat(DataFrames) #Coalesce all data into a single dataframe
        FullData = FullData.reset_index(drop=True) #Reset global index without preserving the old one
        print("\n"+"="*75)
        print(FullData)
        return FullData


    #This function replaces province IDs inside dataframe for a more readable Name Identifier
    def ProvinceIdToNames(self, FullData):
        ReplacementsDict = {1:22, 2:24, 3:23, 4:25, 5:3, 6:4, 7:8, 8:19, 9:20, 10:21, 11:9, 12:26, 13:10, 14:11, 15:12, 16:13, 17:14, 18:15, 19:16, 20:27, 21:17, 22:18, 23:6, 24:1, 25:2, 26:7, 27:5}
        FullData["province"].replace(ReplacementsDict, inplace = True)
        
        ReplacementsDict2 = {1:"Вінницька", 2:"Волинська", 3:"Дніпропетровська", 4:"Донецька", 5:"Житомирська", 6:"Закарпатська", 7:"Запорізька", 8:"Івано-Франківська", 9:"Київська", 10:"Кіровоградська", 11:"Луганська", 12:"Львівська", 13:"Миколаївська", 14:"Одеська", 15:"Полтавська", 16:"Рівенська", 17:"Сумська", 18:"Тернопільська", 19:"Харківська", 20:"Херсонська", 21:"Хмельницька", 22:"Черкаська", 23:"Чернівецька", 24:"Чернігівська", 25:"Республіка Крим", 26:"м. Київ", 27:"м. Севастополь"}
        FullData["province"].replace(ReplacementsDict2, inplace = True)
        print("\n"+"="*75)
        print(FullData)


    #This function loads the initial dataset files from the Internet to the computer, if not already present
    def InitializeLoad(self):
        #Creating temporary directory if it does not exist
        CurrentDirectory = os.getcwd()
        if (os.getcwd()[-13:] != "/DataLab2-tmp"):
            try:
                os.chdir(CurrentDirectory+"/DataLab2-tmp")
            except:
                try:
                    os.makedirs(CurrentDirectory+"/DataLab2-tmp")
                    print("»» Created tmp directory /DataLab2-tmp.")
                except FileExistsError:
                    # directory already exists
                    pass
                os.chdir(CurrentDirectory+"/DataLab2-tmp") #GO TO DATASET DIRECTORY!!!
         
        print("»» The current working directory is: "+os.getcwd()+".")
        print("\n")


        #Loading vegetation data for all provinces of Ukraine
        CWD = os.getcwd()
        AvailableFiles = os.listdir(CWD)
        for province in range(1,28):
            if any("Vegetation-health-index-UKR-provinceNo"+str(province) in path for path in AvailableFiles):
                pass
            else:
                try:
                    Filename = self.LoadClimateDatasetAsCSV(CWD,province,1982,2024)
                except:
                    print("\t» Failed to load for province №",province)
        print("»» Loaded all!!!")
        return


    #This function selects the subset of data from the  full dataset by year and week span
    def GetDataByPeriod(self,FullData,ProvinceName,BeginYear,EndYear,BeginWeek,EndWeek):
        yearset = FullData[(FullData["province"] == ProvinceName) & (FullData["Year"] >= BeginYear)  & (FullData["Year"] <= EndYear) & (FullData["Week"] >= BeginWeek)  & (FullData["Week"] <= EndWeek) ]
        return yearset


    #This function takes a range of integers as a string and extracts the begining and end ("3-15" => begin=3, end=15)
    def PeriodQueryToInt(self,query):
        StrippedQerry = query.strip().split("-")
        if (len(StrippedQerry) == 1):
            return[int(StrippedQerry[0]), int(StrippedQerry[0])]
        
        elif (len(StrippedQerry) == 2):
            StrippedQerry[0] = StrippedQerry[0].strip()
            StrippedQerry[1] = StrippedQerry[1].strip()
            try:
                if (int(StrippedQerry[0]) > int(StrippedQerry[1])):
                        StrippedQerry[0], StrippedQerry[1] = StrippedQerry[1], StrippedQerry[0]
                return[int(StrippedQerry[0]), int(StrippedQerry[1])]
            except:
                return [0,0]
                
        else:
            return [0,0]


# PROCESSING METHODS. They get called everytime an output object is displayed in browser window

    def updatePlotTabText(self, params):
        Type = params["Typ"]
        Years = self.PeriodQueryToInt(params["YearSelect"])
        return "<h1><i>Графік %s за %d - %d рік</i></h1>" % (Type, Years[0], Years[1])
    
    def updateTableTabText(self, params):
        Type = params["Typ"]
        Years = self.PeriodQueryToInt(params["YearSelect"])
        return "<h1><i>VCI,TCI,VHI за %d - %d рік</i></h1>" % (Years[0], Years[1])


    def updateTable(self, params):
        print("="*80,"\nSTARTING TO DRAW TABLE")
        self.InitializeLoad()
        FullDataSet = self.ReadDatasetToCSV(os.getcwd())
        self.ProvinceIdToNames(FullDataSet)
            
        Years = self.PeriodQueryToInt(params["YearSelect"])
        Weeks = self.PeriodQueryToInt(params["WeekSelect"])
              
        #Selecting data from the dataset    
        DataCut = self.GetDataByPeriod(FullDataSet,params["Obl"],Years[0],Years[1],Weeks[0],Weeks[1])
        DataCut.rename(columns={'Year': 'РІК', 'Week': 'ТИЖДЕНЬ', 'province': 'ОБЛАСТЬ'}, inplace=True)
        print(DataCut)
        return DataCut.head(150)
    
    
    def updatePlot(self, params):
        print("="*80,"\nSTARTING TO DRAW PLOT")
        self.InitializeLoad()
        FullDataSet = self.ReadDatasetToCSV(os.getcwd())
        self.ProvinceIdToNames(FullDataSet)
            
        Years = self.PeriodQueryToInt(params["YearSelect"])
        Weeks = self.PeriodQueryToInt(params["WeekSelect"])
        
        #Selecting data from the dataset
        DataCut = self.GetDataByPeriod(FullDataSet,params["Obl"],Years[0],Years[1],Weeks[0],Weeks[1])[["Year","Week", params["Typ"]]]  

        #Plotting multiple graphs on one figure, one by one
        plt = DataCut[(DataCut["Year"] == Years[0])].plot(figsize=(14, 10.5), fontsize=16, linewidth=2, x="Week", y=params["Typ"])
        for i in range(Years[0]+1, Years[1]+1):
            DataCut[(DataCut["Year"] == i)].plot(ax=plt,figsize=(14, 10.5), fontsize=16, linewidth=2, x="Week", y=params["Typ"])
            
        #Setting up the look of the plot
        plt.legend(list(range(Years[0], Years[1]+1)), loc="upper left", fontsize="16", shadow=True)
        plt.grid(linestyle=':', linewidth=1)
        if(Weeks[1] - Weeks[0] < 30):
            plt.set_xticks(list(range(Weeks[0], Weeks[1]+1, 1))) #Smaller X axis step
        else:
            plt.set_xticks(list(range(Weeks[0], Weeks[1]+1, 2))) #Wider X axis step
        plt.set_xlabel("Тиждень", fontsize="14", fontweight="bold")
        plt.set_ylabel("Значення "+params["Typ"], fontsize="14", fontweight="bold", rotation="vertical")
        return plt



#Launch app instance on localhost
app = StockExample()
app.launch(port=9093)