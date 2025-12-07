from config import db, client

def get_db():
    """
    FastAPI dependency to get the MongoDB database instance.
    """
    return db

def get_client():
    """
    FastAPI dependency to get the MongoDB client instance for transactions.
    """
    return client