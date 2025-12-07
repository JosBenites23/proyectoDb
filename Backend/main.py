import os
from fastapi import FastAPI
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# --- Routers Originales (SQLAlchemy) - Comentados ---
# from .routers import user, jwt_auth, protected, obtain_news, create_news, vanish_news, create_link, vanish_link, Birthday, Team, company, Dep, logout, About, stats

# --- Routers Nuevos (MongoDB) ---
from routers import (
    user, 
    jwt_auth_mongo, 
    protected, # No necesita cambios
    obtain_news_mongo, 
    create_news_mongo, 
    vanish_news_mongo, 
    create_link_mongo, 
    vanish_link_mongo, 
    Birthday_mongo, 
    Team_mongo, 
    company_mongo, 
    Dep_mongo, 
    logout, # No necesita cambios
    About_mongo, 
    stats_mongo
)

app = FastAPI()

# Construct an absolute path for the 'uploads' directory
uploads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"], # Hardcoded for debugging CORS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Inclusión de Routers Originales - Comentados ---
# app.include_router(user.router)
# app.include_router(jwt_auth.router)
# app.include_router(protected.router)
# app.include_router(obtain_news.router)
# app.include_router(create_news.router)
# app.include_router(vanish_news.router)
# app.include_router(create_link.router)
# app.include_router(vanish_link.router)
# app.include_router(Birthday.router)
# app.include_router(Team.router)
# app.include_router(company.router)
# app.include_router(Dep.router)
# app.include_router(logout.router)
# app.include_router(About.router)
# app.include_router(stats.router)

# --- Inclusión de Routers Nuevos (MongoDB) ---
app.include_router(user.router)
app.include_router(jwt_auth_mongo.router)
app.include_router(protected.router)
app.include_router(obtain_news_mongo.router)
app.include_router(create_news_mongo.router)
app.include_router(vanish_news_mongo.router)
app.include_router(create_link_mongo.router)
app.include_router(vanish_link_mongo.router)
app.include_router(Birthday_mongo.router)
app.include_router(Team_mongo.router)
app.include_router(company_mongo.router)
app.include_router(Dep_mongo.router)
app.include_router(logout.router)
app.include_router(About_mongo.router)
app.include_router(stats_mongo.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Intranet API - MongoDB Version"}
