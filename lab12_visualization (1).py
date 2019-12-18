

import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns

import pandas as pd
import sqlite3

#create a database named "DCA.db" in the folder where this code is located
conn = sqlite3.connect("DCA.db")  #It will only connect to the DB if it already exists

#create data table to store summary info about each case/well
cur = conn.cursor()


##Syntax to add new columns to a table
#cur.execute("ALTER TABLE Rates ADD rateID INTEGER;")
#conn.commit()

#Syntax to delete a table
#cur.execute("DROP TABLE DCAparams;")
#cur.execute("DROP TABLE Rates;")
#conn.commit()

#Custom Plot parameters
titleFontSize = 18
axisLabelFontSize = 15
axisNumFontSize = 13


#RUN THIS TO CREATE A NEW TABLE
#cur.execute("CREATE TABLE DCAparams (wellID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,  qi REAL, Di REAL, b REAL, fluid TEXT)")
#conn.commit()

dfLength = 24
gasWellID = np.random.randint(1,17,5)   #arguments are low, high, size




#1

for wellID in range(1,18):
    
    productDF = pd.read_sql_query(f"SELECT time,rate,Cum FROM Rates WHERE wellID = {wellID};", conn)    
    DCA_Df = pd.read_sql_query("SELECT * FROM DCAparams;", conn)
    
    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()
    ax1.plot(productDF['time'], productDF['rate'], color = "red", ls = 'None', marker = 'o', markersize = 3)
    ax2.plot(productDF['time'], productDF['Cum'] / 1000, 'b-')
    
    ax1.set_xlabel('Time, Months')
    ax1.set_ylabel('Production Rate, bopm', color = 'g')
    ax2.set_ylabel('Cumulative Oil Production, Mbbls', color = 'b')
    
    plt.show()
    
#2
for wellID in range(1,18):
    
    productDF = pd.read_sql_query(f"SELECT time FROM Rates WHERE wellID = {wellID};", conn)    
    DCA_DF = pd.read_sql_query("SELECT wellID FROM DCAparams WHERE fluid = 'gas';", conn) 
j = 1
for x in DCA_DF['wellID']:
    productDF['Well' + str(x)] = pd.read_sql_query(f"SELECT rate FROM Rates WHERE wellID = {x};", conn)
    
production = productDF.iloc[:,1:].to_numpy()
time = productDF['time'].to_numpy()
labels = productDF.columns
labels = list(labels[1:])
print(labels)
fig, ax = plt.subplots()
ax.stackplot(time, np.transpose(production),labels = labels)
ax.legend(loc = 'upper right')
plt.title('Stacked Field Gas Production')
plt.show()

#3
for wellID in range(1,18):
    productDF = pd.read_sql_query(f"SELECT time FROM Rates WHERE wellID = {wellID};", conn)    
    DCA_DF = pd.read_sql_query("SELECT wellID FROM DCAparams WHERE fluid = 'oil';", conn)  
j = 1
for x in DCA_DF['wellID']:
    productDF['Well' + str(x)] = pd.read_sql_query(f"SELECT rate FROM Rates WHERE wellID = {x};", conn)

productDF
production = productDF.iloc[:,1:].to_numpy()
time = productDF['time'].to_numpy()
labels = productDF.columns
labels = list(labels[1:])
fig, ax = plt.subplots()
ax.stackplot(time, np.transpose(production),labels = labels)
ax.legend(loc = 'upper right')
plt.title('Stacked Field Oil Production')
plt.show()

#4
x = 6
ind = np.arange(1,x+1) 
months = ['January','February','March','April','May','June']
result = np.zeros(len(months))
labels=[]
loc_plts = []
width = 0.5
for wellID in range(1,18):
    cumDF = pd.read_sql_query(f"SELECT time FROM Rates WHERE wellID = {wellID};", conn)    
    dcaDF = pd.read_sql_query("SELECT wellID FROM DCAparams WHERE fluid = 'gas';", conn) 
for z in dcaDF['wellID']:
    cumDF['Well' + str(z)] = pd.read_sql_query(f"SELECT Cum FROM Rates WHERE wellID = {z};", conn)
j = 1
for z in dcaDF['wellID']:
   p1 = plt.bar(cumDF['time'][0:x], cumDF['Well' + str(z)][0:x]/1000,width, bottom = result)
   labels.append('Well' + str(z))
   loc_plts.append(p1)
   plt.ylabel('Gas Production, Mbbls')
   plt.title('Cumulative Gas Production')
   plt.xticks(ind, months, fontweight = 'bold')
   j += 1
   split = cumDF.iloc[0:6,1:j].to_numpy() 
   result = np.sum(a=split,axis=1) / 1000
plt.legend(loc_plts,labels)   
plt.show(loc_plts)

#5
x = 6
ind = np.arange(1,x+1) 
months = ['January','February','March','April','May','June']
result = np.zeros(len(months))
labels = []
loc_plts = []
width = 0.5
for wellID in range(1,18):   
    cumDF = pd.read_sql_query(f"SELECT time FROM Rates WHERE wellID = {wellID};", conn)    
    dcaDF = pd.read_sql_query("SELECT wellID FROM DCAparams WHERE fluid = 'oil';", conn) 
for z in dcaDF['wellID']: 
    cumDF['Well' + str(z)] = pd.read_sql_query(f"SELECT Cum FROM Rates WHERE wellID = {z};", conn)
k = 1
for z in dcaDF['wellID']:
   p1 = plt.bar(cumDF['time'][0:x], cumDF['Well' + str(z)][0:x] / 1000, width, bottom = result)
   labels.append('Well' + str(z))
   loc_plts.append(p1)
   plt.ylabel('Oil Production, Mbbls')
   plt.title('Cumulative Oil Production')
   plt.xticks(ind, months, fontweight = 'bold')
   k += 1
   split = cumDF.iloc[0:6,1:k].to_numpy() 
   result = np.sum(a=split,axis=1) / 1000
 
plt.legend(loc_plts,labels)  
loc_plts = plt.figure(figsize = (36,20),dpi = 100)

#6
i have no idea how to do this

