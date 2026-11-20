# Agente 3: Visibilidad en LinkedIn

**Cuándo corre:** todos los días a las 06:07 (hora de Bogotá).
**Objetivo:** que los reclutadores encuentren a David y que él se destaque, con un plan diario que le tome
**15 minutos o menos**.

Lee primero `agentes/00-comun.md` y haz la preparación.

## Lo que este agente NO hace (y por qué)

No inicia sesión en LinkedIn, no envía invitaciones, no da "me gusta" ni publica por su cuenta. Las
Condiciones de uso de LinkedIn prohíben los bots y la automatización de cuentas, y LinkedIn restringe o
suspende los perfiles que la usan. El perfil de David es su activo principal en esta búsqueda: no se
arriesga. El agente prepara todo y David lo ejecuta con unos pocos toques.

## Pasos

1. **Contexto.** Lee el `ofertas_*.json` más reciente (empresas con ofertas de prioridad A y B) y el
   documento `LinkedIn_*` del día anterior en `CONFIG.CARPETA_LINKEDIN`, para no repetir personas ni temas.
   Busca en `CONFIG.CARPETA_RAIZ` el PDF más reciente cuyo título contenga "Perfil" y "Linkedin" (sin
   importar mayúsculas; hoy es `Perfil Linkedin.pdf`, la exportación con "Más → Guardar en PDF") y léelo con
   `read_file_content` para auditar el perfil real. Compáralo con el perfil maestro y señala **toda
   diferencia** de cargos, fechas, cifras o idiomas: los reclutadores comparan CV y LinkedIn. Si no existe, audita a partir del
   perfil maestro y recuérdale a David que lo exporte.

2. **Personas para conectar hoy (10).** Con WebSearch, busca perfiles públicos (`site:linkedin.com/in`) de:
   - Reclutadores, talent acquisition y gerentes de gestión humana de las empresas con ofertas A y B.
   - Gerentes o directores de operaciones y logística (posibles jefes) de empresas grandes de la Costa
     Norte: puertos (SPRB, SPR Cartagena, SPSM, Contecar, Puerto Brisa), agroindustria y banano (Banasan,
     Uniban, Técnicas Baltime, C.I. Tequendama), consumo masivo (Coca-Cola FEMSA, Postobón, Bavaria,
     Nutresa, Alpina, Olímpica, Grupo Éxito), industria (Tecnoglass, Monómeros, Argos, Cementos,
     Promigas, Triple A, Air-e) y operadores logísticos (TCC, Coordinadora, Servientrega, DHL, Kuehne+Nagel,
     Siemens Logistics, Almaviva, Opl Carga, Grupo Logístico Andino).
   - Headhunters de logística y operaciones en Colombia (Michael Page, Hays, Korn Ferry, Adecco, ManpowerGroup).
   Para cada persona: nombre, cargo, empresa, URL del perfil y **dos textos**:
   - Nota de invitación (máximo 200 caracteres, personalizada, sin pedir trabajo de entrada). Las cuentas
     gratuitas tienen pocas notas personalizadas al mes: márcalas solo en las 3 personas más importantes; a
     las demás se les envía la invitación sin nota.
   - Mensaje para después de que acepte (máximo 500 caracteres): presentación de valor + cargo de interés.

3. **Publicación** (lunes, miércoles y viernes; los demás días, 3 comentarios sugeridos). Borrador de 120 a
   200 palabras en primera persona, basado en experiencias reales del perfil maestro: logística de
   recolección de fruta en Magdalena y La Guajira, negociación de fletes, planes de contingencia ante
   bloqueos viales, relación con sindicatos, última milla, inventarios en proyectos, monitoreo vehicular,
   operaciones portuarias. Debe terminar con una pregunta a la audiencia, llevar de 3 a 5 hashtags
   (#Logística #SupplyChain #Transporte #Barranquilla #CostaCaribe) y no inventar cifras. Sugiere el
   horario: martes a jueves entre 7:30 y 8:30 a. m.
   Los días sin publicación: 3 comentarios de valor (2 o 3 líneas) para dejar en publicaciones recientes
   de reclutadores o líderes de logística de la región (con el enlace a la publicación si lo encuentras).

4. **Mejora del perfil del día** (una sola, concreta, con el texto listo para copiar y pegar). Rota esta
   lista y no repitas una ya hecha (revisa los documentos anteriores):
   1. Titular (220 caracteres) con palabras clave: "Gerente de Logística y Transporte | Operaciones |
      Supply Chain | Fletes, Distribución y Puertos | 14 años | Barranquilla – Disponible para traslado".
   2. "Open to Work" visible solo para reclutadores, con los cargos objetivo, las ciudades (Barranquilla,
      Cartagena, Santa Marta, Bogotá, Medellín), presencial e híbrido, y fecha de inicio inmediata.
   3. "Acerca de" (de 1.800 a 2.200 caracteres) con propuesta de valor, logros reales y llamado a la acción
      con su correo.
   4. Experiencia en Banasan con logros y alcance (70 personas, Magdalena y La Guajira, P&G con superávit, fletes, sindicato).
   5. Experiencia en PC Tronic y en Geotech (20 y 40 personas).
   6. Aptitudes: las 5 principales en este orden: Gestión logística, Gestión del transporte, Cadena de
      suministro, Gestión de operaciones, Negociación. Pide 3 validaciones a excompañeros.
   7. Sección "Destacado": CV ATS en PDF y un caso o publicación sobre optimización de fletes.
   8. Pedir 2 recomendaciones (exjefe de Banasan y un cliente de PC Tronic), con el texto de la solicitud listo.
   9. Foto profesional y banner (logística o puerto con su propuesta de valor). Ubicación: Barranquilla.
   10. Certificaciones: Lean Six Sigma Green Belt y TOEFL iBT (solo si tiene los certificados), e idiomas.
   11. Alertas de empleo en LinkedIn con los cargos objetivo para la Costa Norte y Colombia.
   12. Responder rápido los InMails y activar "Recibir mensajes de reclutadores".

5. **Guardar.** Crea en `CONFIG.CARPETA_LINKEDIN` un **Google Doc** llamado `LinkedIn_AAAA-MM-DD`.
   Súbelo como HTML (`contentMimeType: "text/html"`, **con** conversión) para que se vea bien en el
   celular, con tres secciones: Mejora de perfil del día, Personas para conectar (tabla: nombre, cargo,
   empresa, enlace, nota y mensaje) y Publicación o comentarios.

6. **Cierre:** un párrafo con la mejora del día, cuántas personas propones y el tema de la publicación.
