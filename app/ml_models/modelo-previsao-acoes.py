
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from keras.models import Sequential
from keras.layers import LSTM, Dense

# Coleta de Dados
symbol = 'SAPR4.SA'
start_date = '2018-01-01'
end_date = '2024-07-01'
df = yf.download(symbol, start=start_date, end=end_date)

# Pré-processamento
df = df[['Close']]
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df)

# Função para criar séries temporais
def create_dataset(data, window=60):
    X, y = [], []
    for i in range(window, len(data)):
        X.append(data[i-window:i])
        y.append(data[i])
    return np.array(X), np.array(y)

window_size = 60
X, y = create_dataset(scaled_data, window_size)

# Divisão em treino e teste
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Reformatar para [amostras, tempo, features]
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Construção do Modelo LSTM
model = Sequential()
model.add(LSTM(units=50, return_sequences=False, input_shape=(X_train.shape[1], 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Treinamento
model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=1)

# Avaliação
predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions)
y_test_rescaled = scaler.inverse_transform(y_test)

mae = mean_absolute_error(y_test_rescaled, predictions)
rmse = np.sqrt(mean_squared_error(y_test_rescaled, predictions))
mape = np.mean(np.abs((y_test_rescaled - predictions) / y_test_rescaled)) * 100

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAPE: {mape:.2f}%")

# Visualização
plt.figure(figsize=(14, 6))
plt.plot(y_test_rescaled, label='Valor Real')
plt.plot(predictions, label='Valor Predito')
plt.title('Previsão de Fechamento de SAPR4.SA com LSTM')
plt.xlabel('Dias')
plt.ylabel('Preço de Fechamento (R$)')
plt.legend()
plt.grid(True)
plt.show()
# Salvamento em CSV
resultados = pd.DataFrame({
    'Valor_Real': y_test_rescaled.flatten(),
    'Valor_Predito': predictions.flatten()
})
resultados.to_csv('previsao_sapr4.csv', index=False)
print("Resultados salvos em 'previsao_sapr4.csv'")

"""EXPLORAÇÃO DO PREÇO DE FECHAMENTO DA AÇÃO SAPR4.SA"""

import yfinance as yf
import pandas as pd

# Coleta de Dados
symbol = 'SAPR4.SA'
start_date = '2018-01-01'
end_date = '2024-07-01'
df = yf.download(symbol, start=start_date, end=end_date)

# Exibição Tabular
print("Tabela com os dados de fechamento da SAPR4.SA:")
print(df[['Close']].head(10))  # Exibe os primeiros 10 registros

# Salvamento em CSV
df.to_csv('dados_sapr4_historico.csv', index=True)
print("Arquivo 'dados_sapr4_historico.csv' salvo com sucesso.")

print(df.describe())

df['Close'].plot(title='Preço de Fechamento SAPR4.SA')

!pip install tqdm

!pip install optuna

"""MODELO OTIMIZADO OPTUNA E CAMADA LSTM EXTRA E DROPOUT"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
import optuna
from tqdm import tqdm  # barra de progresso
import time

# Coleta de Dados
symbol = 'SAPR4.SA'
start_date = '2018-01-01'
end_date = '2024-07-01'
df = yf.download(symbol, start=start_date, end=end_date)
df = df[['Close']]

# Pré-processamento
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df)

def create_dataset(data, window=60):
    X, y = [], []
    for i in range(window, len(data)):
        X.append(data[i-window:i])
        y.append(data[i])
    return np.array(X), np.array(y)

window_size = 60
X, y = create_dataset(scaled_data, window_size)

# Treino/Teste
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Reshape
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Optuna - Otimização
def objective(trial):
    units1 = trial.suggest_int("units1", 30, 100)
    units2 = trial.suggest_int("units2", 30, 100)
    dropout_rate = trial.suggest_float("dropout_rate", 0.0, 0.4)
    lr = trial.suggest_float("lr", 1e-4, 1e-2, log=True)

    model = Sequential()
    model.add(LSTM(units=units1, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(dropout_rate))
    model.add(LSTM(units=units2))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)
    preds = model.predict(X_test)
    preds = scaler.inverse_transform(preds)
    y_true = scaler.inverse_transform(y_test)
    return mean_squared_error(y_true, preds)

study = optuna.create_study(direction="minimize")
historico_resultados = []

# Wrapper manual com barra
for trial_index in tqdm(range(20), desc="Rodando Optuna"):
    start_time = time.time()
    trial = study.ask()
    value = objective(trial)
    study.tell(trial, value)
    end_time = time.time()

    historico_resultados.append({
        'Número_do_Teste': trial.number,
        'Units_LSTM_1': trial.params.get('units1'),
        'Units_LSTM_2': trial.params.get('units2'),
        'Dropout': trial.params.get('dropout_rate'),
        'Taxa_Aprendizado': trial.params.get('lr'),
        'MSE': value,
        'Tempo_execucao_segundos': round(end_time - start_time, 2)
    })
# Salvamento em CSV
df_resultados = pd.DataFrame(historico_resultados)
df_resultados.to_csv('historico_optuna_sapr4.csv', index=False)
print("Histórico salvo em 'historico_optuna_sapr4.csv'")
print("Melhores hiperparâmetros encontrados:", study.best_params)

# Modelo Final com hiperparâmetros otimizados
best_params = study.best_params

model = Sequential()
model.add(LSTM(units=best_params['units1'], return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(Dropout(best_params['dropout_rate']))
model.add(LSTM(units=best_params['units2']))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=1)

# Avaliação
predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions)
y_test_rescaled = scaler.inverse_transform(y_test)

mae = mean_absolute_error(y_test_rescaled, predictions)
rmse = np.sqrt(mean_squared_error(y_test_rescaled, predictions))
mape = np.mean(np.abs((y_test_rescaled - predictions) / y_test_rescaled)) * 100

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAPE: {mape:.2f}%")

# Visualização
plt.figure(figsize=(14, 6))
plt.plot(y_test_rescaled, label='Valor Real')
plt.plot(predictions, label='Valor Predito')
plt.title('Previsão de Fechamento SAPR4.SA com LSTM Otimizado')
plt.xlabel('Dias')
plt.ylabel('Preço de Fechamento (R$)')
plt.legend()
plt.grid(True)
plt.show()

# Salvamento em CSV
resultados = pd.DataFrame({
    'Valor_Real': np.round(y_test_rescaled.flatten(), 2),
    'Valor_Predito': np.round(predictions.flatten(), 2)
})
resultados.to_csv('previsao_sapr4_otimizada.csv', index=False)
print("Resultados salvos em 'previsao_sapr4_otimizada.csv'")

# Salvamento do modelo completo em formato HDF5 o .h5 incluí tudo arquitetura, pesos treinados, otimizador, função de perda e etc
model.save('modelo_completo_lstm_sapr4.h5')
print("Modelo completo salvo como 'modelo_completo_lstm_sapr4.h5'")