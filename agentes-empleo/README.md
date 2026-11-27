# Agentes de búsqueda de empleo

Seis agentes programados en Claude Code (sesiones en la nube) que buscan empleo directivo en todas las
vertientes de la ingeniería industrial: logística, operaciones, proyectos, administrativo, comercial, servicio al
cliente, producción y compras (prioridad Colombia y Costa Norte; también remoto y otros países), adaptan la hoja de vida en formato ATS y escriben una carta de presentación para cada oferta, las envían, y
cada mañana entregan un resumen con lo que hay que hacer ese día.

| Agente | Horario (Bogotá) | Qué hace | Instrucciones |
|---|---|---|---|
| 1. Buscador | todos los días, 05:13 · 13:13 · 19:13 | Recorre Computrabajo, Elempleo, Magneto, LinkedIn (ofertas públicas de Colombia, Latinoamérica, España y EE. UU.) y Torre/headhunters por búsqueda web; filtra por salario > $9M COP o su equivalente, contrato indefinido y prioridad Costa Norte; puntúa la afinidad | [`agentes/01-buscador.md`](agentes/01-buscador.md) |
| 2. Postulador | lunes a viernes, 07:37 · 14:37 | Genera el CV ATS y una carta de presentación personalizada para cada oferta (PDF + Word), los envía si la oferta publica un correo (máx. 8/día), los deja listos para portales y hace seguimiento a los 5 días hábiles | [`agentes/02-postulador.md`](agentes/02-postulador.md) |
| 3. LinkedIn | todos los días, 06:07 | Plan de 15 minutos: 10 personas para conectar con notas listas, una acción de LinkedIn Premium (InMail, quién vio tu perfil, Learning), comentarios y una mejora del perfil por día. No automatiza la cuenta | [`agentes/03-linkedin.md`](agentes/03-linkedin.md) |
| 4. Resumen matutino | todos los días, 06:41 | Correo con correos enviados, ofertas para seguimiento, respuestas de empresas, postulaciones por portal pendientes, qué corregir en LinkedIn y las cuentas de empleo remoto para crear | [`agentes/04-resumen-matutino.md`](agentes/04-resumen-matutino.md) |
| 5. Empleo remoto | todos los días, 17:23 | Recorre portales de trabajo remoto (Remotive, Remote OK, We Work Remotely, Himalayas, Jobicy, Get on Board, Working Nomads y LinkedIn remoto), puntúa las ofertas que se pueden hacer desde Colombia y lleva la guía de en qué plataformas crear cuenta (David las crea; nada se automatiza) | [`agentes/05-remoto.md`](agentes/05-remoto.md) |
| 6. Marca personal | lunes, 05:47 | Plan semanal de publicaciones para LinkedIn (e Instagram cuando esté conectada la cuenta profesional): temas con logros reales, imágenes y videos de Higgsfield y borradores en Metricool que solo se publican con el OK de David; le pregunta cada lunes si está de acuerdo | [`agentes/06-marca-personal.md`](agentes/06-marca-personal.md) |

Reglas comunes (veracidad, criterios, puntaje, almacenamiento): [`agentes/00-comun.md`](agentes/00-comun.md).

## Scripts

- `scripts/buscar_ofertas.py`: buscador multiportal (solo biblioteca estándar de Python). Uso:
  `python3 buscar_ofertas.py --vistas vistas.txt --salida resultado.json [--portales Computrabajo,Elempleo,Magneto,LinkedIn]`
- `scripts/buscar_remoto.py`: ofertas remotas desde APIs y RSS públicos y LinkedIn (solo biblioteca estándar). Uso:
  `python3 buscar_remoto.py --vistas vistas_remoto.txt --salida remoto.json --usd-cop 4000`
- `scripts/generar_cv.js`: CV en formato ATS (PDF de una columna, máximo 2 páginas) con Playwright y Chromium.
  Uso: `node generar_cv.js cv.json salida.pdf`
- `scripts/generar_cv_docx.py`: el mismo CV en Word (python-docx). Uso: `python3 generar_cv_docx.py cv.json salida.docx`
  Con `"idioma": "en"` en el JSON, ambos generadores ponen los títulos y etiquetas en inglés.
- `scripts/generar_carta.js` y `scripts/generar_carta_docx.py`: carta de presentación de una página (PDF y Word).
  Uso: `node generar_carta.js carta.json salida.pdf` y `python3 generar_carta_docx.py carta.json salida.docx`
- `ejemplos/cv_ejemplo.json` y `ejemplos/carta_ejemplo.json`: estructura de los JSON que reciben los generadores
  (datos ficticios).

## Datos privados

Este repositorio es público, así que **no** contiene datos personales. El perfil maestro (fuente única de
verdad del CV), las ofertas encontradas, el historial de postulaciones y los CV generados viven en una
carpeta privada de Google Drive. Los IDs de esa carpeta y de las etiquetas de Gmail llegan a cada agente
en el bloque `CONFIG` de su tarea programada.

## Red necesaria en el entorno de la nube

Hosts permitidos: `co.computrabajo.com`, `www.elempleo.com`, `www.magneto365.com`, `search.torre.co`,
`torre.ai` y `www.linkedin.com`; para el agente de empleo remoto, `remotive.com`, `remoteok.com`,
`weworkremotely.com`, `himalayas.app`, `jobicy.com`, `www.getonbrd.com` y `www.workingnomads.com`; para el agente de marca
personal, `d8j0ntlcm91z4.cloudfront.net` (imágenes de Higgsfield); además de los registros de paquetes. Gmail, Google Drive,
Metricool y Higgsfield entran como conectores.
