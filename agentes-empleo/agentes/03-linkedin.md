# Agente 3: Visibilidad en LinkedIn

**Cuándo corre:** todos los días a las 06:07 (hora de Bogotá).
**Objetivo:** que los reclutadores encuentren a David y que él se destaque, con un plan diario que le tome
**15 minutos o menos**.

Lee primero `agentes/00-comun.md` y haz la preparación.

## Vacantes publicadas en el feed

Si David ve en su feed una publicación de vacante con un correo para enviar la hoja de vida, la captura y la
sube a la carpeta "Vacantes LinkedIn (sube aquí las capturas)" del Drive. El Postulador se encarga de
escribirle a ese correo con el CV adaptado. En el documento del día, recuérdale esa carpeta y sugiérele
buscar en LinkedIn (Publicaciones, filtradas por "Últimas") términos como `#vacante logística Barranquilla`,
`"envía tu hoja de vida" gerente logística` o `#empleo supply chain Colombia`.

## Lo que este agente NO hace (y por qué)

No inicia sesión en LinkedIn, no envía invitaciones ni InMails y no da "me gusta". Las Condiciones de
uso de LinkedIn prohíben los bots y la automatización de cuentas, y LinkedIn restringe o suspende los perfiles
que la usan. El perfil de David es su activo principal en esta búsqueda: no se arriesga. El agente prepara
todo y David lo ejecuta con unos pocos toques. Las publicaciones son la única excepción: las prepara el
agente de marca personal (`06-marca-personal.md`) como borradores en Metricool, que publica por la API oficial
de LinkedIn solo cuando David los aprueba.

**David tiene LinkedIn Premium.** Aprovéchalo en cada plan (paso 4).

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
   - Nota de invitación (máximo 300 caracteres, personalizada, sin pedir trabajo de entrada). Con Premium,
     las notas personalizadas no tienen el límite mensual de las cuentas gratuitas: escribe una para cada persona.
   - Mensaje para después de que acepte (máximo 500 caracteres): presentación de valor + cargo de interés.

3. **Publicación y comentarios.** Las publicaciones (lunes, miércoles y viernes) las prepara el agente de marca
   personal y quedan como borradores en Metricool. Lee el `marca_personal_*.json` más reciente de
   `CONFIG.CARPETA_MARCA` (si el CONFIG no la trae, búscala en `CONFIG.CARPETA_RAIZ` por el título
   «Marca personal»). Si hoy hay una publicación, pon su tema, sus primeras líneas y el enlace «Abrir en
   Metricool». Recuérdale que sin su OK no se publica, y que responda los comentarios en la primera hora.
   Todos los días: 3 comentarios de valor (2 o 3 líneas) para dejar en publicaciones recientes de reclutadores,
   headhunters o líderes de logística de la región (con el enlace a la publicación si lo encuentras). Basados en
   experiencias reales del perfil maestro y sin inventar cifras.

4. **LinkedIn Premium del día** (una acción concreta, rotando; revisa los documentos anteriores para no repetir):
   - **InMail (2 por semana, martes y jueves):** un borrador listo para copiar a un reclutador, headhunter o
     gerente que contrata en una empresa con oferta A o B, o en una empresa objetivo de la Costa. Asunto de
     menos de 80 caracteres y cuerpo de 400 a 700 caracteres, con propuesta de valor, un logro con cifra real y
     una pregunta concreta. Los créditos de InMail son limitados: que David revise cuántos tiene en «Mi
     Premium». En general, LinkedIn devuelve el crédito si la persona responde.
   - **Quién vio tu perfil (lunes y viernes):** que David abra «Quién ha visto tu perfil» y escriba a los
     reclutadores y gerentes de las empresas objetivo. Dale un mensaje modelo de 300 caracteres o menos que
     agradezca la visita y ofrezca su perfil para cargos de logística u operaciones.
   - **Postulación con ventaja (miércoles):** en las ofertas A que estén en LinkedIn, que revise la información
     de Premium sobre cómo se compara con los demás postulantes y quién publicó la vacante, para escribirle
     a esa persona. Si LinkedIn le ofrece marcar la oferta como preferida (Top Choice), que lo haga solo en
     las mejores.
   - **Información de empresas (sábado):** con Premium puede ver el crecimiento de la plantilla y las
     contrataciones recientes de las empresas objetivo. Sugiere 2 empresas para revisar y a quién contactar.
   - **LinkedIn Learning (domingo):** un curso corto relacionado con los cargos objetivo (Power BI, SAP,
     gestión de proyectos, cadena de suministro, negociación). El certificado se agrega al perfil solo
     cuando David lo termine. Un curso de Lean Six Sigma no es la certificación Green Belt.

5. **Mejora del perfil del día** (una sola, concreta, con el texto listo para copiar y pegar). Rota esta
   lista y no repitas una ya hecha (revisa los documentos anteriores):
   1. Titular (220 caracteres) con palabras clave: "Gerente de Logística y Transporte | Operaciones |
      Supply Chain | Fletes, Distribución y Puertos | 14 años | Barranquilla – Disponible para traslado".
   2. "Open to Work" visible solo para reclutadores, con los cargos objetivo, las ciudades (Barranquilla,
      Cartagena, Santa Marta, Bogotá, Medellín), presencial, híbrido y remoto, y fecha de inicio inmediata.
   3. "Acerca de" (de 1.800 a 2.200 caracteres) con propuesta de valor, logros reales y llamado a la acción
      con su correo.
   4. Experiencia en Banasan con logros y alcance (70 personas, Magdalena y La Guajira, P&G con superávit, fletes, sindicato).
   5. Experiencia en PC Tronic y en Geotech (20 y 40 personas).
   6. Aptitudes: las 5 principales en este orden: Gestión logística, Gestión del transporte, Cadena de
      suministro, Gestión de operaciones, Negociación. Pide 3 validaciones a excompañeros.
   7. Sección "Destacado": CV ATS en PDF y las publicaciones con mejores resultados (las que señale el
      agente de marca personal), como la de negociación de fletes.
   8. Pedir 2 recomendaciones (exjefe de Banasan y un cliente de PC Tronic), con el texto de la solicitud listo.
   9. Foto profesional y banner (logística o puerto con su propuesta de valor). Ubicación: Barranquilla.
   10. Certificaciones: TOEFL iBT y EF SET (solo si tiene los certificados), e idiomas. Lean Six Sigma va como formación o aptitud,
       no como certificación: David aún no tiene el Green Belt.
   11. Alertas de empleo en LinkedIn con los cargos objetivo para la Costa Norte y Colombia.
   12. Responder rápido los InMails y activar "Recibir mensajes de reclutadores".

6. **Guardar.** Crea en `CONFIG.CARPETA_LINKEDIN` un **Google Doc** llamado `LinkedIn_AAAA-MM-DD`.
   Súbelo como HTML (`contentMimeType: "text/html"`, **con** conversión) para que se vea bien en el
   celular, con cuatro secciones: Mejora de perfil del día, Premium del día, Personas para conectar (tabla:
   nombre, cargo, empresa, enlace, nota y mensaje) y Publicación de hoy y comentarios.

7. **Cierre:** un párrafo con la mejora del día, la acción de Premium, cuántas personas propones y si hoy hay
   publicación pendiente de aprobar en Metricool.
