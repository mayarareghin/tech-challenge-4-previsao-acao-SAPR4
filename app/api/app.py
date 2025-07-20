from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.routers.auth import  auth
from app.api.routers.users import users
from app.api.routers.predict import predict

app = FastAPI(title="Previsão de Ações SAPR4")

app.include_router(predict)
app.include_router(users)
app.include_router(auth)

@app.get('/')
async def redirect_to_docs():
    return RedirectResponse(url="/docs", status_code=302)