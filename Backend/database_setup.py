from sqlalchemy import text

def initialize_functions_sql(engine):
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
        """,
        # --- Función para limpiar texto de entrada ---
        """
        CREATE FUNCTION IF NOT EXISTS fn_clean_input(
            p_input TEXT
        )
        RETURNS TEXT
        DETERMINISTIC
        BEGIN
            RETURN TRIM(p_input);
        END;
        """,
        # --- Stored Procedure para crear una Noticia ---
        """
        CREATE PROCEDURE IF NOT EXISTS sp_create_news(
            IN p_titulo VARCHAR(500),
            IN p_descripcion TEXT,
            IN p_tipo_contenido VARCHAR(50),
            IN p_contenido_url VARCHAR(2083),
            IN p_autor_id INT
        )
        BEGIN
            START TRANSACTION;

            INSERT INTO news (titulo, descripcion, tipo_contenido, contenido, autor_id, fecha_creacion)
            VALUES (
                fn_clean_input(p_titulo),
                fn_clean_input(p_descripcion),
                p_tipo_contenido,
                p_contenido_url,
                p_autor_id,
                NOW()
            );

            COMMIT;
        END;
        """,
        # --- Vistas ---        
        """
        CREATE OR REPLACE VIEW v_user_activity_log AS
        SELECT
            l.id AS log_id,
            u.username,
            u.name AS user_name,
            l.action,
            l.table_name,
            l.record_id,
            l.timestamp
        FROM
            logsdb l
        JOIN
            users u ON l.user_id = u.id;
        """,
        """
        CREATE OR REPLACE VIEW v_news_with_author AS
        SELECT
            n.id,
            n.titulo,
            n.descripcion,
            n.tipo_contenido,
            n.contenido,
            n.fecha_creacion,
            n.autor_id,
            u.username AS autor_username,
            u.name AS autor_name
        FROM
            news n
        JOIN
            users u ON n.autor_id = u.id;
        """
    ]

    with engine.connect() as connection:
        for sql in setup_sqls:
            if sql.strip():
                connection.execute(text(sql))
    
    print("Verificación de Triggers y Stored Procedures completada.")