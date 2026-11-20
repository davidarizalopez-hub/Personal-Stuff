#!/usr/bin/env node
// Genera una carta de presentación (PDF de una página, texto seleccionable) a partir de un JSON.
// Uso: node generar_carta.js carta.json salida.pdf
// Misma línea visual del CV ATS: una columna, fuente estándar, sin imágenes ni tablas.
// Estructura del JSON: ver ejemplos/carta_ejemplo.json.
// Requiere Playwright con Chromium (preinstalado en las sesiones en la nube).
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const [, , entrada, salida] = process.argv;
if (!entrada || !salida) { console.error('Uso: node generar_carta.js carta.json salida.pdf'); process.exit(1); }
const k = JSON.parse(fs.readFileSync(entrada, 'utf8'));
const e = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const b = (s) => e(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
const ingles = (k.idioma || 'es') === 'en';

const c = k.contacto || {};
const contacto = [c.telefono, c.email, c.linkedin, c.ubicacion].filter(Boolean).map(e).join(' | ');
const parrafos = (xs) => (xs || []).map(p => `<p>${b(p)}</p>`).join('');

const html = `<!doctype html><html lang="${ingles ? 'en' : 'es'}"><head><meta charset="utf-8">
<title>${e(k.nombre)} - ${ingles ? 'Cover letter' : 'Carta de presentación'}</title>
<style>
  @page { size: A4; margin: 20mm 22mm 18mm 22mm; }
  body { font-family: "Liberation Sans", Arial, Helvetica, sans-serif; color: #000; font-size: 10.8pt; line-height: 1.42; margin: 0; }
  h1 { font-size: 16pt; margin: 0 0 1px; font-weight: 700; }
  .titulo { font-size: 10.5pt; margin: 0 0 2px; }
  .contacto { font-size: 9.8pt; margin: 0 0 4px; padding-bottom: 6px; border-bottom: 1px solid #000; }
  .fecha { margin: 14px 0 12px; }
  .dest p { margin: 0; }
  .ref { margin: 12px 0 12px; font-weight: 700; }
  p { margin: 0 0 9px; text-align: justify; }
  ul { margin: 0 0 9px 0; padding-left: 18px; }
  li { margin: 0 0 4px; text-align: justify; }
  .firma { margin-top: 18px; }
  .firma p { margin: 0; text-align: left; }
</style></head><body>
<h1>${e(k.nombre)}</h1>
${k.titulo_profesional ? `<p class="titulo">${e(k.titulo_profesional)}</p>` : ''}
<p class="contacto">${contacto}</p>

<p class="fecha">${e(k.lugar_fecha)}</p>
<div class="dest">${(k.destinatario || []).map(x => `<p>${e(x)}</p>`).join('')}</div>
${k.referencia ? `<p class="ref">${ingles ? 'Re' : 'Referencia'}: ${e(k.referencia)}</p>` : ''}

<p>${e(k.saludo)}</p>
${parrafos(k.parrafos)}
${(k.vinetas || []).length ? `${k.vinetas_titulo ? `<p>${b(k.vinetas_titulo)}</p>` : ''}<ul>${k.vinetas.map(v => `<li>${b(v)}</li>`).join('')}</ul>` : ''}
${parrafos(k.parrafos_finales)}

<div class="firma">
  <p>${e(k.despedida || (ingles ? 'Sincerely,' : 'Cordialmente,'))}</p>
  <p style="margin-top:22px"><strong>${e(k.nombre)}</strong></p>
  ${k.titulo_profesional ? `<p>${e(k.titulo_profesional)}</p>` : ''}
  <p>${[c.telefono, c.email].filter(Boolean).map(e).join(' | ')}</p>
</div>
</body></html>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'load' });
  // La carta debe caber en una página: reduce la escala hasta 0.85 si hace falta.
  let escala = 1, buf, paginas;
  for (;;) {
    buf = await page.pdf({ format: 'A4', printBackground: false, preferCSSPageSize: true, scale: escala, tagged: true });
    paginas = (buf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
    if (paginas <= 1 || escala <= 0.85) break;
    escala = Math.round((escala - 0.03) * 100) / 100;
  }
  fs.writeFileSync(salida, buf);
  const palabras = [k.saludo, ...(k.parrafos || []), k.vinetas_titulo, ...(k.vinetas || []), ...(k.parrafos_finales || [])]
    .filter(Boolean).join(' ').split(/\s+/).length;
  console.log(`Páginas: ${paginas} (escala ${escala}) · ${palabras} palabras en el cuerpo`);
  if (paginas > 1) console.warn('AVISO: la carta supera una página; acórtala (meta: 250 a 380 palabras).');
  await browser.close();
  console.log('PDF generado:', path.resolve(salida));
})().catch(err => { console.error(err); process.exit(1); });
