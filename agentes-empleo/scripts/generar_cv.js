#!/usr/bin/env node
// Genera un CV en formato ATS (PDF con texto seleccionable, una sola columna) a partir de un JSON.
// Uso: node generar_cv.js cv.json salida.pdf
// Reglas ATS que respeta la plantilla:
//   - Una sola columna, sin tablas, sin columnas, sin cuadros de texto, sin íconos ni imágenes.
//   - Datos de contacto en el cuerpo (no en encabezado/pie de página).
//   - Títulos de sección estándar (PERFIL PROFESIONAL, EXPERIENCIA LABORAL, EDUCACIÓN...).
//   - Fuente estándar (Arial/Liberation Sans), 10-11 pt, texto negro.
//   - Fechas en formato MM/AAAA en la misma línea del cargo.
//   - Viñetas simples. Máximo 2 páginas.
// Requiere Playwright con Chromium (preinstalado en las sesiones en la nube).
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const [, , entrada, salida] = process.argv;
if (!entrada || !salida) { console.error('Uso: node generar_cv.js cv.json salida.pdf'); process.exit(1); }
const cv = JSON.parse(fs.readFileSync(entrada, 'utf8'));
const e = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
// **negrita** permitida para resaltar cifras (los ATS ignoran el formato, no lo penalizan)
const b = (s) => e(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
const lista = (x) => Array.isArray(x) ? x.join(', ') : (x || '');

const c = cv.contacto || {};
const contacto = [
  c.telefono && `Teléfono: ${e(c.telefono)}`,
  c.email && `Correo: ${e(c.email)}`,
  c.linkedin && `LinkedIn: ${e(c.linkedin)}`,
  c.ubicacion && `Ubicación: ${e(c.ubicacion)}`,
].filter(Boolean).join(' | ');

const html = `<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>${e(cv.nombre)} - Hoja de vida</title>
<style>
  @page { size: A4; margin: 16mm 17mm 16mm 17mm; }
  body { font-family: "Liberation Sans", Arial, Helvetica, sans-serif; color: #000; font-size: 10.5pt; line-height: 1.35; margin: 0; }
  h1 { font-size: 18pt; margin: 0 0 2px; font-weight: 700; }
  .titular { font-size: 11pt; font-weight: 700; margin: 0 0 4px; }
  .contacto { font-size: 10pt; margin: 0 0 4px; }
  h2 { font-size: 11pt; font-weight: 700; text-transform: uppercase; margin: 12px 0 4px; padding-bottom: 2px; border-bottom: 1px solid #000; }
  p { margin: 0 0 4px; }
  .exp { margin: 0 0 8px; }
  .cargo { font-weight: 700; margin: 0; }
  .empresa { margin: 0 0 2px; }
  ul { margin: 2px 0 0 0; padding-left: 16px; }
  li { margin: 0 0 2px; }
</style></head><body>
<h1>${e(cv.nombre)}</h1>
<p class="titular">${e(cv.titular)}</p>
<p class="contacto">${contacto}</p>

<h2>Perfil profesional</h2>
<p>${b(cv.perfil)}</p>

${(cv.logros_clave || []).length ? `<h2>Logros destacados</h2><ul>${cv.logros_clave.map(l => `<li>${b(l)}</li>`).join('')}</ul>` : ''}

${(cv.competencias || []).length ? `<h2>Competencias clave</h2><p>${e(lista(cv.competencias))}</p>` : ''}

<h2>Experiencia laboral</h2>
${(cv.experiencia || []).map(x => `<div class="exp">
  <p class="cargo">${e(x.cargo)} | ${e(x.fechas)}</p>
  <p class="empresa">${e(x.empresa)}${x.lugar ? ', ' + e(x.lugar) : ''}</p>
  ${x.resumen ? `<p>${b(x.resumen)}</p>` : ''}
  <ul>${(x.logros || []).map(l => `<li>${b(l)}</li>`).join('')}</ul>
</div>`).join('')}

${(cv.otras_experiencias || []).length ? `<h2>Otras experiencias</h2><ul>${cv.otras_experiencias.map(x => `<li><strong>${e(x.cargo)}</strong> | ${e(x.empresa)} | ${e(x.fechas)}</li>`).join('')}</ul>` : ''}

<h2>Educación</h2>
<ul>${(cv.educacion || []).map(x => `<li><strong>${e(x.titulo)}</strong> | ${e(x.institucion)} | ${e(x.anio)}</li>`).join('')}</ul>

<h2>Habilidades técnicas</h2>
${cv.herramientas ? `<p>Herramientas: ${e(lista(cv.herramientas))}</p>` : ''}
${cv.metodologias ? `<p>Metodologías: ${e(lista(cv.metodologias))}</p>` : ''}

${cv.idiomas ? `<h2>Idiomas</h2><p>${e(lista(cv.idiomas))}</p>` : ''}
${cv.informacion_adicional ? `<h2>Información adicional</h2><p>${e(lista(cv.informacion_adicional))}</p>` : ''}
${cv.nota_final ? `<p style="margin-top:8px">${e(cv.nota_final)}</p>` : ''}
</body></html>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'load' });
  // Ajuste automático a 2 páginas como máximo (reduce la escala hasta 0.86)
  const maxPaginas = Number(process.env.CV_MAX_PAGINAS || 2);
  let escala = 1, buf, paginas;
  for (;;) {
    buf = await page.pdf({ format: 'A4', printBackground: false, preferCSSPageSize: true, scale: escala, tagged: true });
    paginas = (buf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
    if (paginas <= maxPaginas || escala <= 0.86) break;
    escala = Math.round((escala - 0.03) * 100) / 100;
  }
  fs.writeFileSync(salida, buf);
  console.log(`Páginas: ${paginas} (escala ${escala})`);
  if (paginas > maxPaginas) console.warn(`AVISO: el CV supera ${maxPaginas} páginas; recorta logros u otras experiencias.`);
  await browser.close();
  console.log('PDF generado:', path.resolve(salida));
})().catch(err => { console.error(err); process.exit(1); });
