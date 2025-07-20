# app/services/prediction.py
from datetime import datetime, timedelta
import yfinance as yf
import numpy as np
from keras.models import load_model
import joblib  # para carregar scaler salvo com pickle ou joblib

# Caminhos relativos aos arquivos salvos
MODELO_PATH = "app/ml_models/modelo_completo_lstm_sapr4.h5"
SCALER_PATH = "app/ml_models/scaler_sapr4.gz"

# Função principal
def prever_preco(data: datetime) -> float:
    print(f"🟢 Iniciando previsão para a data: {data}")
    
    model = load_model(MODELO_PATH)
    scaler = joblib.load(SCALER_PATH)
    
    print("✅ Modelo carregado")    
    print("✅ Scaler carregado")

    # Buscar últimos 90 dias antes da data
    start_date = data - timedelta(days=360)
    end_date = data + timedelta(days=1)
    print(f"🔍 Baixando dados de {start_date.date()} até {end_date.date()}")

    df = yf.download('SAPR4.SA', start=start_date.strftime('%Y-%m-%d'), end=(data + timedelta(days=1)).strftime('%Y-%m-%d'))
    
    print(f"📊 Número de registros baixados: {len(df)}")

    if df.empty or len(df) < 60:
        raise ValueError("Não há dados suficientes para prever a data fornecida.")

    df = df[['Close']]
    df_scaled = scaler.transform(df)

    ultimos_60 = df_scaled[-60:]  # Últimos 60 dias
    X_input = np.reshape(ultimos_60, (1, 60, 1))  # reshape para LSTM

    previsao_normalizada = model.predict(X_input)
    previsao_real = scaler.inverse_transform(previsao_normalizada)
    
    return float(previsao_real[0][0])
