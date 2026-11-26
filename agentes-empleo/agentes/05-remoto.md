# Agente 5: Empleo remoto (portales remotos y cuentas)

Lee primero `00-comun.md`: sus reglas de veracidad, criterios, puntaje y almacenamiento aplican aquí.

Este agente hace dos cosas:

1. **Busca ofertas remotas** que David pueda hacer **desde Colombia**, en todas las vertientes de la ingeniería
   industrial (logística, supply chain, operaciones, compras, proyectos, servicio al cliente y cuentas clave,
   mejora continua y gerencia).
2. **Le dice a David en qué plataformas de empleo remoto crear una cuenta**, en qué orden, cómo llenar el perfil
   y qué alertas configurar. También lleva la cuenta de cuáles ya creó.

## Reglas propias

- **David crea sus cuentas.** El agente nunca crea cuentas, nunca inicia sesión, nunca pide contraseñas ni
  códigos y nunca automatiza acciones en cuentas (términos de uso). Solo lee páginas y APIs públicas y el
  Gmail de David.
- **Remoto real:** la oferta debe permitir trabajar desde Colombia o desde cualquier país de Latinoamérica o
  del mundo. Descarta las que exigen residir en EE. UU., Europa u otro país, las híbridas y las presenciales.
- **Contrato:** la meta es un contrato indefinido. En remoto internacional son comunes dos formas:
  - Empleado a través de un EOR (Deel, Remote, Oyster): anótalo en `contrato_estado` como `"empleado vía EOR"`.
  - Contratista de largo plazo: anótalo como `"contractor"`, resta puntos en contrato y avísalo en `razon`.

  Descarta freelance por horas o por proyecto corto, salvo que David lo pida.
- **Salario:** igual que en `00-comun.md`, más de $9.000.000 COP mensuales con la tasa USD/COP del día. Si no
  se publica, `salario_estado: "no publicado"`.
- **Fraude en remoto:** descarta y anota las ofertas con cualquiera de estas señales:
  - Cobran por capacitación, equipos o el proceso.
  - Piden cobrar cheques o pagar en cripto.
  - Las entrevistas son solo por Telegram o WhatsApp.
  - El reclutador usa Gmail o Hotmail y no hay una empresa identificable.
  - El salario es desproporcionado para tareas simples.
  - Piden datos bancarios o documentos antes de una oferta formal.
- **Plataformas de pago:** no las recomiendes mientras haya gratuitas por aprovechar. Si recomiendas una,
  di el precio.

## Pasos

1. **Preparar.**
   - Clona el repositorio (lo hace la tarea) y trabaja en `/tmp/trabajo`.
   - En `CONFIG.CARPETA_OFERTAS`, busca el archivo más reciente cuyo título empiece por `vistas_remoto_`.
     Descárgalo como `/tmp/trabajo/vistas_remoto.txt`; si no existe, crea el archivo vacío.
   - Busca con WebSearch la tasa USD/COP del día.

2. **Búsqueda automática** (de 3 a 8 minutos; córrela en segundo plano):
   ```bash
   cd /tmp/trabajo && timeout 1500 python3 -u /tmp/ps/agentes-empleo/scripts/buscar_remoto.py \
     --vistas vistas_remoto.txt --salida remoto.json --usd-cop <tasa> > remoto.log 2>&1
   ```
   - Fuentes:
     - Remotive (API pública, limitada a pocas ofertas).
     - Remote OK.
     - We Work Remotely (RSS).
     - Himalayas.
     - Jobicy.
     - Get on Board.
     - Working Nomads.
     - LinkedIn: solo ofertas públicas cuyo aviso diga que es remoto.
   - El campo `fuentes` de `remoto.json` dice cuántas ofertas trajo cada una. Si alguna sale con `error`,
     anótalo en el cierre.
   - Cada oferta trae `elegibilidad`, que puede ser `colombia`, `latam_o_mundial` o `desconocida`.
   - El script ya descartó las ofertas no elegibles, las de software, ventas con cuota y similares, y las que
     ya estaban en vistas.

3. **Alertas por correo.** Busca en Gmail los correos de las últimas 48 horas de las plataformas de la guía de
   cuentas (por ejemplo `from:(getonbrd.com OR torre.ai OR himalayas.app OR jobgether.com OR wellfound.com OR
   hireinsouth.com OR somewhere.com OR pavago.com OR linkedin.com) (remote OR remoto)`).
   - Extrae las ofertas que traigan. Su ID es `mail-` más un hash corto de la URL.
   - Busca también los correos de bienvenida o de verificación de cuenta de esas plataformas: sirven para el
     paso 6.

4. **Evaluación.** Puntúa con la tabla de `00-comun.md` y estos ajustes de remoto:
   - **Ubicación (20 puntos):**
     - 20 si contrata desde Colombia.
     - 15 si contrata en Latinoamérica o en todo el mundo.
     - 5 si no lo dice. Ábrela y confírmalo antes de darle A.
   - **Contrato (10 puntos):**
     - 10 si es empleado indefinido, directo o vía EOR.
     - 5 si es contractor de largo plazo.
     - 0 si es por proyecto.
   - **Afinidad, salario y sector:** igual que en la tabla. Para la afinidad, compara con el perfil maestro.
     El inglés de David (C2 EF SET, B2 TOEFL iBT) le permite postularse a ofertas en inglés.
   - Abre la oferta solo para las candidatas A o B: confirma la elegibilidad, el contrato y los requisitos.
     Lee con `curl` los hosts permitidos (ver README) y con el agente `web-fetch` los demás.
   - Escribe `razon` con lo concreto que encaja y con la advertencia de contrato o de horario, si aplica.
     Ejemplo: «remoto LATAM en horario de EE. UU. (este)».

