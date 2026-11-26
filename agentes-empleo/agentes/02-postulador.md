# Agente 2: Postulador (CV ATS adaptado + envío)

**Cuándo corre:** de lunes a viernes a las 07:37 y a las 14:37 (hora de Bogotá).
**Objetivo:** por cada oferta buena, preparar un CV en **formato ATS** y una **carta de presentación**, ambos
adaptados a la oferta. Si la oferta publica un correo, enviarlos. Si se postula por portal, dejarlos listos para
que David aplique en un minuto.
También hace el seguimiento de las postulaciones enviadas.

Lee primero `agentes/00-comun.md` y haz la preparación (incluye leer el perfil maestro).

## Límites (autorizados por David el 19-nov-2026)

- Máximo **8 correos de postulación por día** (suma de las dos ejecuciones) y **5 correos de seguimiento por día**.
- Un solo correo por oferta y nunca dos postulaciones a la misma empresa en 14 días, salvo que sean cargos distintos.
- Solo a direcciones publicadas en la oferta, o en la página oficial de "trabaje con nosotros" de la misma empresa.
- Envío automático: no se crean borradores, se envía directamente.

## Pasos

1. **Historial.** En `CONFIG.CARPETA_POSTULACIONES` lee el `registro_postulaciones_*` más reciente
   (si no existe, el historial está vacío). Cada entrada:
   ```json
   {"fecha": "AAAA-MM-DD HH:MM", "oferta_id": "", "empresa": "", "cargo": "", "ciudad": "", "url": "",
    "canal": "correo|portal", "correo_destino": "", "thread_id": "", "message_id": "",
    "cv_pdf_url": "", "cv_docx_url": "", "carta_pdf_url": "", "carta_docx_url": "", "puntaje": 0, "prioridad": "A|B",
    "estado": "enviada|pendiente_envio|lista_para_portal|aplicada_por_david|seguimiento_enviado|respondio|entrevista|descartada",
    "seguimiento_fecha": "", "notas": ""}
   ```
   Cuenta cuántos correos de postulación y de seguimiento lleva hoy.
   **Envíos pendientes:** las entradas con `estado: pendiente_envio` ya tienen CV y carta generados (se prepararon
   cuando el tope diario estaba lleno). Envíalas primero, dentro del tope, con el formato del paso 4 y los PDF de
   `cv_pdf_url` y `carta_pdf_url` (descárgalos con `download_file_content`); usa el asunto que indique `notas`.
   Después cambia el estado a `enviada` y mueve la captura correspondiente a "procesadas".

2. **Ofertas candidatas.** Lee los `ofertas_*.json` de `CONFIG.CARPETA_OFERTAS` de los últimos 3 días.
   Quédate con las de prioridad A y B que no estén en el historial. Antes de postular, vuelve a abrir la URL:
   si la oferta ya no existe o cerró, márcala como `descartada` con esa nota.

   **¿Ya se postuló David?** Antes de preparar el CV o enviar algo, verifica en Gmail que David no se
   haya postulado ya a esa oferta o a esa empresa:
   - Confirmaciones de los portales: `newer_than:90d (from:elempleo OR from:magneto365 OR from:computrabajo
     OR from:linkedin.com OR from:torre.ai) (<palabra clave del cargo> OR "<empresa>")`, buscando textos como
     "te postulaste", "aplicaste", "tu postulación", "tu hoja de vida fue enviada" o "application sent".
   - Correos que David envió a la empresa: `in:sent newer_than:60d (<dominio del correo de la oferta> OR "<empresa>")`.
   - Si la oferta en el portal muestra "Ya aplicaste" o "Postulado" (por ejemplo, la etiqueta
     `applied-offer-tag` visible en Computrabajo), también cuenta como postulada.
   Si ya se postuló, no hagas nada más con esa oferta: regístrala con `estado: aplicada_por_david` y la
   nota de dónde lo detectaste. Si la empresa es "Confidencial" y no hay forma de saberlo, sigue adelante.

   **Ofertas falsas:** descarta y avisa en el registro (`estado: descartada`, nota "posible estafa") las
   que piden pagos, entrevistas solo por chat o WhatsApp, o vienen de dominios desconocidos con mensajes
   genéricos ("buscamos asistentes, supervisores y gerentes", "vimos su currículum en la plataforma").

