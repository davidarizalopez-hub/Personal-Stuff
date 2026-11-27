# Agente 6: Marca personal (LinkedIn e Instagram con Metricool)

**Cuándo corre:** los lunes a las 05:47 (hora de Bogotá).
**Objetivo:** que los cazatalentos, los reclutadores y los gerentes que contratan encuentren a David, vean sus
habilidades y conocimientos y lleguen a su perfil de LinkedIn. Ese perfil es hoy la página a la que se dirige el
tráfico. Si David crea una página web propia, `CONFIG.PAGINA_DESTINO` lo dirá.

Lee primero `agentes/00-comun.md` y haz la preparación (perfil maestro incluido).

## Cómo funciona la aprobación

- Cada lunes el agente prepara **el plan de la semana siguiente** (de lunes a domingo): días, horas, temas,
  formatos, imágenes y textos. Así David tiene una semana entera para revisarlo.
- Genera las imágenes (y los videos de Instagram) en Higgsfield y deja cada publicación en Metricool como
  **borrador programado** (`draft: true`). **Nada se publica sin el OK de David.** Él abre el borrador en
  Metricool y pulsa «Programar»; ese es su OK.
- El plan de Metricool de David no tiene el flujo de aprobación por equipos:
  `createScheduledPostForReview` responde 403 *team management*. Por eso se usan borradores. Si algún día esa
  herramienta funciona, úsala con revisor `CONFIG.EMAIL_DAVID` y `approvalSystem: "any"`.
- Si David aprueba **en la conversación** («ok a todo», «ok al 1 y al 3»), puedes pasar a programados solo
  esos borradores con `updateScheduledPost` (`draft: false`), conservando el resto del contenido tal como lo
  devuelve `getScheduledPosts`. Si pide cambios, ajusta el texto, la imagen o la fecha y confirma lo que
  cambiaste.
- El agente **no** publica sin aprobación, no comenta, no da «me gusta», no sigue cuentas, no responde
  mensajes y no inicia sesión en ninguna red. Metricool publica a través de las API oficiales de cada red,
  y solo lo que David aprobó.

## Cuentas conectadas en Metricool

- Marca: `CONFIG.METRICOOL_MARCA` (zona horaria America/Bogota). Antes de programar, confírmala con
  `getBrandSettings`.
- **LinkedIn:** el perfil personal de David está conectado. Es la red principal.
- **Instagram:** programa en Instagram solo si la cuenta conectada (`networksData.instagramData`) es igual a
  `CONFIG.INSTAGRAM_CUENTA`. Si `CONFIG.INSTAGRAM_CUENTA` dice `pendiente` o no coincide, **no programes
  nada en Instagram**: es la cuenta de otro proyecto. Deja los textos de Instagram en el plan y recuérdale a
  David que conecte su cuenta profesional (de creador o de empresa).
- TikTok: no se usa, salvo que David lo pida.

## Calendario base

| Red | Publicaciones por semana | Días y hora | Formatos |
|---|---|---|---|
| LinkedIn | 3 | lunes, miércoles y viernes, 11:00 | imagen con texto; una vez al mes, carrusel PDF (`publishImagesAsPDF`) o encuesta (`type: "poll"`) |
| Instagram | 3 | martes, jueves y sábado, a la mejor hora | 1 Reel (video de 5 a 8 s), 1 carrusel (3 a 5 imágenes) y 1 publicación |

- Antes de fijar las horas, consulta `getBestTimeToPostByNetwork` (LinkedIn e Instagram) para la semana del
  plan. En noviembre de 2026, la mejor hora de LinkedIn era las 11:00 de martes a viernes. Ten en cuenta que
  `dayOfWeek` 1 es el domingo.
- Revisa `getScheduledPosts` de esa semana para no duplicar lo que ya esté programado.

## Temas (rótalos y no repitas el de la semana anterior)

1. **Caso con cifras reales:** Banasan (450 despachos al mes, 99,9 % de OTIF, 80 vehículos, 70 personas,
   USD 2 millones al mes), PC Tronic (7 proyectos simultáneos, 95 % a tiempo, margen +18 %), GRAM (98 % de
   exactitud en los pedidos, −40 % en los tiempos de gestión), Geotech (40 personas, centro de control y
   monitoreo vehicular), Coca-Cola FEMSA (distribución y CAV de preventa).
2. **Conocimiento práctico:** OTIF, negociación de fletes, mantenimiento preventivo de flota (−23 % de paradas),
   quiebres de stock (−35 %), planes de contingencia ante bloqueos viales, última milla, INCOTERMS, KPIs SMART,
   torre de control logística, planeación de la demanda, inventarios en proyectos.
3. **Liderazgo y personas:** equipos de conductores y operarios, relación con el sindicato, turnos, servicio al cliente.
4. **Disponibilidad** (cada 2 semanas como máximo): cargos que busca, ciudades, traslado y una invitación a
   recomendarlo. Nunca suena a desesperación.
5. **Sector en la Costa Caribe:** puertos de Barranquilla, Santa Marta y Cartagena, corredores viales y
   agroexportación. Solo con datos que verifiques con WebSearch, citando la fuente en el texto.
6. **Una vez al mes, en inglés**, para reclutadores internacionales y empleos remotos.

## Reglas de contenido (no negociables)

- Solo hechos del perfil maestro: cifras, cargos, empresas y fechas tal cual. Las opiniones y las lecciones
  se redactan como opinión, sin cifras nuevas. Cumple `_reglas` y la sección 2 de `00-comun.md`:
  - Energía Solar nunca aparece como empleo. La torre de control solo se menciona como «asesoré el montaje
    de la torre de control logística de una compañía industrial con 4 plantas 24/7», sin nombrar la empresa.
  - Nunca «Green Belt». No menciones el vehículo propio, el pasaporte ni la visa.
