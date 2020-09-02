##First import pandas for a better work with the csv
import pandas as pd
##Import date to convert date strings into date objects
from datetime import date
##Import pyplot
import matplotlib.pyplot as plt
##Import bioinfokit to use to create correlation maps
from bioinfokit import visuz
##Import os to create folders and move files
import os
##Import scipy.stats to obtain a numeric value of the correlation
from scipy.stats import spearmanr, pearsonr
##Import this to use the name of the variables as a strings
from varname import nameof

##Create an arry of the methods used
methods = ['pearson','spearman']

##Read the csv file, it's stored as a DataFrame structure
##Change the encoding because the file contains special characters from spanish
data = pd.read_csv('200901COVID19MEXICO.csv', encoding = 'latin')

############################################# Begin of cleaning ###################################################

##Pop the columns "Register Id", "Actualization date", "Country of origin", "Nationality Country" and "Date of death",
##so we can reduce the size of the DataFrame.
##These columns also don't contribute great information related to ICU usage
data.pop('ID_REGISTRO'); data.pop('FECHA_ACTUALIZACION');data.pop('FECHA_DEF');data.pop('PAIS_ORIGEN');data.pop('PAIS_NACIONALIDAD')
data.pop('MUNICIPIO_RES')

##Create a new column called DELTA
##This column DELTA represents the elapsed time (in days) between
##the beginning of the symptoms and the patient admission
cols = ['FECHA_INGRESO', 'FECHA_SINTOMAS']
for col in cols:
    data[col] = data[col].apply(lambda x: x.split('-'))
    data[col] = data[col].apply(lambda x: date(int(x[0]),int(x[1]),int(x[2])))

data['DELTA'] = data['FECHA_INGRESO']-data['FECHA_SINTOMAS']
data['DELTA'] = data['DELTA'].apply(lambda x: x.days)

##I pop the "Symptoms date" and the "Admission date" columns, so i can reduce the size of the DataFrame
data.pop('FECHA_INGRESO');data.pop('FECHA_SINTOMAS')

##I make a new variable that indicates if the patient's birth state is different to his home state
data['MOVILIDAD'] = (data['ENTIDAD_NAC']-data['ENTIDAD_RES'])
data['MOVILIDAD']=data['MOVILIDAD'].apply(lambda x: x+2 if x==0 else 1)
data.pop('ENTIDAD_NAC')

##In the other hand, I make a new variable that indicates if the patient has been hospitalized
##in a different state from his home state
data['TRANSF'] = (data['ENTIDAD_UM']-data['ENTIDAD_RES'])
data['TRANSF']=data['TRANSF'].apply(lambda x: x+2 if x==0 else 1)
#data.pop('ENTIDAD_RES')

##Print the info and the statistics of the DataFrame
print(data.info())
print(data.describe())

######################################## End of cleaning ##########################################################
##Function to analize the given data
def write(f,A,method):
    ##Write in the file the numeric values of the Pearson's correlation coefficient with the othe cols
    if method == 'pearson':
        f.write('Pearson\'s correlation coefficient ########################### \n')
        for col in A.columns:
            corr,_ = pearsonr(A['UCI'],A[col])
            f.write(f'Correlation with {col}: {corr} \n')
            pass
    ##Write in the file the numeric values of the Spearman's correlation coefficient with the othe cols
    else:
        f.write('Spearman\'s correlation coefficient ########################### \n')
        for col in A.columns:
            corr,_ = pearsonr(A['UCI'],A[col])
            f.write(f'Correlation with {col}: {corr} \n')
            pass
    pass
def Analysis(A,name,dt=None):
    ##Create the folder where the charts will be saved
    os.mkdir(name)
    ##Create the txt file where the numeric data will be written
    f = open(f'./{name}/correlations.txt','a')
    ##Iterate over the columns to create the charts
    for col in A.columns:
        labels = A[col].value_counts().index
        values = A[col].value_counts().values
        fig1, ax1 = plt.subplots()
        ax1.pie(values,labels=labels,shadow=True,autopct='%1.1f%%')
        ax1.axis('equal')
        ##Save the fig in the {given name} folder
        plt.savefig(f'./{name}/{col}')
        plt.close()
        pass
    ##Make this for the 2 methods
    for method in methods:
        if dt is not None:
            ##Create a correlation map of the secondary data
            visuz.stat.corr_mat(dt, corm=method)
            plt.close('all')
            write(f,dt,method)
        else:
            ##Create a correlation map of the principal data
            visuz.stat.corr_mat(A, corm=method)
            plt.close('all')
            write(f,A,method)

        ###Move the correlation map to the {given name} folder
        os.rename('./corr_mat.png',f'./{name}/{method}.png')
        pass
    f.close()
    pass


