from datetime import datetime, timedelta
import yfinance as yf
import numpy as np
from keras.models import load_model
import joblib 

MODELO_PATH = "app/ml_models/modelo_completo_lstm_sapr4.h5"
SCALER_PATH = "app/ml_models/scaler_sapr4.gz"

model = load_model(MODELO_PATH)
scaler = joblib.load(SCALER_PATH)

def prever_preco(data: datetime) -> float:
    start_date = data - timedelta(days=360)
    end_date = data + timedelta(days=1)
    
    df = yf.download('SAPR4.SA', start=start_date.strftime('%Y-%m-%d'), end=(data + timedelta(days=1)).strftime('%Y-%m-%d'))
    
    if df.empty or len(df) < 60:
        raise ValueError("Não há dados suficientes para prever a data fornecida.")

    df = df[['Close']]
    df_scaled = scaler.transform(df)

    ultimos_60 = df_scaled[-60:]
    X_input = np.reshape(ultimos_60, (1, 60, 1)) 

    previsao_normalizada = model.predict(X_input)
    previsao_real = scaler.inverse_transform(previsao_normalizada)
    
    return float(previsao_real[0][0])
