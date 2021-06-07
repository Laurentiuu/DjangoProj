from rest_framework.generics import ListAPIView
from sklearn.model_selection import train_test_split

from .models import Weather
from .serializers import WheatherSerializers
from .getDataFromAPI import getData
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Bidirectional
import numpy as np
import pandas as pd


def prezicere(trainData, coloana):
    input = trainData.drop(coloana, axis=1)
    output = trainData.pop(coloana)

    # fac split la date(doua seturi de date)
    trainInput, testInput, trainOutput, testOutput = train_test_split(input, output, test_size=0.25, random_state=3)

    # creez modelul si antrenez reteaua
    model = LinearRegression()
    model.fit(trainInput, trainOutput)
    prediction = model.predict(testInput)
    pred = np.mean((prediction - testOutput) ** 2)
    print(pd.DataFrame({'actual': testOutput, 'prediction': prediction, 'diff': (testOutput - prediction)}))
    print(pred)


# am gasit o retea neuronala dar nu merge
def rnn(trainData):
    dataset = trainData.dropna(subset=['pressure'])
    dataset = trainData.reset_index(drop=True)
    training_set = dataset.iloc[:, 4:5].values
    sc = MinMaxScaler(feature_range=(0, 1))
    training_set_scaled = sc.fit_transform(training_set)
    x_train = []
    y_train = []
    n_future = 4  # next 4 days temperature forecast
    n_past = 30  # Past 30 days
    for i in range(0, len(training_set_scaled) - n_past - n_future + 1):
        x_train.append(training_set_scaled[i: i + n_past, 0])
        y_train.append(training_set_scaled[i + n_past: i + n_past + n_future, 0])
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    regressor = Sequential()
    regressor.add(Bidirectional(LSTM(units=30, return_sequences=True, input_shape=(x_train.shape[1], 1))))
    regressor.add(Dropout(0.2))
    regressor.add(LSTM(units=30, return_sequences=True))
    regressor.add(Dropout(0.2))
    regressor.add(LSTM(units=30, return_sequences=True))
    regressor.add(Dropout(0.2))
    regressor.add(LSTM(units=30))
    regressor.add(Dropout(0.2))
    regressor.add(Dense(units=n_future, activation='linear'))
    regressor.compile(optimizer='adam', loss='mean_squared_error', metrics=['acc'])
    # read test dataset
    testdataset = pd.read_json('date.json')
    # get only the temperature column
    testdataset = testdataset.iloc[:30, 3:4].values
    real_temperature = pd.read_json('date.json')
    real_temperature = real_temperature.iloc[30:, 3:4].values
    testing = sc.transform(testdataset)
    testing = np.array(testing)
    testing = np.reshape(testing, (testing.shape[1], testing.shape[0], 1))
    predicted_temperature = regressor.predict(testing)
    predicted_temperature = sc.inverse_transform(predicted_temperature)
    predicted_temperature = np.reshape(predicted_temperature,
                                       (predicted_temperature.shape[1], predicted_temperature.shape[0]))
    print(predicted_temperature)


class WeatherListView(ListAPIView):
    days = [1514832008.0, 1515696008.0, 1516560008.0]
    # daca vreau sa iau date pentru 3 zile diferite
    # for i in range(0, len(days)):
    #     data = getData(days[i])
    data = getData(days[0])

    # creez dataFrame-ul si le afisez
    trainData = pd.DataFrame([i.createDict() for i in Weather.objects.all()])
    aux = trainData
    # fac prezicere pentru temperatura, vizibilitate si directia vantului(doar datele astea le-am luat din API)
    print('Prezicere pentru temperatura aerului:\n')
    prezicere(aux, 'airTemperature')
    print('Prezicere pentru vizibilitate:\n')
    prezicere(aux, 'visibility')
    print('Prezicere pentru directia vantului:\n')
    prezicere(aux, 'windDirection')

    # rnn(trainData)

    val_dataframe = trainData.sample(frac=0.2, random_state=1337)
    train_dataframe = trainData.drop(val_dataframe.index)

    print(
        "Folosesc %d samples pentru training si %d pentru validare"
        % (len(train_dataframe), len(val_dataframe))
    )
    print('\n')

    queryset = Weather.objects.all()
    serializer_class = WheatherSerializers