##Make the analysis of general data(without division by states) of patients in ICU
##First take all the patients in ICU
A=data[data['UCI']==1]
##Send to 'Analysis' Function the data of patients in ICU, and all the general data
Analysis(A,'GraficasGenerales',data)

##Separate the DataFrame into States according to the data dictionary
##Take the state of the medical unit where the patient is hospitalized
##This step below takes an array of boolean that indicates if the patient is hospitalized in the respective state
AGS = data['ENTIDAD_UM']== 1; BCA = data['ENTIDAD_UM']== 2  ##AGUASCALIENTES, BAJA CALIFORNIA
BCAS = data['ENTIDAD_UM']== 3; CPCHE = data['ENTIDAD_UM']== 4 ##BAJA CALIFORNIA SUR, CAMPECHE
COA = data['ENTIDAD_UM']== 5; CLMA = data['ENTIDAD_UM']== 6 ##COAHUILA, COLIMA
CHI = data['ENTIDAD_UM']== 7; CHUA = data['ENTIDAD_UM']== 8 ## CHIAPAS, CHIHUAHUA
CDMX = data['ENTIDAD_UM']== 9; DGO = data['ENTIDAD_UM']== 10 ##CDMX, DURANGO
GTO = data['ENTIDAD_UM']== 11; GRO = data['ENTIDAD_UM']== 12 ##GUANAJUATO, GUERRERO
HGO = data['ENTIDAD_UM']== 13; JAL = data['ENTIDAD_UM']== 14 ##HIDALGO, JALISCO
EDMX = data['ENTIDAD_UM']== 15; MICH = data['ENTIDAD_UM']== 16 ##ESTADO DE MEXICO, MICHOACAN
MOR = data['ENTIDAD_UM']== 17; NAY = data['ENTIDAD_UM']== 18 ##MORELOS, NAYARIT
NLN = data['ENTIDAD_UM']== 19; OAX = data['ENTIDAD_UM']== 20 ##NUEVO LEON, OAXACA
PBA = data['ENTIDAD_UM']== 21; QRO = data['ENTIDAD_UM']== 22 ##PUEBLA, QUERETARO
QROO = data['ENTIDAD_UM']== 23; SLP = data['ENTIDAD_UM']== 24 ##QUINTANA ROO, SAN LUIS POTOSI
SLOA = data['ENTIDAD_UM']== 25; SNRA = data['ENTIDAD_UM']== 26 ##SINALOA, SONORA
TBSCO = data['ENTIDAD_UM']== 27; TAM = data['ENTIDAD_UM']== 28 ##TABASCO, TAMAULIPAS
TLAX = data['ENTIDAD_UM']== 29; VRZ = data['ENTIDAD_UM']== 30 ##TLAXCALA, VERACRUZ
YCTN = data['ENTIDAD_UM']== 31; ZCS = data['ENTIDAD_UM']== 32 ##YUCATAN, ZACATECAS

##We define an array of States, so we can make things easier later
States = {'AGUASCALIENTES':AGS,'BAJA CALIFORNIA': BCA,'BAJA CALIFORNIA SUR':BCAS,'CAMPECHE':CPCHE,'COAHUILA': COA,'COLIMA':CLMA,
'CHIAPAS':CHI,'CHIHUAHUA': CHUA,'CDMX': CDMX,'DURANGO':DGO,'GUANAJUATO': GTO,'GUERRERO': GRO,'HIDALGO': HGO,'JALISCO': JAL,
'EDOMEX': EDMX,'MICHOACAN': MICH,'MORELOS': MOR,'NAYARIT': NAY,'NUEVOLEON': NLN,'OAXACA': OAX,'PUEBLA': PBA,'QUERETARO': QRO,
'QUINTANAROO': QROO,'SANLUIS': SLP,'SINALOA': SLOA,'SONORA': SNRA,'TABASCO': TBSCO,'TAMAULIPAS': TAM,'TLAXCALA': TLAX,
'VERACRUZ': VRZ,'YUCATAN': YCTN,'ZACATECAS': ZCS}

##Iterate over the States for individual analysis
for key, value in States.items():
    A = data[value]
    Analysis(A,key)
    pass
