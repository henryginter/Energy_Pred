# Energy_Pred

Hi! This is my solution for an assignment that I got from a job interview. The data preprocessing takes place in building.py and model creation takes place at mudel.py. I'm not sure yet whether this data is sensitive or not so I won't upload it for now.

# Test Assignment
The data of this test assignment comes in two csv files. The files contain the readings of various sensors of a building, data is given for two buildings 1 and 2 represented by files 1 and 2. The columns in the files are as follows:

 - reta_id – the unique id code of the sensor

- cat_var – the category of the sensor (described below)

- read_time – the timestamp of the sensor readout

- tag_value – the actual readout of the sensor

- cat_var have the following meanings:

- SR – solar radiation (W/m2)

- AT – ambient temperature (°C)

- ARH – ambient relative humidity (%)

- MBEP – building electricity consumption (W)

Building 1 has 4 electricity meters and building 2 has 6 meters. To get the total electricity consumption of a building at a particular moment, the readings of all power meters must be summed. If the readouts of some electricity meters are missing at a particular time point then the time points should be discarded.

## Analyse the consumption patterns of the buildings and summarise the key findings. Are there any noticeable differences in the consumption patterns of the two buildings? What could be the types of the two buildings?

On figure 1 you can see a typical energy consumption pattern of the two buildings on a workday. It seems that building #2 opens about an hour earlier and closes about 2 hours earlier.
![Figure 1](https://github.com/henryginter/Energy_Pred/blob/master/daily_pattern.png)

On figure 2 you can see a typical weekly energy consumption pattern. It seems that on weekends building #2 is closed and has only a base consumption. It’s also closed on national holidays. Meanwhile building #1 has basically the same pattern throughout the week.
![Figure 2](https://github.com/henryginter/Energy_Pred/blob/master/weekly_pattern.png)

On figure 3 you can see how solar radiation spikes create energy consumption peaks during the day.
![Figure 3](https://github.com/henryginter/Energy_Pred/blob/master/SR.png)

On figure 4 you can see clearly how the average weekly ambient temperature affects the average energy consumption of both buildings. Probably the ventilation consumption creates the repeating up and down patterns while temperature and radiation add seasonality trends.
![Figure 4](https://github.com/henryginter/Energy_Pred/blob/master/temp.png)

Building #2 reminds a bank, some office building or a school. Building #1 looks like a mall, hotel, cinema, grocery store or whatever building that has constant opening hours. 

## Try to build models that predict the energy consumption of the buildings. Estimate the performance of the models.

For both of the buildings 2 different models were trained:

- Multiple linear regression
- Artificial neural network regression

The purpose of the models is to predict energy hourly consumption 24 hours ahead. The following inputs were chosen for training:

- Energy consumption 24h ago

- Average ambient temperature of the previous day

- Average solar radiation of the previous day

- Average relative humidity of the previous day

- Month

- Weekday

- Hour

For building #2 another categorical input was added to distinguish between workdays and weekends. Also for Mondays the energy consumption 24h ago was set to the energy consumption of last Friday. For evaluating the models, R squared and root mean squared parameters were chosen. The datasets were split into training and test sets randomly with a ratio of 80/20 respectively.
```plain
+------------+---------------+---------------+---------------+---------------+
|            | B#1 MLR       | B#1 ANN       | B#2 MLR       | B#2 ANN       |
+            +---------------+---------------+---------------+---------------+
|            | Train | Test  | Train | Test  | Train | Test  | Train | Test  |
+------------+-------+-------+-------+-------+-------+-------+-------+-------+
| R^2        | 0.955 | 0.953 | 0.957 | 0.955 | 0.793 | 0.811 | 0.897 | 0.912 |
+------------+-------+-------+-------+-------+-------+-------+-------+-------+
| RMSE (kWh) | 46.02 | 46.75 | 45.00 | 45.84 | 92.10 | 89.13 | 64.80 | 60.52 |
+------------+-------+-------+-------+-------+-------+-------+-------+-------+
```
![Figure 5](https://github.com/henryginter/Energy_Pred/blob/master/b2_mlr.png)
![Figure 6](https://github.com/henryginter/Energy_Pred/blob/master/b2_ann.png)

For building #1 both models have quite good performance since the consumption pattern is similar every day. There should probably be more data for the ANN model to perform significantly better.

For building #2 the ANN model performed much better. As you can see on figure 5, the linear functions don’t handle weekends well. Saturdays seem like a mean between Sundays and Fridays (this was a repeating pattern). Possibly a better alternative would have been using polynomial or SVM regression. Note that the figures are a mix of  predictions based on training and test data. The actual test set hours were selected randomly, not with weekly intervals like on the figures.

Possible ways to improve the models:

- Change weekday input from continuous to multiple categorical inputs

- Take national holidays into account

- Train the model using the raw data instead of using hourly means

- Try adding more hidden layers to the ANN

- Try changing the number of neurons in the hidden layers

- Try different neuron functions

- Model a daily profile model with 24 energy con. inputs and outputs

- Add the energy consumption of the other building as an input
## Is there any correlation between the energy consumption of the two buildings?

There is a positive correlation with a value of 0.64 between the energy consumption of the buildings. On figure 7 you can see the mean line and marked out clusters of higher correlation.

Cluster #1 can probably be explained by the low base consumption of the buildings during night which mostly happens at the same time.

Cluster #2 is the peak operation of the buildings during work days.

Cluster #3 is the correlation on weekends and national holidays during the day – building #1 is operating at a nominal high power while building #2 is operating at nominal low power.

Higher correlation values could probably be achieved by separating the data into work days and weekends. The reason there are very sparse points in between high and low power mode is that the buildings open and close at different times.
![Figure 7](https://github.com/henryginter/Energy_Pred/blob/master/correlation.PNG)


