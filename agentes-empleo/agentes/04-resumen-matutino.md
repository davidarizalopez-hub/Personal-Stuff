# Agente 4: Resumen matutino

**Cuándo corre:** todos los días a las 06:41 (hora de Bogotá).
**Objetivo:** que David abra un solo correo cada mañana y sepa qué pasó, qué ofertas seguir de cerca y
qué hacer hoy, en menos de 3 minutos de lectura.

Lee primero `agentes/00-comun.md` y haz la preparación.

## Datos que reúne

1. **Postulaciones:** el `registro_postulaciones_*` más reciente de `CONFIG.CARPETA_POSTULACIONES`.
   Calcula: correos de postulación enviados en las últimas 24 horas y en total, seguimientos enviados, CV
   listos para portal que aún no se han aplicado, respuestas y entrevistas.
2. **Correo de David (Gmail):** busca respuestas reales de empresas en las últimas 48 horas:
   - `label:"Agente Empleo/Postulaciones" newer_than:2d` y abre con `get_thread` los hilos con más de un mensaje.
   - `newer_than:2d -from:me (entrevista OR "proceso de selección" OR postulación OR "hoja de vida" OR vacante OR candidato)`.
   - Notificaciones de portales: `newer_than:2d (from:computrabajo OR from:elempleo OR from:magneto365 OR from:linkedin OR from:torre)`
     con mensajes como "tu hoja de vida fue vista", "una empresa vio tu perfil" o "avanzaste en el proceso".
   - **Postulaciones que David hizo por su cuenta:** confirmaciones de los portales ("te postulaste",
     "aplicaste", "tu postulación fue enviada", "application sent"). Cruza cada una con el registro: si
     corresponde a una oferta `lista_para_portal`, márcala `aplicada_por_david`; si no estaba registrada,
     agrégala con ese estado. Así ningún agente vuelve a postular a la misma oferta.
   - **Posibles estafas:** correos que ofrecen entrevistas o empleo desde dominios desconocidos, con textos
     genéricos o que piden pagos o datos sensibles. Adviértelo en "Lo urgente hoy" para que David no responda.
   No respondas ningún correo: solo resume e indica la acción sugerida.
3. **Ofertas:** los `ofertas_*.json` de las últimas 24 horas (nuevas) y de los últimos 10 días (seguimiento).
4. **LinkedIn:** el documento `LinkedIn_<hoy>` (o el más reciente) de `CONFIG.CARPETA_LINKEDIN`.
5. **Empleo remoto:** el `ofertas_remoto_*` más reciente de `CONFIG.CARPETA_OFERTAS` y el `cuentas_remoto_*` más
   reciente de `CONFIG.CARPETA_SISTEMA`.
6. **Marca personal:** con `getScheduledPosts` de la marca `CONFIG.METRICOOL_MARCA` (zona America/Bogota), las
   publicaciones de hoy y de mañana. Las que siguen con `draft: true` no se publican sin el OK de David.

## Ofertas destacadas para seguimiento constante (máximo 7)

Elige las de mejor puntaje, con este orden de preferencia: hubo respuesta o entrevista, prioridad A en la
Costa Norte, salario publicado que cumple y postulación hace 3 días o más. Para cada una: cargo, empresa,
ciudad, salario, estado, días desde la postulación y la **siguiente acción concreta** (por ejemplo:
"llamar al conmutador y preguntar por el proceso", "buscar en LinkedIn a la gerente de gestión humana y
escribirle", "aplicar hoy en el portal con el CV adaptado", "preparar entrevista: repasar el caso de fletes de Banasan").

## Formato del correo

- `to`: `CONFIG.EMAIL_DAVID`. Asunto:
  `☀️ Búsqueda de empleo · <día> <fecha> · <N> enviados · <M> ofertas nuevas · <K> respuestas`
- `htmlBody` limpio y legible en el celular (una sola columna, títulos cortos, tablas pequeñas), y `body`
  con la versión en texto plano. Secciones en este orden:
  1. **Lo urgente hoy** (solo si hay): respuestas de empresas, entrevistas y ofertas prioritarias que vencen.
  2. **Números del día:** correos enviados (24 horas y en total), CV listos para portal, ofertas nuevas
     revisadas y válidas, respuestas, y días que faltan para el 1 de diciembre.
  3. **Ofertas destacadas para seguimiento** (la lista de arriba).
  4. **Aplica hoy en portales:** las postulaciones `lista_para_portal` (máximo 6, primero las de prioridad A),
     numeradas. Cada una con un enlace **"Ver oferta y postularme"** a la URL de la oferta (no al CV) y los
     nombres del CV y de la carta de presentación que debe adjuntar (y del CV en inglés si la oferta es fuera de Colombia). **Adjunta al correo los PDF del CV y de la
     carta** de esas ofertas (descárgalos de `CONFIG.CARPETA_CV` con `download_file_content` usando los enlaces
     `cv_pdf_url`, `carta_pdf_url` y, si existe, `cv_en_pdf_url` del registro, y adjúntalos con referencia `sha256:<hash>:<ruta>`), para
     que David los tenga a mano al postularse desde el celular. Indica: "Al aplicar, sube el CV adaptado y la
     carta (o pega su texto en el campo de presentación del portal) y responde a este correo con 'aplicada' y
     los números (por ejemplo, 'aplicada 1, 2, 5')". Si una entrada aún no tiene carta, dilo ("carta en
     preparación"). En cada
     ejecución busca en Gmail las respuestas de David que digan `aplicada` (`from:me aplicada newer_than:7d`),
     abre el hilo con `get_thread` para saber a qué oferta corresponde cada número del correo original, y
     actualiza esas entradas a `aplicada_por_david` en un nuevo `registro_postulaciones_*`.
     Recuérdale también la carpeta "Vacantes LinkedIn (sube aquí las capturas)" del Drive, y cuántas capturas
     procesó el Postulador desde el último resumen.
  5. **LinkedIn hoy (15 minutos):** la mejora del perfil del día (resumida), la acción de Premium del día,
     cuántas invitaciones enviar con el enlace al documento del día, y los comentarios sugeridos. Si hoy o
     mañana hay una publicación en Metricool que sigue como borrador, ponla primero: tema, hora y enlace
     «Abrir en Metricool para aprobarla». Sin su OK no se publica.
  6. **Empleo remoto:**
     - Las ofertas remotas nuevas de prioridad A y B, con su elegibilidad (Colombia o LATAM) y su tipo de
       contrato (empleado o contractor).
     - **Cuentas para crear hoy:** las 2 de `proximas` en `cuentas_remoto`, con el enlace y los pasos cortos
       (qué llenar del perfil y qué alertas configurar).
     - Pide a David que responda «cuenta creada <plataforma>» cuando la cree. Busca esas respuestas
       (`from:me "cuenta creada" newer_than:7d`) y anótalas en un nuevo `cuentas_remoto_*`.
  7. **Qué corregir del perfil de LinkedIn** (de 3 a 5 puntos priorizados, acumulando lo pendiente).
  8. **Pendientes de David:** lo que solo él puede resolver (datos del CV por confirmar en
     `_pendientes_de_confirmar`, exportar el PDF de LinkedIn, cifras de impacto que faltan).
- Envíalo con `send_message` y ponle la etiqueta `CONFIG.ETIQUETA_RESUMEN`.
- Si una ejecución de otro agente no dejó su archivo (por ejemplo, no hay `ofertas_*` de las últimas
  24 horas), dilo en el resumen como "⚠️ El buscador no corrió ayer" para que se pueda revisar.

## Cierre

Termina con 2 líneas: lo más importante del día para David.
