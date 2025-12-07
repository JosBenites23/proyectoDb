from fastapi import APIRouter, Depends
from typing import List
from client_mongo import get_db
from dataBase.schemaStats_mongo import UserNewsStat

router = APIRouter(prefix="/stats", tags=["Estadísticas"])

@router.get("/news_per_user", response_model=List[UserNewsStat])
async def get_news_stats_per_user(db=Depends(get_db)):
    """
    Devuelve una lista de usuarios y la cantidad de noticias que cada uno ha publicado.
    Demuestra el uso de $lookup, $group y $sort en un Aggregation Pipeline.
    """
    pipeline = [
        {
            # Paso 1: Unir 'users' con 'news' (como un JOIN)
            '$lookup': {
                'from': 'news',           # La colección con la que unir
                'localField': '_id',      # El campo de 'users'
                'foreignField': 'autor_id', # El campo de 'news'
                'as': 'user_news'         # El array resultante
            }
        },
        {
            # Paso 2: Agrupar por usuario y contar las noticias
            '$group': {
                '_id': {                  # El identificador del grupo
                    'username': '$username',
                    'name': '$name'
                },
                'news_count': { '$sum': { '$size': '$user_news' } } # Contar elementos en el array
            }
        },
        {
            # Paso 3: Reformatear el resultado para que coincida con el schema
            '$project': {
                '_id': 0, # No incluir el _id compuesto
                'username': '$_id.username',
                'name': '$_id.name',
                'news_count': 1
            }
        },
        {
            # Paso 4: Ordenar por la cantidad de noticias
            '$sort': {
                'news_count': -1
            }
        }
    ]

    # La colección base para la agregación es 'users'
    stats_cursor = db["users"].aggregate(pipeline)
    return await stats_cursor.to_list(length=None)