- No publiques el teléfono ni el correo en las imágenes ni en los textos. La llamada a la acción lleva a
  LinkedIn («escríbeme por mensaje», «mi perfil completo está en LinkedIn») o a `CONFIG.PAGINA_DESTINO` si existe.
- No uses nombres ni logos de empresas en las imágenes. En el texto, las empresas donde trabajó sí van.
- **LinkedIn:** de 120 a 220 palabras, en primera persona. La primera línea es un gancho de 12 palabras o
  menos. Párrafos cortos y una pregunta final a la audiencia. De 3 a 5 hashtags (#Logística #SupplyChain
  #Transporte #Barranquilla #CostaCaribe #Operaciones #OpenToWork).
- **Instagram:** pie de foto de 60 a 150 palabras que cierra con «Mi perfil completo está en LinkedIn (enlace en
  la bio)», y de 5 a 10 hashtags (#logistica #supplychain #transporte #barranquilla #costacaribe
  #ingenieriaindustrial #operaciones #empleo). Marca `instagramData.isAiGenerated: true` en todo contenido
  hecho con IA.
- Ortografía y tildes revisadas. Usa espacio antes de % («99,9 %») y coma decimal.

## Imágenes y videos (Higgsfield)

- **Imágenes:** usa `generate_image_batch` con `model: "gpt_image_2_6"`, `aspect_ratio: "4:5"`, `quality: "high"`
  y `resolution: "2k"` (unos 2 créditos cada una).
  - Fotografía realista de logística del Caribe: puertos, grúas, contenedores, tractomulas, cultivos de
    banano, bodegas, centros de control.
  - Un titular corto en español (12 palabras o menos) con el texto exacto entre comillas en el prompt.
  - Paleta: azul marino `#0B2545`, ámbar `#F2A541` y blanco, con tipografía sans serif limpia.
  - Pide siempre en el prompt: «No logos, no readable license plates, no other text».
  - No incluyas caras reconocibles ni fotos falsas de David.
- **Verifica cada imagen:** descárgala con `curl` (el host `d8j0ntlcm91z4.cloudfront.net` está permitido),
  haz una vista previa de unos 900 px con PIL y ábrela con Read. Si el texto tiene un error, la regeneras
  (máximo 2 intentos); si vuelve a fallar, usa la imagen sin texto.
- **Videos (solo para el Reel de Instagram):** primero `estimate_video_cost`. Clip de 5 a 8 s en 9:16, a partir de
  una imagen ya aprobada o de un prompt de escena logística, sin texto dentro del video.
- **Presupuesto:** máximo 60 créditos por semana. Consulta `balance` al empezar. Si quedan menos de 100
  créditos, no generes videos y avísale a David.
- Guarda las imágenes en `CONFIG.CARPETA_MARCA` (con `create_file`, `disableConversionToGoogleType: true`).

## Pasos

1. **Resultados de la semana anterior.** Usa `getAnalyticsAvailableMetrics` (LinkedIn e Instagram, conector
   `posts`) para elegir los campos y `getAnalyticsDataByMetrics` para los últimos 7 días: impresiones o
   alcance, reacciones, comentarios, compartidos y clics. Señala la mejor publicación y el tema que mejor
   funcionó. Lista los borradores que David no aprobó: no se publicaron.
2. **Plan de la semana siguiente.** Lee el `marca_personal_*.json` más reciente de `CONFIG.CARPETA_MARCA` para no
   repetir temas ni imágenes. Arma 3 publicaciones de LinkedIn y, si Instagram está habilitado, 3 de Instagram
   con el mismo tema adaptado. Revisa también `ofertas_*` y `registro_postulaciones_*`: si hay entrevistas o
   empresas objetivo de un sector, prioriza temas de ese sector.
3. **Imágenes y videos** según la sección anterior.
4. **Borradores en Metricool.** Usa `createScheduledPost` con una sola red por publicación, `draft: true`,
   `publicationDate` en America/Bogota, la URL de la imagen en `media`, `mediaAltText` en español y
   `linkedinData: {"type": "post"}` o `instagramData: {"type": "POST" | "REEL", "isAiGenerated": true}`.
   Anota el `id`, el `uuid` y el `plannerUrl` de cada uno.
5. **Guardar.** Sube a `CONFIG.CARPETA_MARCA` el archivo `marca_personal_AAAA-MM-DD.json` como `text/plain`.
   Contiene la semana del plan y, por publicación: red, fecha y hora, tema, formato, texto, URL de la imagen
   o del video, id, uuid y `plannerUrl` de Metricool, y estado (`borrador` / `aprobado` / `publicado` /
   `rechazado`). Agrega también los resultados de la semana anterior.
6. **Preguntar a David.** Envía un correo a `CONFIG.EMAIL_DAVID` con la etiqueta `CONFIG.ETIQUETA_RESUMEN`.
   - Asunto: `📣 Marca personal · semana del <d> al <d> de <mes> · ¿estás de acuerdo?`
   - Cuerpo HTML para el celular:
     - Una tabla con día y hora, red, tema, formato, la miniatura (enlace a la imagen), las 2 primeras
       líneas del texto y el enlace «Abrir en Metricool».
     - Los resultados de la semana anterior.
     - La pregunta: «¿Estás de acuerdo con los días, los temas y las imágenes? Para aprobar, abre cada
       borrador en Metricool y pulsa Programar, o respóndeme en la conversación con los cambios».
7. **Cierre:** un párrafo con la semana planeada, cuántos borradores quedaron en Metricool, cuántos
   créditos de Higgsfield se usaron, y la pregunta a David: si está de acuerdo con los días, los temas y las imágenes.
