// =================================================================
// ARCHIVO SIMULADO: atlas_functions.js
// Este archivo contiene ejemplos de cómo las lógicas de SQL de
// database_setup.py se traducirían a Funciones y Triggers de MongoDB Atlas.
// Este código se escribiría en la UI de Atlas, no en el proyecto.
// =================================================================

// -----------------------------------------------------------------
// 1. TRIGGERS DE LOG (Traducción de los triggers de `logsdb`)
// -----------------------------------------------------------------
// En Atlas, crearías un Trigger para cada colección y evento.
// Por ejemplo, para la colección "news":
// - Nombre del Trigger: logNewsInsert
// - Colección: news
// - Operación: Insert
// - Función a ejecutar: logOperation

// - Nombre del Trigger: logNewsUpdate
// - Colección: news
// - Operación: Update
// - Función a ejecutar: logOperation

// - Nombre del Trigger: logNewsDelete
// - Colección: news
// - Operación: Delete
// - Función a ejecutar: logOperation

// Y lo mismo para la colección "dep". Todas llamarían a esta función genérica:

/**
 * Función de Atlas que se ejecuta por un Trigger para registrar una operación.
 * @param {object} changeEvent - El objeto de evento que pasa el Trigger.
 */
exports.logOperation = function(changeEvent) {
  const logsCollection = context.services.get("mongodb-atlas").db("mydatabase").collection("logs");
  
  const { operationType, ns, fullDocument, documentKey, updateDescription } = changeEvent;
  const { db, coll } = ns;

  let autor_id = null;
  // En insert/update, el autor está en el documento completo.
  if (fullDocument) {
    autor_id = fullDocument.autor_id;
  } 
  // Nota: Para 'delete', el documento completo no siempre está disponible.
  // Una estrategia común es no eliminar documentos, sino marcarlos como "deleted: true",
  // o asegurarse de que el autor_id se pase de alguna manera en el contexto de la operación.
  // Por simplicidad, aquí lo dejamos como null si no se encuentra.

  const logDoc = {
    user_id: autor_id,
    action: operationType.toUpperCase(), // 'INSERT', 'UPDATE', 'DELETE'
    table_name: coll, // nombre de la colección
    record_id: documentKey._id, // el _id del documento afectado
    timestamp: new Date(),
    update_details: updateDescription || null // Opcional: para ver qué cambió
  };

  return logsCollection.insertOne(logDoc);
};


// -----------------------------------------------------------------
// 2. FUNCIONES (Traducción de Stored Procedures)
// -----------------------------------------------------------------

/**
 * Función de Atlas para crear una noticia.
 * Equivalente a `sp_create_news`.
 * La limpieza de datos (TRIM) se haría aquí o en el cliente.
 * @param {object} newsData - Datos de la noticia: { titulo, descripcion, ... }
 */
exports.createNews = function(newsData) {
  const newsCollection = context.services.get("mongodb-atlas").db("mydatabase").collection("news");
  
  // Limpieza de datos (equivalente a fn_clean_input)
  const cleanedTitle = newsData.titulo.trim();
  const cleanedDesc = newsData.descripcion.trim();
  
  const doc = {
    titulo: cleanedTitle,
    descripcion: cleanedDesc,
    tipo_contenido: newsData.tipo_contenido,
    contenido: newsData.contenido,
    autor_id: newsData.autor_id,
    fecha_creacion: new Date()
  };

  return newsCollection.insertOne(doc);
};


// -----------------------------------------------------------------
// 3. VISTAS (Traducción de `v_user_activity_log` y `v_news_with_author`)
// -----------------------------------------------------------------
// En Atlas, irías a "Views", seleccionarías una colección base (e.g., `logs`)
// y construirías un "Aggregation Pipeline".

// --- Pipeline para v_news_with_author ---
// Colección Base: news
// Pipeline:
[
  {
    '$lookup': {
      'from': 'users', 
      'localField': 'autor_id', 
      'foreignField': '_id', 
      'as': 'autor_details'
    }
  }, {
    '$unwind': { // $lookup devuelve un array, $unwind lo "desenrolla"
      'path': '$autor_details',
      'preserveNullAndEmptyArrays': true // como un LEFT JOIN
    }
  }, {
    '$project': { // Selecciona y renombra los campos finales
      '_id': 1, 
      'titulo': 1, 
      'descripcion': 1, 
      'tipo_contenido': 1, 
      'contenido': 1, 
      'fecha_creacion': 1, 
      'autor_id': 1, 
      'autor_username': '$autor_details.username', 
      'autor_name': '$autor_details.name'
    }
  }
]

// --- Pipeline para v_user_activity_log ---
// Colección Base: logs
// Pipeline:
[
    // Similar al anterior, usando $lookup para unir 'logs' con 'users'
]
