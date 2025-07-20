from http import HTTPStatus
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.database import get_session
from app.db.models import User
from app.api.schemas import PrevisaoRequest
from fastapi import FastAPI, HTTPException, Query
from datetime import datetime
from app.services.prediction import prever_preco
from app.api.dependencies.security import (
    get_current_user,
    get_password_hash,
)

predict = APIRouter(prefix='/prever', tags=['prever'])

@predict.get("/")
def prever(
    data: str = Query(..., example="2025-07-20"),
    user: User = Depends(get_current_user)
):
    try:
        data_convertida = datetime.strptime(data, "%Y-%m-%d")
        preco_previsto = prever_preco(data_convertida)
        return {
            "data": data,
            "preco_previsto": round(preco_previsto, 2)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
