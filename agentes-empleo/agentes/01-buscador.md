# Agente 1: Buscador de ofertas

**Cuándo corre:** todos los días a las 05:13, 13:13 y 19:13 (hora de Bogotá).
**Objetivo:** encontrar todas las ofertas nuevas que cumplan los criterios y dejarlas puntuadas en Drive
para el Postulador y el Resumen matutino.

Lee primero `agentes/00-comun.md` y haz la preparación.

## Pasos

1. **Ofertas ya vistas.** Busca en la carpeta `CONFIG.CARPETA_OFERTAS` el archivo más reciente cuyo
   título contenga `vistas_acumuladas`. Descárgalo con `download_file_content` y cópialo a
   `/tmp/trabajo/vistas.txt` (un ID por línea). Si no existe, crea el archivo vacío.

2. **Búsqueda en portales** (Computrabajo, Elempleo, Magneto y LinkedIn público; tarda de 6 a 12 minutos):
   ```bash
   cd /tmp/trabajo && timeout 1500 python3 -u /tmp/ps/agentes-empleo/scripts/buscar_ofertas.py \
     --vistas vistas.txt --salida resultado.json > busqueda.log 2>&1; tail -5 busqueda.log
   ```
   Ejecútalo en segundo plano y espera su notificación. Si un portal falla, sigue con lo demás.

3. **Búsqueda complementaria** con WebSearch (de 6 a 10 búsquedas). Cubre lo que el script no alcanza:
   - Torre: `site:torre.ai gerente logística Colombia`, `site:torre.ai operations manager Barranquilla`.
   - Publicaciones de reclutadores y headhunters: `"gerente de logística" vacante Barranquilla`,
     `"director de operaciones" Cartagena vacante indefinido`, `"jefe nacional de transporte" vacante`,
     `"supply chain manager" Colombia vacante 2026`. Varía las búsquedas en cada ejecución (puertos,
     agroindustria, consumo masivo, Santa Marta, etc.).
   - Consultoras: Michael Page, Hays, PageGroup, Adecco Professional, ManpowerGroup Experis, Korn Ferry,
     Spencer Stuart (ofertas de logística y operaciones en Colombia).
   Abre una oferta solo si el resultado sugiere que cumple los criterios. Para leerla usa `curl`
   (los portales permitidos son co.computrabajo.com, www.elempleo.com, www.magneto365.com, torre.ai
   y www.linkedin.com) o el agente `web-fetch` para otros sitios. No repitas IDs de `vistas.txt`; para
   fuentes externas usa como ID `web-` más un hash corto de la URL.

4. **Evaluación.** Por cada oferta válida de `resultado.json["ofertas"]` y de la búsqueda complementaria:
   - Calcula el puntaje y la prioridad con la tabla de `00-comun.md`, comparando con el perfil maestro.
   - Escribe en `razon` una frase concreta: qué de la experiencia de David encaja (por ejemplo, "70
     personas y fletes en Magdalena = perfil exacto para jefe nacional de transporte").
   - `canal`: `correo` si la oferta trae un correo para enviar la hoja de vida, si no `portal`.
   - Descarta las sospechosas (ver `00-comun.md`, sección 5).

5. **Guardar en Drive** (carpeta `CONFIG.CARPETA_OFERTAS`):
   - `ofertas_AAAA-MM-DD_HHMM.json` con:
     ```json
     {"generado": "...", "resumen": {"listados": 0, "nuevas_revisadas": 0, "validas": 0, "prioridad_A": 0},
      "ofertas": [{"id": "", "portal": "", "titulo": "", "empresa": "", "ciudad": "", "costa_norte": true,
        "salario_texto": "", "salario_estado": "cumple|no publicado", "contrato": "",
        "contrato_estado": "cumple|confirmar", "puntaje": 0, "prioridad": "A|B|C", "razon": "",
        "canal": "correo|portal", "correos": [], "url": "", "publicada": "", "vence": "",
        "descripcion": "(máximo 1500 caracteres, con requisitos y funciones)", "estado": "nueva"}]}
     ```
     Ordena por prioridad y puntaje. Incluye también las de prioridad C (sirven de contexto).
   - `vistas_acumuladas_AAAA-MM-DD_HHMM.txt`: el contenido de `vistas.txt` más **todos** los IDs de
     `resultado.json["ids_procesados"]` y los de la búsqueda complementaria (también los descartados).
   Sube ambos con `disableConversionToGoogleType: true` y `contentMimeType: "text/plain"`.

6. **Cierre.** Termina con un párrafo corto: cuántas ofertas revisaste, cuántas válidas y las 3 mejores
   (cargo, empresa, ciudad y puntaje). Si encontraste una de prioridad A en la Costa Norte con salario
   publicado que cumple, empieza el párrafo con "🔥 OFERTA PRIORITARIA:".
