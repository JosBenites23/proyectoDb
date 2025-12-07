import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient # Cliente asíncrono

# Carga el .env desde la raíz del proyecto
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

# Variables de entorno
MONGO_DATABASE_URL = os.getenv("MONGO_DATABASE_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "mydatabase")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
URLBACK = os.getenv("URLBACK", "http://localhost")
URLFRONT = os.getenv("URLFRONT", "http://localhost")
PUBLIC_BACKEND_URL = os.getenv("PUBLIC_BACKEND_URL", "http://localhost:8000")

# Configuración de MongoDB Asíncrona
client = AsyncIOMotorClient(MONGO_DATABASE_URL)
db = client[MONGO_DB_NAME]