from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.routers.auth import  auth
from app.api.routers.users import users
from app.api.routers.predict import predict
import time
import boto3
from fastapi import Request

app = FastAPI(title="Previsão de Ações SAPR4")

app.include_router(predict)
app.include_router(users)
app.include_router(auth)

@app.get('/')
async def redirect_to_docs():
    return RedirectResponse(url="/docs", status_code=302)


@app.middleware("http")
async def log_latency_metric(request: Request, call_next):

    start_time = time.time()  

    response = await call_next(request)  

    process_time = time.time() - start_time  

    if request.url.path.startswith(predict.prefix):
        try:
            cloudwatch_client.put_metric_data(
                Namespace='API/Performance',  
                MetricData=[
                    {
                        'MetricName': 'Latency',  
                        'Dimensions': [
                            {
                                'Name': 'APIName',
                                'Value': 'PrevisaoAcoesSAPR4'
                            },
                        ],
                        'Unit': 'Seconds',      
                        'Value': process_time   
                    },
                ]
            )
        except Exception as e:
            print(f"Erro ao enviar métrica para o CloudWatch: {e}")

    return response

