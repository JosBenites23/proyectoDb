from fastapi import FastAPI
from config import DATABASE_URL, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from routers import user, jwt_auth, protected, obtain_news, create_news, vanish_news, create_link, vanish_link, Birthday, Team, company, Dep, logout
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from client import engine, Base

app = FastAPI() 

app.mount("/images", StaticFiles(directory="C:/inetpub/wwwroot/intraner10/dist/images/"), name="images")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://9.0.1.247:8090"],  # origen de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # puedes restringir si quieres
    allow_headers=["*"],  # puedes restringir si quieres
)


app.include_router(user.router)
app.include_router(jwt_auth.router)
app.include_router(protected.router)
app.include_router(obtain_news.router)
app.include_router(create_news.router)
app.include_router(vanish_news.router)
app.include_router(create_link.router)
app.include_router(vanish_link.router)
app.include_router(Birthday.router)
app.include_router(Team.router)
app.include_router(company.router)
app.include_router(Dep.router)
app.include_router(logout.router)

Base.metadata.create_all(bind=engine)



@app.get("/")
async def root():
    return {"message": DATABASE_URL}


### para correr el servidor
# uvicorn main:app --reload --host no olvidar activar entorno virtual