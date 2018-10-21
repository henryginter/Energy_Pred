import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA

# Importing the datasets
df1 = pd.read_csv('building el consumption data 1.csv', sep=';')
df2 = pd.read_csv('building el consumption data 2.csv', sep=';')
remove_list = [2818, 7815, 7821, 5988] # Removing duplicate/empty sensor data
for i in remove_list:
    df2 = df2[df2['reta_id'] != i]
df = pd.concat([df1, df2]) # Joining dataframes together to reformat the data

# Creating separate columns for sensors
onehot = pd.get_dummies(df['reta_id']) 
df = df.drop(['reta_id'], axis =1)
df = pd.concat([df, onehot], axis=1)

# Assigning tag values to correct sensor columns
col = list(onehot)
for i in col:
    df[i] = np.where(df[i]==1, df['tag_value'], np.NaN)

mbep1_col = col[9:13] # Building #1 power consumption columns
mbep2_col = col[0:6] # Building #2 power consumption columns
sen_col = list(set(col) - set(mbep1_col+mbep2_col)) # Sensor columns
df = df.drop(['cat_var', 'tag_value'], axis = 1) # Removing unnecessary columns
df = df.groupby('read_time').sum() # Combining rows with same timestamp

# Separating data into different dataframes to clear empty values
df1 = df[mbep1_col]
df2 = df[mbep2_col]
df3 = df[sen_col]
for i in mbep1_col:
    df1 = df1[df1[i] != 0]
for i in mbep2_col:
    df2 = df2[df2[i] != 0]
    
# Removing anomalous humidity readings
mask = df3[7821] > 100.06
df3.loc[mask, 7821] = np.NaN

# Summing up power meters
df1['mbep_sum1'] = df1[mbep1_col].sum(axis = 1)
df2['mbep_sum2'] = df2[mbep2_col].sum(axis = 1)

# Joining sensor data back to power data and taking hourly means
df1 = pd.concat([df1, df3], axis=1, join_axes=[df1.index])
df1.index = pd.to_datetime(df1.index)
df1 = df1.resample('H').mean()
df2 = pd.concat([df2, df3], axis=1, join_axes=[df2.index])
df2.index = pd.to_datetime(df2.index)
df2 = df2.resample('H').mean()

# For creating models of df1 or df2, continue to mudel.py. For creating plots, continue below



# Joining dataframes together for plotting
dataset = pd.DataFrame()
dataset = dataset.join(df1['mbep_sum1'], how='outer')
dataset = dataset.join(df2['mbep_sum2'], how='outer')
dataset = dataset.join(df3, how='outer')
dataset.index = pd.to_datetime(dataset.index)
dtestX = dataset.resample('H').mean()

# Find correlation value cor and create correlation plot
from numpy.polynomial.polynomial import polyfit
col = ['mbep_sum1', 'mbep_sum2']
for i in col:
    dtestX = dtestX[pd.notnull(dtestX[i])] 
x = dtestX['mbep_sum1']
y = dtestX['mbep_sum2']
b, m = polyfit(x, y, 1)
cor = np.corrcoef(x, y)
plt.style.use('ggplot')
plt.scatter(x, y)
plt.plot(x, b + m * x, 'blue')
plt.xlabel('Building 1 consumption (kW)')
plt.ylabel('Building 2 consumption (kW)')
plt.show()

# Create unified plot for general analysis
plt.style.use('ggplot')
plt.plot(dtestX.index, dtestX[7815], 'red', label ='Solar radiation')
plt.plot(dtestX.index, dtestX[7821], 'gray', label ='Humidity')
plt.plot(dtestX.index, dtestX['mbep_sum1'], 'blue', label ='Energy con.')
plt.plot(dtestX.index, dtestX['mbep_sum2'], 'indigo', label ='Energy con2')
plt.plot(dtestX.index, dtestX[5988], 'orange', label ='Ambient Temperature')
plt.legend(loc='upper left')
plt.show()

# Energy consumption and ambient temperature plot with separate y-axises
plt.style.use('ggplot')
from matplotlib import rc
rc('mathtext', default='regular')
fig = plt.figure()
ax = fig.add_subplot(111)
lns1 = ax.plot(dtestX.index, dtestX['mbep_sum1'], 'blue', label = 'Building #1')
lns2 = ax.plot(dtestX.index, dtestX['mbep_sum2'], 'indigo', label = 'Building #2')
ax2 = ax.twinx()
lns3 = ax2.plot(dtestX.index, dtestX[5988], '-r', label = 'Ambient temperature')
lns = lns1+lns2+lns3
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)
ax.grid()
ax.set_xlabel("Time (week)")
ax.set_ylabel(r"Average weekly energy consumption (kW)")
ax2.set_ylabel(r"Temperature ($^\circ$C)")
ax2.set_ylim(0, 35)
ax.set_ylim(0,1000)
plt.show()


