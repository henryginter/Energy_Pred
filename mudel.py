import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = df1
dataset.index = pd.to_datetime(dataset.index)
dataset = dataset.resample('H').mean()

dataset['M'] = dataset.index.month
dataset['D'] = dataset.index.weekday
dataset['H'] = dataset.index.hour



X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, 3].values

# Taking care of missing data
from sklearn.preprocessing import Imputer
imputer = Imputer(missing_values = 'NaN', strategy = 'mean', axis = 0)
imputer = imputer.fit(X[:, 1:3])
X[:, 1:3] = imputer.transform(X[:, 1:3])