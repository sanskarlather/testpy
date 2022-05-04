import pandas as p
import numpy as n
import seaborn as s
import matplotlib.pyplot as mp

data_U=p.read_csv('urldata.csv')
print("Data obtained in last step")
print(data_U.head())
print("No. of rows and coloumns" )
print(data_U.shape)
print("Index of coloumns") 
print(data_U.columns)
print("Info about the data")
print(data_U.info())
data_U.hist(bins=50,figsize=(40,40))
mp.show()
mp.figure(figsize=(30,26))
s.heatmap(data_U.corr())
mp.show()