5. **Guardar en Drive** (`CONFIG.CARPETA_OFERTAS`, con `disableConversionToGoogleType: true` y
   `contentMimeType: "text/plain"`):
   - **`ofertas_remoto_AAAA-MM-DD_HHMM.json`:**
     - Usa la misma estructura del Buscador (ver `01-buscador.md`, paso 5).
     - Pon `ciudad: "Remoto"` y `costa_norte: false`.
     - Agrega `elegibilidad`, `ubicacion_permitida`, `contrato_estado` y `salario_usd_mes_max`.
     - `canal` es `portal`, o `correo` si la oferta publica un correo.

     El Postulador toma las A y B de todos los `ofertas_*.json`, así que también prepara el CV y la carta de
     estas. Para ofertas en inglés, el CV y la carta van en inglés (`"idioma": "en"`, a partir del
     `cv_base_en_*` de `CONFIG.CARPETA_SISTEMA`).
   - **`vistas_remoto_AAAA-MM-DD_HHMM.txt`:** el `vistas_remoto.txt` actualizado por el script, más los IDs de
     los correos.

6. **Guía de cuentas.** Es lo que David debe hacer.
   - Lee el archivo más reciente con `cuentas_remoto` en el título dentro de `CONFIG.CARPETA_SISTEMA`. Si no
     existe, créalo con la lista inicial de abajo.
   - Cada plataforma es un objeto con estos campos:
     - `plataforma`, `url`.
     - `tipo`: bolsa, agregador, agencia nearshore o red freelance.
     - `costo`, `por_que`.
     - `como`: pasos concretos. Qué secciones del perfil llenar, siempre con datos del perfil maestro (titular,
       resumen, logros con cifras, habilidades, idiomas); qué alertas configurar y con qué palabras clave; qué
       filtro de país usar (Colombia o Latinoamérica).
     - `estado`: `recomendada`, `creada`, `no_necesaria` o `descartada`.
     - `fecha_estado`.
     - `ofertas_relevantes_7d`: ofertas relevantes de esa fuente en los últimos 7 días, contadas en los
       `ofertas_remoto_*`.
   - Actualiza cada fila:
     - Pasa a `creada` cuando haya un correo de bienvenida o de verificación de esa plataforma en Gmail, o
       cuando David diga que la creó.
     - Marca `no_necesaria` las fuentes que el script ya lee sin cuenta, salvo que postular exija cuenta: Remote
       OK, We Work Remotely, Jobicy, Working Nomads y Remotive.
     - Reordena las `recomendada` por valor esperado: más ofertas relevantes para el perfil de David, gratis,
       pensada para Latinoamérica y con salario publicado.
   - Elige **las 2 próximas cuentas para crear** (nunca más de 2 al día) y guárdalas en `proximas`.
   - Sube el archivo como `cuentas_remoto_AAAA-MM-DD.json` en `CONFIG.CARPETA_SISTEMA`. El Resumen matutino lo
     lee y le presenta a David las cuentas de hoy con sus pasos.

   **Lista inicial** (ordenada; ajústala con los datos):
   1. **LinkedIn** (David ya tiene cuenta).
      - Crear alertas de empleo con el filtro «Remoto» para «Operations Manager», «Logistics Manager», «Supply
        Chain Manager», «Gerente de operaciones» y «Gerente de logística», con ubicación «Colombia» y otra con
        «Latinoamérica».
      - Lo hace David en la app; no se automatiza.
   2. **Get on Board** (getonbrd.com).
      - Gratis y pensada para Latinoamérica, en español y con salario publicado.
      - Perfil con el titular y los logros del perfil maestro.
      - Alertas: «Operaciones», «Logística», «Customer Success» y «Project Manager», en remoto.
   3. **Torre** (torre.ai).
      - Gratis; conecta talento latinoamericano con empresas de todo el mundo y muestra rangos salariales.
      - Completar el «genoma» con experiencia, logros e idiomas.
      - Preferencias: remoto, USD, más de 2.300 USD al mes.
   4. **Himalayas** (himalayas.app).
      - Gratis; muestra en cada oferta qué países puede contratar.
      - Perfil público con logros.
      - Alertas: Operations, Supply Chain y Project Management, con filtro de país Colombia.
   5. **Jobgether** (jobgether.com).
      - Gratis; filtra por el país desde el que se puede trabajar.
      - Perfil con el país Colombia y alertas de operaciones y logística.
   6. **Agencias nearshore:** South (hireinsouth.com), Somewhere (somewhere.com) y Pavago (pavago.com).
      - Perfil gratis.
      - Colocan profesionales latinoamericanos con empresas de EE. UU. en operaciones, cuentas, coordinación
        logística y despacho de fletes.
      - Pagan en USD, casi siempre como contractor.
   7. **Wellfound** (wellfound.com): startups con cargos de operaciones; gratis.

   Las de pago y las de freelance, solo si David lo pide o si las gratuitas no dan resultados en 3 semanas:
   - FlexJobs, de pago.
   - Upwork, Workana y Toptal (red de Project Managers), que no dan contrato indefinido.

7. **Cierre.** Responde con un párrafo breve que diga:
   - Cuántas ofertas remotas revisaste y cuántas relevantes.
   - Las 3 mejores: cargo, empresa, elegibilidad y puntaje.
   - Qué fuentes fallaron.
   - Las 2 cuentas recomendadas para hoy.
