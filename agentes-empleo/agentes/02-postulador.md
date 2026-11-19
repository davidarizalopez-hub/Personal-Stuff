# Agente 2: Postulador (CV ATS adaptado + envío)

**Cuándo corre:** de lunes a viernes a las 07:37 y a las 14:37 (hora de Bogotá).
**Objetivo:** por cada oferta buena, preparar un CV en **formato ATS** adaptado a la oferta. Si la oferta
publica un correo, enviarlo. Si se postula por portal, dejar el CV listo para que David aplique en un minuto.
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
    "cv_pdf_url": "", "cv_docx_url": "", "puntaje": 0, "prioridad": "A|B",
    "estado": "enviada|lista_para_portal|aplicada_por_david|seguimiento_enviado|respondio|entrevista|descartada",
    "seguimiento_fecha": "", "notas": ""}
   ```
   Cuenta cuántos correos de postulación y de seguimiento lleva hoy.

2. **Ofertas candidatas.** Lee los `ofertas_*.json` de `CONFIG.CARPETA_OFERTAS` de los últimos 3 días.
   Quédate con las de prioridad A y B que no estén en el historial. Antes de postular, vuelve a abrir la URL:
   si la oferta ya no existe o cerró, márcala como `descartada` con esa nota.

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

4. **Envío por correo** (canal `correo`, dentro del tope):
   - Asunto: si la oferta pide un asunto, úsalo exactamente. Si no: `Postulación: <Cargo> - David Ariza López`.
   - Cuerpo en español, cordial y directo, de 120 a 170 palabras, sin emojis:
     saludo ("Respetado equipo de selección de <Empresa>:" o el nombre del reclutador si aparece) →
     a qué cargo se postula y dónde vio la oferta → 3 viñetas con hechos del perfil que responden a los
     requisitos → disponibilidad para trasladarse si la vacante no está en Barranquilla → invitación a
     conversar → firma: David Ariza López, Ingeniero Industrial, Esp. en Logística Empresarial,
     +57 300 274 0653, linkedin.com/in/davidarizalpz.
     Si la oferta pide aspiración salarial, escribe: "Mi aspiración salarial es superior a $9.000.000
     mensuales, negociable según el paquete integral." Si no la pide, no menciones salario.
   - Envía con `send_message`: `to` = el correo de la oferta, `body` en texto plano y `htmlBody` con el
     mismo contenido en HTML simple, y en `attachments` **solo el PDF** (referencia
     `sha256:<hash>:<ruta>`, `mimeType: application/pdf`, `filename: CV_David_Ariza_<Empresa>.pdf`).
   - Ponle la etiqueta `CONFIG.ETIQUETA_POSTULACIONES` al mensaje enviado (`label_message`).
   - Registra la entrada con `estado: enviada`, `thread_id` y `message_id`.

5. **Canal portal:** registra la entrada con `estado: lista_para_portal`, la URL de la oferta y los
   enlaces del CV. El Resumen matutino se los presenta a David para que aplique.

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

8. **Cierre:** un párrafo con los correos enviados (empresa y cargo), los CV listos para portal, los
   seguimientos y las respuestas recibidas.
