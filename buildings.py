import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
df1 = pd.read_csv('building el consumption data 1.csv', sep=';')
df2 = pd.read_csv('building el consumption data 2.csv', sep=';')
remove_list = [2818, 7815, 7821]
for i in remove_list:
    df2 = df2[df2['reta_id'] != i]
df = pd.concat([df1, df2]).drop_duplicates(subset=['reta_id', 'READ_TIME'])

#dtest = dataset[dataset.index>38073]

onehot = pd.get_dummies(df['reta_id']) 
df = df.drop(['reta_id'], axis =1)
df = df.join(onehot)

col = list(onehot)
for i in col:
    df[i] = np.where(df[i]==1, df['TAG_VALUE'], 0)
df = df[df[7821] <= 100]
df = df.drop(['CAT_VAR', 'TAG_VALUE'], axis = 1)
df = df.groupby('READ_TIME').sum()
mbep1_col = col[8:12]
mbep2_col = col[0:6]
for i in mbep1_col:
    dtest = dtest[dtest[i] != 0]
dtest['mbep_sum'] = dtest[mbep_columns].sum(axis = 1)

dtest.index = pd.to_datetime(dtest.index)
dtestX = dtest.resample('H').mean()

plt.plot(dtestX.index, dtestX[7815], 'r', label ='Solar radiation')
plt.plot(dtestX.index, dtestX[7821], 'pink', label ='Humidity')
plt.plot(dtestX.index, dtestX['mbep_sum'], 'b', label ='Energy con.')
plt.plot(dtestZ.index, dtestZ['mbep_sum'], 'indigo', label ='Energy con2')
plt.show()

dtest.to_csv('1_H.csv')

compare = pd.DataFrame()
compare