3. **CV adaptado (ATS) para cada candidata.** Orden: primero prioridad A, primero Costa Norte, primero canal correo.
   Por ejecución: hasta 6 por correo (respetando el tope diario) y hasta 6 por portal.
   - Copia `perfil_maestro.json → cv_base` en `/tmp/trabajo/cv_<id>.json` y adáptalo:
     - `titular`: el nombre del cargo de la oferta (si coincide con la experiencia real) más la especialidad.
       Ejemplo: "Gerente de Operaciones Logísticas | Transporte, Distribución y Comercio Exterior | 14 años".
     - `perfil`: de 4 a 6 líneas que respondan a los requisitos de la oferta usando sus mismas palabras
       clave, sin afirmar nada que no esté en el perfil maestro.
     - `logros_clave`: los 3 o 4 más relevantes para la oferta.
     - `competencias`: de 10 a 14, empezando por las que pide la oferta y David tiene.
     - `experiencia`: todos los cargos, en orden cronológico inverso. En los relevantes deja de 4 a 6 viñetas
       reordenadas por relevancia; en los menos relevantes, 2 o 3.
     - Fechas siempre MM/AAAA. No uses tablas, columnas, íconos ni imágenes (la plantilla ya es ATS).
     - **Según el área de la oferta**, prioriza estos hechos reales (de `cv_base` y de
       `perfil_maestro.detalle_otras_experiencias`):
       - Proyectos: PC Tronic primero en logros (7 proyectos, 95 % a tiempo, $900 MM, margen +18 %) y metodologías (SCRUM, Agile, híbrido).
       - Comercial / ventas / cuentas clave: Geotech (consecución de clientes, planes de servicio y venta), PC Tronic (relación B2B y
         postventa), Coca-Cola (CAV de preventa, P&G de concesionarios); agrega Arena 57 como experiencia con sus logros.
       - Servicio al cliente: Geotech (líder de servicio al cliente y PQR), Arena 57, OTIF de 99,9 % en Banasan.
       - Administrativo / gerencia general: presupuestos (USD 2 M/mes, $900 MM), gestión humana y procesos (GRAM administrativo),
         P&G en superávit, relación sindical.
       - Producción / mejora continua: formación en Lean Six Sigma, 5S, KPIs; −23 % paradas y −35 % quiebres en Banasan; asesoría de
         torre de control logística (solo en «otras experiencias»).
       Nunca afirmes cuotas de venta, certificaciones (PMP, ISO) ni cargos de planta que no estén en el perfil.
     - **Documentos por oferta (regla de David, 26-nov-2026):** a cada oferta van **siempre** el CV adaptado en español y la
       carta. Si confirmas que la oferta es **fuera de Colombia**, genera además el **CV adaptado en inglés** con los mismos
       parámetros (experiencia y resultados elegidos y ordenados según la oferta), con el nombre
       `CV_David_Ariza_<Empresa>_<Cargo>_EN.pdf` y `.docx`. Súbelo a `CONFIG.CARPETA_CV` y guarda sus enlaces en
       `cv_en_pdf_url` y `cv_en_docx_url` del registro.
     - **Oferta en inglés o CV en inglés:** pon `"idioma": "en"` en el JSON (los generadores cambian títulos y etiquetas) y redacta
       todo el contenido en inglés. Parte del `cv_base_en_*` más reciente de `CONFIG.CARPETA_SISTEMA`: es la
       traducción fiel del perfil maestro revisada con David. Adáptalo igual que el CV en español, sin agregar
       hechos que no estén en el perfil maestro.
     - **Oferta fuera de Colombia:** `informacion_adicional` = `perfil_maestro.permiso_trabajo.texto_cv` y
       `contacto.ubicacion` = "Barranquilla, Colombia · Disponible para reubicación internacional". En
       ofertas de Colombia no pongas esa sección.
   - Genera los dos formatos y verifica que el texto se lea en orden y quepa en 2 páginas:
     ```bash
     cd /tmp/trabajo
     node /tmp/ps/agentes-empleo/scripts/generar_cv.js cv_<id>.json "CV_David_Ariza_<Empresa>_<Cargo>.pdf"
     python3 /tmp/ps/agentes-empleo/scripts/generar_cv_docx.py cv_<id>.json "CV_David_Ariza_<Empresa>_<Cargo>.docx"
     pdftotext "CV_David_Ariza_<Empresa>_<Cargo>.pdf" - | head -30
     ```
     (Si falta `python-docx`: `pip install -q python-docx`.) Nombres de archivo sin tildes ni espacios.
   - Sube el PDF y el DOCX a `CONFIG.CARPETA_CV` con `create_file`, usando como `base64Content` una
     referencia de archivo `sha256:<hash>:<ruta absoluta>` (calcula el hash con `sha256sum`) y
     `disableConversionToGoogleType: true`. Guarda los enlaces `viewUrl`.

