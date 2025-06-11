
import os
from dotenv import load_dotenv

# Carga el .env desde la raíz del proyecto
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

# Variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
URLBACK = os.getenv("URLBACK", "http://localhost")
URLFRONT = os.getenv("URLFRONT", "http://localhost")

print(URLBACK)
print(URLFRONT)
