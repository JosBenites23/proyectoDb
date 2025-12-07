from datetime import datetime
from typing import Optional

from dataBase.modelLog_mongo import Log

async def create_log_entry(
    db, 
    user_id: Optional[str],
    action: str,
    table_name: str,
    record_id: Optional[str] = None
):
    """
    Creates and inserts a log entry into the 'logs' collection.
    """
    try:
        # Pydantic model will handle the default timestamp
        log_entry = Log(
            user_id=user_id,
            action=action,
            table_name=table_name,
            record_id=record_id
        )
        await db["logs"].insert_one(log_entry.dict(by_alias=True))
        print(f"--- ACTION LOGGED: User '{user_id}' performed '{action}' on table '{table_name}' ---")
    except Exception as e:
        # We print the error but don't re-raise it, as logging failure
        # should not crash the main application endpoint.
        print(f"!!! FAILED TO CREATE LOG ENTRY: {e} !!!")
