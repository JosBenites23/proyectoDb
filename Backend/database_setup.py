from sqlalchemy import text

# Ya no necesitamos event, DDL, o el modelo Noticia aquí

def initialize_triggers(engine):
    """
    Ejecuta los comandos DDL para crear los triggers de auditoría si no existen.
    """
    
    trigger_sqls = [
        """
        CREATE TRIGGER IF NOT EXISTS log_news_insert
        AFTER INSERT ON news
        FOR EACH ROW
        BEGIN
            INSERT INTO logsdb (user_id, action, table_name, record_id, timestamp)
            VALUES (NEW.autor_id, 'CREATE', 'news', NEW.id, CURRENT_TIMESTAMP);
        END;
        """,
        """
        CREATE TRIGGER IF NOT EXISTS log_news_update
        AFTER UPDATE ON news
        FOR EACH ROW
        BEGIN
            INSERT INTO logsdb (user_id, action, table_name, record_id, timestamp)
            VALUES (NEW.autor_id, 'UPDATE', 'news', NEW.id, CURRENT_TIMESTAMP);
        END;
        """,
        """
        CREATE TRIGGER IF NOT EXISTS log_news_delete
        AFTER DELETE ON news
        FOR EACH ROW
        BEGIN
            INSERT INTO logsdb (user_id, action, table_name, record_id, timestamp)
            VALUES (OLD.autor_id, 'DELETE', 'news', OLD.id, CURRENT_TIMESTAMP);
        END;
        """
    ]

    with engine.connect() as connection:
        for sql in trigger_sqls:
            connection.execute(text(sql))
    
    print("Verificación de triggers completada.")