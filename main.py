from fastapi import FastAPI
from routers.admins import admins_router
from routers.companies import companies_router
from routers.professionalas import professionals_router

app = FastAPI()
app.include_router(admins_router)
app.include_router(companies_router)
app.include_router(professionals_router)