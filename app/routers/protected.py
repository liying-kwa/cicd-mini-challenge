from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from app.api import api
from dotenv import load_dotenv
import os

load_dotenv()
router = APIRouter()
api_key_header = APIKeyHeader(name="X-API-Key")
API_KEY = os.getenv("API_KEY")

assert API_KEY is not None, "API_KEY must be set in the environment"


@router.get("/secret")
def protected(api_key: Optional[str] = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid API key")
    secret = api.print_secret()
    return {"msg": secret.decode("utf-8")}
