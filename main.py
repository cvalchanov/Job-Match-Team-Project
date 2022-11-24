from fastapi import FastAPI
from routers.admins import admins_router
from routers.companies import companies_router
from routers.professionals import professionals_router
from routers.job_ads import job_ads_router
from routers.skills import skills_router
from routers.approvals import approvals_router
from routers.professional_ads import professional_ads_router, my_professional_ads_router
from routers.search import search_router
from routers.match_requests import match_router

app = FastAPI()
app.include_router(admins_router)
app.include_router(companies_router)
app.include_router(professionals_router)
app.include_router(job_ads_router)
app.include_router(skills_router)
app.include_router(approvals_router)
app.include_router(professional_ads_router)
app.include_router(my_professional_ads_router)
app.include_router(search_router)
app.include_router(match_router)
