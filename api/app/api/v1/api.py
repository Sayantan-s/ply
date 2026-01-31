# app/api/v1/api.py

from fastapi import APIRouter

from app.api.v1.endpoints import jdmatch

api_router = APIRouter()

# JD Match Router
api_router.include_router(jdmatch.router, tags=["JD Match"], prefix="/jdmatch")
