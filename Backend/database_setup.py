from sqlalchemy import text

def initialize_triggers(engine):
    """
    Ejecuta los comandos DDL para crear los triggers y otros objetos de BD si no existen.
    """
    
    setup_sqls = [
        # --- Triggers para la tabla 'news' ---
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
        """,
        # --- Triggers para la tabla 'dep' ---
        """
        CREATE TRIGGER IF NOT EXISTS log_dep_insert
        AFTER INSERT ON dep
        FOR EACH ROW
        BEGIN
            INSERT INTO logsdb (user_id, action, table_name, record_id, timestamp)
            VALUES (NEW.autor_id, 'CREATE', 'dep', NEW.id, CURRENT_TIMESTAMP);
        END;
        """,
        """
        CREATE TRIGGER IF NOT EXISTS log_dep_update
        AFTER UPDATE ON dep
        FOR EACH ROW
        BEGIN
            INSERT INTO logsdb (user_id, action, table_name, record_id, timestamp)
            VALUES (NEW.autor_id, 'UPDATE', 'dep', NEW.id, CURRENT_TIMESTAMP);
        END;
        """,
        """
        CREATE TRIGGER IF NOT EXISTS log_dep_delete
        AFTER DELETE ON dep
        FOR EACH ROW
        BEGIN
            INSERT INTO logsdb (user_id, action, table_name, record_id, timestamp)
            VALUES (OLD.autor_id, 'DELETE', 'dep', OLD.id, CURRENT_TIMESTAMP);
        END;
        """,
        # --- Stored Procedure para crear Dep y Link atómicamente ---
        """
        CREATE PROCEDURE IF NOT EXISTS sp_create_department_with_link(
            IN p_titulo VARCHAR(500),
            IN p_slug VARCHAR(500),
            IN p_descripcion TEXT,
            IN p_imagen VARCHAR(500),
            IN p_autor_id INT,
            IN p_titulo_link VARCHAR(500),
            IN p_url_link VARCHAR(500)
        )
        BEGIN
            DECLARE new_dep_id INT;
            START TRANSACTION;
            INSERT INTO dep (titulo, slug, descripcion, imagen, autor_id, fecha_creacion)
            VALUES (p_titulo, p_slug, p_descripcion, p_imagen, p_autor_id, NOW());
            SET new_dep_id = LAST_INSERT_ID();
            INSERT INTO linkdep (titulo_link, url, dep_id, fecha_creacion)
            VALUES (p_titulo_link, p_url_link, new_dep_id, NOW());
            COMMIT;
        END
        """
    ]

    with engine.connect() as connection:
        for sql in setup_sqls:
            if sql.strip():
                connection.execute(text(sql))
    
    print("Verificación de Triggers y Stored Procedures completada.")