3b. **Carta de presentación personalizada (obligatoria en toda postulación).** Por cada oferta con CV adaptado,
   escribe una carta específica para ese puesto en `/tmp/trabajo/carta_<id>.json` (estructura en
   `ejemplos/carta_ejemplo.json`). No es una plantilla con el nombre cambiado: cada carta se redacta para la oferta.
   - **Encabezado:** `nombre`, `titulo_profesional` ("Ingeniero Industrial, Esp. en Logística Empresarial"),
     `contacto` (el mismo del CV), `lugar_fecha` ("Barranquilla, <d> de <mes> de <aaaa>"), `destinatario` (el
     nombre del reclutador si aparece en la oferta o publicación; si no, "Señores" / "Equipo de Selección" /
     empresa / ciudad; si la empresa es confidencial, "Equipo de Selección" y la ciudad), `referencia`
     ("Postulación al cargo de <cargo exacto de la oferta>").
   - **Cuerpo de 220 a 380 palabras, una página:**
     1. *Gancho* (2 o 3 líneas): el cargo, dónde vio la oferta y por qué ese reto en particular, citando algo
        concreto de la oferta (el sector, la región, el reto o el propósito que declara). No inventes datos de la
        empresa: usa solo lo que dice la oferta o información pública que hayas verificado.
     2. *Experiencia más relevante para el rol*: el cargo o la empresa del perfil que mejor responde a la oferta,
        con 2 o 3 cifras reales (las mismas del CV adaptado).
     3. `vinetas` (3): "Lo que aportaría a <Empresa>" — cada viñeta conecta un requisito de la oferta con un hecho
        real del perfil maestro, usando las palabras clave de la oferta.
     4. *Toque personal* (2 o 3 líneas): una conexión verdadera con el cargo, la región o el sector, y el estilo
        de liderazgo. Fuentes válidas: vive en Barranquilla y conoce la Costa Caribe; operó transporte en
        Magdalena y La Guajira; empezó su carrera en distribución de consumo masivo en Coca-Cola FEMSA; creó y
        dirigió un emprendimiento propio (Arena 57); lidera equipos grandes en operación 24/7; decide con datos
        (Power BI, SQL); mejora continua (formación en Lean Six Sigma; no está certificado). Nada de frases genéricas ("soy una
        persona proactiva y apasionada") ni de afirmaciones que no estén en el perfil maestro.
     5. *Cierre*: disponibilidad para trasladarse si el cargo no es en Barranquilla (fuera de Colombia, la frase del
        permiso de trabajo patrocinado), invitación a una entrevista y agradecimiento. Salario solo si la oferta
        lo pide, con la frase del paso 4.
   - Idioma: el de la oferta (`"idioma": "en"` si está en inglés). Tono formal, cercano y seguro; sin emojis.
   - Mismas reglas de veracidad que el CV (`00-comun.md`, sección 2): si la oferta pide algo que David no tiene,
     no lo menciones.
   - Genera los dos formatos y verifica que quede en una página:
     ```bash
     node /tmp/ps/agentes-empleo/scripts/generar_carta.js carta_<id>.json "Carta_David_Ariza_<Empresa>_<Cargo>.pdf"
     python3 /tmp/ps/agentes-empleo/scripts/generar_carta_docx.py carta_<id>.json "Carta_David_Ariza_<Empresa>_<Cargo>.docx"
     ```
   - Sube ambos a `CONFIG.CARPETA_CV` igual que el CV y guarda los enlaces en `carta_pdf_url` y `carta_docx_url`.
   - **CV pendientes con Energía Solar (desde el 26-nov-2026):** si hay entradas `lista_para_portal` de los últimos 10 días
     cuya oferta siga abierta y cuyo CV o carta muestre a Energía Solar como experiencia laboral o diga «Green Belt», regenera CV y carta con el
     perfil maestro vigente (y el CV en inglés si es fuera de Colombia). Máximo 6 por ejecución, primero las de prioridad A.
     Actualiza los enlaces en el registro.
   - **Cartas pendientes:** si hay entradas `lista_para_portal` de los últimos 10 días sin `carta_pdf_url` cuya
     oferta siga abierta, genérales la carta en esta ejecución (máximo 6, primero las de prioridad A) y
     actualiza la entrada en el registro.

4. **Envío por correo** (canal `correo`, dentro del tope):
   - Asunto: si la oferta pide un asunto, úsalo exactamente. Si no: `Postulación: <Cargo> - David Ariza López`.
   - Cuerpo en español, cordial y directo, de 120 a 170 palabras, sin emojis:
     saludo ("Respetado equipo de selección de <Empresa>:" o el nombre del reclutador si aparece) →
     a qué cargo se postula y dónde vio la oferta → 3 viñetas con hechos del perfil que responden a los
     requisitos → disponibilidad para trasladarse si la vacante no está en Barranquilla (si es fuera de
     Colombia: "Soy de nacionalidad colombiana y tengo plena disponibilidad para trasladarme a <ciudad>; para
     ello requeriría el patrocinio del permiso de trabajo") → invitación a conversar → firma: David Ariza López, Ingeniero Industrial, Esp. en Logística Empresarial,
     +57 300 274 0653, linkedin.com/in/davidarizalpz.
     Si la oferta pide aspiración salarial, escribe: "Mi aspiración salarial es superior a $9.000.000
     mensuales, negociable según el paquete integral." Si no la pide, no menciones salario.
   - El cuerpo del correo es una nota breve; la carta adjunta es la que desarrolla la motivación. Antes de la
     invitación a conversar, menciona: "Adjunto mi hoja de vida y una carta de presentación para el cargo."
   - Envía con `send_message`: `to` = el correo de la oferta, `body` en texto plano y `htmlBody` con el
     mismo contenido en HTML simple, y en `attachments` **dos PDF**: el CV (`filename:
     CV_David_Ariza_<Empresa>.pdf`) y la carta (`filename: Carta_presentacion_David_Ariza_<Empresa>.pdf`), con
     referencia `sha256:<hash>:<ruta>` y `mimeType: application/pdf`. Si la oferta es fuera de Colombia, adjunta
     **tres PDF**: también el CV en inglés (`filename: CV_David_Ariza_<Empresa>_EN.pdf`), y en el correo di «Adjunto mi hoja de vida en español y en inglés y una carta de presentación para el cargo.». Nunca adjuntes los .docx.
   - Ponle la etiqueta `CONFIG.ETIQUETA_POSTULACIONES` al mensaje enviado (`label_message`).
   - Registra la entrada con `estado: enviada`, `thread_id` y `message_id`.

5. **Canal portal:** registra la entrada con `estado: lista_para_portal`, la URL de la oferta y los
   enlaces del CV y de la carta. El Resumen matutino se los presenta a David para que aplique (en el campo
   "carta de presentación" o "mensaje al reclutador" del portal puede pegar el texto de la carta o subir el PDF).

5b. **Vacantes de publicaciones de LinkedIn (capturas que sube David).** En `CONFIG.CARPETA_RAIZ` está la
   carpeta "Vacantes LinkedIn (sube aquí las capturas)" (búscala por título). Revisa los archivos que haya
   dentro (imágenes, PDF o texto), excepto la subcarpeta "procesadas":
   - Lee cada uno: `read_file_content` (extrae el texto de imágenes y PDF). Si no basta, descárgalo con
     `download_file_content` y mira la imagen con la herramienta Read. Extrae: quién publica (persona y
     empresa), cargo, ciudad, requisitos y funciones declarados en la publicación, salario y contrato si
     los dicen, el **correo** para enviar la hoja de vida, el asunto que pidan y la fecha de publicación.
   - Valida: cualquier país sirve (fuera de Colombia aplica la regla de permiso de trabajo de `00-comun.md`
     y la conversión de salario); que el cargo encaje con el perfil (puntaje de `00-comun.md`; si salario
     o contrato no se dicen, se acepta). Si David subió la captura, asume que le interesa aunque el salario
     convertido quede por debajo de la meta, pero anótalo en el registro y en el resumen; que no sea sospechosa y que David no haya escrito ya a
     ese correo o empresa (Gmail `in:sent`). Si no hay correo en la publicación, regístrala como
     `lista_para_portal` con la nota "publicación sin correo" para que David responda por LinkedIn.
   - Prepara el CV ATS y la carta de presentación adaptados a lo que dice la publicación (mismas reglas de los
     pasos 3 y 3b; en la carta, dirígete a quien publicó si se sabe su nombre) y envía el correo
     con el formato del paso 4, con estas particularidades: menciona que viste la publicación en LinkedIn
     (y de quién, si se sabe); responde punto por punto a los requisitos y declaraciones de la publicación
     con hechos reales del perfil maestro; usa el asunto que pida la publicación, si pide uno. Cuenta para el
     tope diario de 8 correos.
   - Registra la entrada con `canal: correo_linkedin_post`, el ID del archivo de la captura en `notas`, y
     mueve el archivo a la subcarpeta "procesadas" (créala si no existe) con `update_file` (`parentId`).

6. **Seguimiento** (máximo 5 por día). En cada entrada con `estado: enviada` y 5 o más días hábiles desde
   el envío, sin seguimiento previo:
   - Lee el hilo con `get_thread`. Si alguien de la empresa respondió, cambia el estado a `respondio`
     (o a `entrevista` si proponen una cita) y **no respondas**: eso lo decide David.
   - Si no hay respuesta, responde en el mismo hilo (`replyThreadId`) con 2 a 4 líneas: reitera el interés
     en el cargo, ofrece ampliar información y da las gracias. Estado: `seguimiento_enviado`.
   - Revisa también si hay respuestas a las entradas `seguimiento_enviado`.

7. **Guardar el historial:** sube `registro_postulaciones_AAAA-MM-DD_HHMM.json` con el historial
   **completo** (lo anterior más lo nuevo y los cambios de estado) a `CONFIG.CARPETA_POSTULACIONES`
   (`text/plain`, sin conversión). Nunca borres entradas.

8. **Cierre:** un párrafo con los correos enviados (empresa y cargo), los CV y cartas listos para portal, las
   cartas pendientes que generaste, los seguimientos y las respuestas recibidas.
