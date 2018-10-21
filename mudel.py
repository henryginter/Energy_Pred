import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error
from math import sqrt

# Importing the dataset from buildings.py
dataset = df1
dataset.index = pd.to_datetime(dataset.index)
dataset = dataset.resample('H').mean()

# Creating inputs form timestamps
dataset['M'] = dataset.index.month
dataset['D'] = dataset.index.weekday
dataset['H'] = dataset.index.hour
dataset['e24'] = dataset['mbep_sum1'].shift(24) # Creating an input from power consumption 24h ago

# Taking daily means from sensor data, shifting them 24h and filling empty rows
dataset['t_day'] = dataset[5988].resample('D').mean()
dataset['hum_day'] = dataset[7821].resample('D').mean()
dataset['sr_day'] = dataset[7815].resample('D').mean()
dataset['t_day'] = dataset['t_day'].fillna(method='ffill').shift(24)
dataset['hum_day'] = dataset['hum_day'].fillna(method='ffill').shift(24)
dataset['sr_day'] = dataset['sr_day'].fillna(method='ffill').shift(24)

# Create work_day category for building number 2 and shift e24 for additional 48 hours on Mondays
#dataset['work_day'] = 1
#mask = dataset['D'] > 4
#dataset.loc[mask, 'work_day'] = 0
#mask = dataset['D'] == 0
#dataset.loc[mask, 'e24'] = dataset['e24'].shift(48)

# Removing rows with nan values
col = ['e24', 't_day', 'hum_day', 'sr_day', 7821]
for i in col:
    dataset = dataset[pd.notnull(dataset[i])] 

# Defining dependent and independent values (differs for building #2)
X = dataset.iloc[:, 8:15].values
y = dataset.iloc[:, 4].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Importing the Keras libraries and packages
import keras
from keras.models import Sequential
from keras.layers import Dense

# Initialising the ANN
regressor = Sequential()

# Adding the input layer and the hidden layer
regressor.add(Dense(output_dim = 7, activation = 'relu', input_dim = 7))

# Adding the output layer
regressor.add(Dense(output_dim = 1, activation = 'linear'))

# Compiling the ANN
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

# Fitting the ANN to the Training set
regressor.fit(X_train, y_train, batch_size = 10, nb_epoch = 1000)

# Part 3 - Predicting Test set results
y_pred = regressor.predict(X_test)

# Fitting Multiple Linear Regression to the Training set (Skip this if you want the scores and plot of ANN)
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)

# Finding R^2 and RMSE
from sklearn.metrics import r2_score
R2 = r2_score(y_test, y_pred)
rms = sqrt(mean_squared_error(y_test, y_pred))

#Plot predicted and real data
plt.plot(y_test, color = 'red', label = 'Real data')
plt.plot(y_pred, color = 'blue', label = 'Predicted data')
plt.title('Prediction')
plt.legend()
plt.show()
