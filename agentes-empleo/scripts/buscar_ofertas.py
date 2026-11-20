#!/usr/bin/env python3
"""Agente Buscador: recorre Computrabajo, Elempleo, Magneto y LinkedIn (ofertas públicas)
y devuelve en JSON las ofertas de nivel directivo en Colombia, con salario y contrato.

Uso:
  python3 buscar_ofertas.py --vistas vistas.txt --salida ofertas.json [--max-detalles 80]

  --vistas  archivo con IDs ya procesados (uno por línea) para no repetir.
Solo usa la biblioteca estándar de Python.
"""
import argparse, html, json, re, sys, time, unicodedata, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
SALARIO_MIN = 9_000_000

CARGOS = [
    "gerente de logistica", "director de logistica", "gerente de operaciones",
    "director de operaciones", "director de transporte", "gerente de transporte",
    "jefe de transporte", "jefe de logistica", "gerente de cadena de abastecimiento",
    "director de cadena de suministro", "gerente de distribucion", "director de proyectos",
    "gerente de supply chain", "director de supply chain", "jefe nacional de logistica",
    "gerente de comercio exterior", "director de operaciones portuarias",
]
LI_KEYWORDS = ["gerente logistica", "director logistica", "gerente operaciones",
               "director operaciones", "director transporte", "supply chain manager",
               "jefe transporte", "director proyectos", "gerente cadena abastecimiento",
               "logistics manager"]
# Fuera de Colombia (David confirmó el 19-nov-2026 que busca en todos los países; requiere visa patrocinada)
LI_KEYWORDS_INTL = ["gerente de logistica", "gerente de operaciones", "logistics manager",
                    "supply chain manager", "operations manager", "director de logistica"]
LI_LOCS_INTL = ["México", "Panamá", "Perú", "Chile", "Ecuador", "República Dominicana", "Costa Rica",
                "Guatemala", "España", "Estados Unidos"]
CT_DEPTOS = ["", "atlantico", "bolivar", "magdalena"]
EE_CIUDADES = ["", "barranquilla", "cartagena", "santa-marta"]

COSTA = ["barranquilla", "cartagena", "santa marta", "soledad", "malambo", "galapa",
         "puerto colombia", "sabanalarga", "cienaga", "riohacha", "valledupar", "monteria",
         "sincelejo", "atlantico", "bolivar", "magdalena", "la guajira", "cesar", "cordoba",
         "sucre", "turbaco", "maicao", "fundacion", "zona bananera", "aracataca", "costa"]

TITULO_SI = re.compile(r"\b(gerente|director|directora|head|manager|jefe|subgerente|vp|vicepresidente|lider|superintendente)\b")
DIRECTIVO = re.compile(r"\b(gerente|director|directora|head|manager|subgerente|vp|vicepresidente|superintendente|jefe nacional|jefe regional)\b")
TITULO_NO = re.compile(r"\b(auxiliar|asistente|aprendiz|practicante|pasante|operari[oa]|conductor|analista|tecnico|tecnologo|ayudante|mensajero|vendedor|asesor|promotor|cajer[oa]|bodeguer[oa]|montacarguista|recepcionista|enfermer[oa]|medic[oa]|docente|profesor|chef|cocin)\b")
AREA_SI = re.compile(r"(logistic|transporte|operacion|supply|cadena|abastecimiento|suministro|distribucion|almacen|bodega|inventario|comercio exterior|puert|portuari|flota|proyecto|planta|produccion|compras|despacho|aduan|carga|cedi|centro de distribucion|ultima milla|fleet)")


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", s).strip()


def slug(s):
    return norm(s).replace(" ", "-")


def get(url, data=None, headers=None, timeout=25):
    h = {"User-Agent": UA, "Accept-Language": "es-CO,es;q=0.9"}
    h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h)
    for intento in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            if e.code in (404, 410) or (e.code == 500 and "magneto365" in url):
                return ""
            if e.code == 429:
                time.sleep(5 * (intento + 1))
                continue
            if intento == 2:
                print(f"[aviso] {url} -> HTTP {e.code}", file=sys.stderr)
                return ""
        except Exception as e:  # red, timeout
            if intento == 2:
                print(f"[aviso] {url} -> {e}", file=sys.stderr)
                return ""
        time.sleep(1.5 * (intento + 1))
    return ""


def texto(h):
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
    h = re.sub(r"<br\s*/?>|</p>|</li>", "\n", h)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h))
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", t)).strip()


def jsonld_jobposting(h):
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', h, re.S):
        try:
            d = json.loads(m.group(1))
        except Exception:
            continue
        for x in (d if isinstance(d, list) else [d]):
            if isinstance(x, dict) and x.get("@type") == "JobPosting":
                return x
    return None


def parse_pesos(s):
    """'$ 9.500.000,00' -> 9500000 ; '$8 a $10 millones' -> (8e6,10e6)"""
    s = norm(s)
    m = re.search(r"\$?\s*([\d.,]+)\s*(?:a|-|y)\s*\$?\s*([\d.,]+)\s*millon", s)
    if m:
        return float(m.group(1).replace(",", ".")) * 1e6, float(m.group(2).replace(",", ".")) * 1e6
    m = re.search(r"\$?\s*([\d.,]+)\s*millon", s)
    if m:
        v = float(m.group(1).replace(",", ".")) * 1e6
        return v, v
    vals = []
    for x in re.findall(r"\$\s*([\d]{1,3}(?:[.,]\d{3})+)(?:,\d{2})?", s):
        vals.append(float(re.sub(r"[.,]", "", x)))
    vals = [v for v in vals if v >= 500_000]
    if vals:
        return min(vals), max(vals)
    return None, None


def contrato_de(t):
    n = norm(t)
    if re.search(r"(termino )?indefinido", n):
        return "indefinido"
    if re.search(r"obra (o|y|u) labor|obra labor", n):
        return "obra o labor"
    if re.search(r"prestacion de servicios", n):
        return "prestacion de servicios"
    if re.search(r"termino fijo|contrato fijo|a termino fijo", n):
        return "termino fijo"
    if re.search(r"temporal", n) and "contrato" in n:
        return "temporal"
    return "no especificado"


NO_PATROCINIO = re.compile(r"(not (be )?(able to )?sponsor|no (visa )?sponsorship|without (the need for )?(visa )?sponsorship|"
    r"must be (legally )?authorized to work|authorized to work in the (us|united states)|u\.?s\.? citizen|"
    r"green card|security clearance|no patrocina|sin patrocinio|residencia (legal|vigente)|permiso de trabajo vigente)")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
EMAIL_IGNORAR = re.compile(r"(computrabajo|elempleo|magneto365|linkedin|sentry|example|wixpress|noreply|no-reply)", re.I)


def correos(t):
    return sorted({e.strip(".") for e in EMAIL_RE.findall(t or "") if not EMAIL_IGNORAR.search(e)})


def titulo_relevante(titulo):
    n = norm(titulo)
    return bool(TITULO_SI.search(n)) and not TITULO_NO.search(n) and bool(AREA_SI.search(n) or "operaciones" in n)


# ---------------------------------------------------------------- Computrabajo
def computrabajo():
    out = {}
    for cargo in CARGOS:
        for d in CT_DEPTOS:
            url = f"https://co.computrabajo.com/trabajo-de-{slug(cargo)}" + (f"-en-{d}" if d else "")
            h = get(url)
            for m in re.finditer(r"<article[^>]*data-id='([^']+)'(.*?)</article>", h, re.S):
                oid, body = m.group(1), m.group(2)
                a = re.search(r'class="js-o-link[^"]*" href="([^"#]+)[^"]*"[^>]*>\s*(.*?)\s*</a>', body, re.S)
                if not a:
                    continue
                titulo = html.unescape(re.sub(r"\s+", " ", a.group(2)))
                emp = re.search(r"offer-grid-article-company-url>\s*(.*?)\s*</a>", body, re.S)
                ciudad = re.search(r'<p class="fs16 fc_base mt5">\s*<span class="mr10">\s*(.*?)\s*</span>', body, re.S)
                sal = re.search(r"i_salary\"></span>\s*(.*?)\s*</span>", body, re.S)
                fecha = re.search(r'<p class="fs13 fc_aux mt15">\s*(.*?)\s*</p>', body, re.S)
                out["ct-" + oid] = dict(
                    id="ct-" + oid, portal="Computrabajo", titulo=titulo,
                    empresa=html.unescape(emp.group(1)).strip() if emp else "Confidencial",
                    ciudad=html.unescape(ciudad.group(1)).strip() if ciudad else "",
                    salario_texto=html.unescape(sal.group(1)).strip() if sal else "",
                    publicada=html.unescape(fecha.group(1)).strip() if fecha else "",
                    url="https://co.computrabajo.com" + a.group(1))
            time.sleep(0.8)
    return out


def computrabajo_detalle(o):
    h = get(o["url"])
    if not h:
        return False
    t = texto(h)
    i = t.find("Descripción de la oferta")
    if i < 0:  # oferta cerrada: Computrabajo redirige al listado
        return False
    cuerpo = t[i:i + 6000]
    j = cuerpo.find("Requerimientos")
    o["descripcion"] = cuerpo[:4000]
    o["contrato"] = contrato_de(cuerpo[:400]) if contrato_de(cuerpo[:400]) != "no especificado" else contrato_de(cuerpo)
    if not o.get("salario_texto"):
        m = re.search(r"\$\s?[\d.,]+[^()]*\((Mensual)\)", cuerpo)
        o["salario_texto"] = m.group(0) if m else ""
    o["correos"] = correos(cuerpo)
    return True


# ---------------------------------------------------------------- Elempleo
def elempleo():
    out = {}
    for cargo in CARGOS:
        for c in EE_CIUDADES:
            url = "https://www.elempleo.com/co/ofertas-empleo/" + (f"{c}/" if c else "") + f"trabajo-{slug(cargo)}"
            h = get(url)
            for m in re.finditer(r'"@id":\s*"(https://www\.elempleo\.com/co/ofertas-trabajo/[^"]+-(\d+))",\s*"@type":\s*"WebPage",\s*"name":\s*"([^"]+)"', h):
                out["ee-" + m.group(2)] = dict(id="ee-" + m.group(2), portal="Elempleo",
                                               titulo=html.unescape(m.group(3)), url=m.group(1))
            time.sleep(0.8)
    return out


def elempleo_detalle(o):
    h = get(o["url"])
    if not h:
        return False
    jp = jsonld_jobposting(h) or {}
    t = texto(h)
    o["empresa"] = (jp.get("hiringOrganization") or {}).get("name", "") or "Confidencial"
    if o["empresa"].upper() == "CONFIDENTIAL":
        o["empresa"] = "Confidencial"
    addr = ((jp.get("jobLocation") or {}).get("address") or {})
    o["ciudad"] = ", ".join(x for x in [addr.get("addressRegion"), addr.get("addressLocality")] if x)
    o["publicada"] = jp.get("datePosted", "")
    o["vence"] = jp.get("validThrough", "")
    bs = ((jp.get("baseSalary") or {}).get("value") or {})
    if bs.get("minValue") or bs.get("maxValue"):
        o["salario_min"], o["salario_max"] = bs.get("minValue"), bs.get("maxValue")
        o["salario_texto"] = f"${bs.get('minValue', 0):,.0f} - ${bs.get('maxValue', 0):,.0f}".replace(",", ".")
    else:
        m = re.search(r"\$[\d.,]+\s*a\s*\$[\d.,]+\s*millones|\$[\d.,]+\s*millones|Salario confidencial|A convenir", t)
        o["salario_texto"] = m.group(0) if m else ""
    m = re.search(r"(Indefinido|Fijo|Obra o labor|Prestación de servicios|Temporal|Aprendizaje)\s+Tipo de contrato", t)
    o["contrato"] = norm(m.group(1)) if m else contrato_de(t)
    desc = texto(jp.get("description", "")) if jp.get("description") else ""
    o["descripcion"] = desc[:4000]
    o["correos"] = correos(desc)
    return True


# ---------------------------------------------------------------- Magneto
def magneto():
    out = {}
    for cargo in CARGOS:
        url = f"https://www.magneto365.com/co/trabajos/ofertas-empleo-de-{slug(cargo).replace('-de-', '-', 1)}"
        h = get(url)
        for u in dict.fromkeys(re.findall(r'href="(https://www\.magneto365\.com/co/empleos/[^"]+-(\d+))"', h)):
            oid = u[1]
            tit = u[0].rsplit("/", 1)[-1].rsplit("-", 1)[0].replace("-", " ")
            out["mg-" + oid] = dict(id="mg-" + oid, portal="Magneto", titulo=tit, url=u[0])
        time.sleep(0.8)
    return out


def magneto_detalle(o):
    h = get(o["url"])
    if not h:
        return False
    t = texto(h)
    m = re.search(r"<title>\s*Empleo como (.*?) en (.*?)\s*\|\s*Magneto", h, re.S)
    if m:
        o["titulo"] = html.unescape(m.group(1)).strip()
        o["empresa"] = html.unescape(m.group(2)).strip() or "Confidencial"
    i = t.find("Requisitos para aplicar a la vacante")
    cab = t[max(0, i - 400):i]
    m = re.search(r"\|\s*(Término indefinido|Término fijo|Temporal|Por obra o labor|Prestación de servicios|Contrato de aprendizaje)", cab)
    o["contrato"] = contrato_de(m.group(1)) if m else contrato_de(t)
    if m and "obra" in m.group(1).lower():
        o["contrato"] = "obra o labor"
    m = re.search(r"Fecha de publicación\s*(\d{4}-\d{2}-\d{2})", cab)
    o["publicada"] = m.group(1) if m else ""
    lineas = [l.strip() for l in t[i:i + 6000].split("\n") if l.strip()]
    # Estructura: Requisitos... / experiencia y estudios / salario / ciudad / descripción
    sal_idx = next((k for k, l in enumerate(lineas[:6]) if l.startswith("$") or "convenir" in l.lower() or "salario" in l.lower()), None)
    o["salario_texto"] = lineas[sal_idx] if sal_idx is not None else ""
    o["ciudad"] = lineas[sal_idx + 1] if sal_idx is not None and sal_idx + 1 < len(lineas) else ""
    desc = "\n".join(lineas[(sal_idx + 2) if sal_idx is not None else 1:])
    o["requisitos"] = lineas[1] if len(lineas) > 1 else ""
    o["descripcion"] = desc[:4000]
    o["correos"] = correos(desc)
    return True


# ---------------------------------------------------------------- LinkedIn (ofertas públicas, sin iniciar sesión)
def linkedin():
    out = {}
    pares = [(kw, loc) for kw in LI_KEYWORDS
             for loc in ["Colombia", "Barranquilla, Atlántico, Colombia", "Cartagena, Bolívar, Colombia", "Santa Marta, Magdalena, Colombia"]]
    pares += [(kw, loc) for kw in LI_KEYWORDS_INTL for loc in LI_LOCS_INTL]
    for kw, loc in pares:
        if True:
            q = urllib.parse.urlencode({"keywords": kw, "location": loc, "f_TPR": "r1209600", "start": 0})
            h = get("https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?" + q)
            for c in re.findall(r'<div class="base-card.*?</li>', h, re.S) or re.findall(r"<li>.*?</li>", h, re.S):
                href = re.search(r'href="(https://[a-z]+\.linkedin\.com/jobs/view/[^"?]*?-(\d+))[?"]', c)
                if not href:
                    continue
                oid = href.group(2)
                tit = re.search(r'base-search-card__title[^>]*>\s*(.*?)\s*</h3>', c, re.S)
                emp = re.search(r'base-search-card__subtitle[^>]*>.*?(?:<a[^>]*>)?\s*([^<]+?)\s*(?:</a>)?\s*</h4>', c, re.S)
                ciu = re.search(r'job-search-card__location[^>]*>\s*(.*?)\s*</span>', c, re.S)
                fec = re.search(r'<time[^>]*datetime="([^"]+)"', c)
                out["li-" + oid] = dict(id="li-" + oid, portal="LinkedIn",
                                        titulo=html.unescape(tit.group(1)).strip() if tit else "",
                                        empresa=html.unescape(emp.group(1)).strip() if emp else "",
                                        ciudad=html.unescape(ciu.group(1)).strip() if ciu else "",
                                        publicada=fec.group(1) if fec else "",
                                        url=f"https://www.linkedin.com/jobs/view/{oid}")
            time.sleep(2)
    return out


def linkedin_detalle(o):
    oid = o["id"].split("-", 1)[1]
    h = get(f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{oid}")
    if not h:
        return False
    d = re.search(r'show-more-less-html__markup[^>]*>(.*?)</div>', h, re.S)
    desc = texto(d.group(1)) if d else texto(h)[:4000]
    o["descripcion"] = desc[:4000]
    crit = texto(" ".join(re.findall(r'description__job-criteria-item.*?</li>', h, re.S)))
    o["criterios"] = re.sub(r"\s+", " ", crit)[:300]
    o["contrato"] = contrato_de(desc)
    m = re.search(r"\$\s?[\d.,]+(?:\s*(?:a|-)\s*\$\s?[\d.,]+)?(?:\s*millones)?|[\d.,]+\s*millones", desc)
    o["salario_texto"] = m.group(0) if m else ""
    o["correos"] = correos(desc)
    o["aplicantes"] = (re.search(r"(Over \d+ applicants|\d+ applicants|Más de \d+ solicitudes|\d+ solicitudes)", texto(h)) or [None])[0] if re.search(r"applicants|solicitudes", h) else ""
    return True


DETALLE = {"Computrabajo": computrabajo_detalle, "Elempleo": elempleo_detalle,
           "Magneto": magneto_detalle, "LinkedIn": linkedin_detalle}


def clasificar(o):
    if o.get("salario_min") is None and o.get("salario_max") is None:
        mn, mx = parse_pesos(o.get("salario_texto", ""))
        o["salario_min"], o["salario_max"] = mn, mx
    mx = o.get("salario_max")
    if mx is None:
        o["salario_estado"] = "no publicado"
    elif mx >= SALARIO_MIN:
        o["salario_estado"] = "cumple"
    else:
        o["salario_estado"] = "bajo"
    c = o.get("contrato", "no especificado")
    o["contrato_estado"] = "cumple" if c == "indefinido" else ("confirmar" if c == "no especificado" else "no cumple")
    o["costa_norte"] = any(k in norm(o.get("ciudad", "") + " " + o.get("titulo", "")) for k in COSTA)
    ciudad_n = norm(o.get("ciudad", ""))
    o["fuera_de_colombia"] = o.get("portal") == "LinkedIn" and bool(ciudad_n) and "colombia" not in ciudad_n
    motivo_ext = ""
    if o["fuera_de_colombia"]:
        desc_n = norm(o.get("descripcion", ""))
        if re.search(r"\b(brasil|brazil)\b", ciudad_n):
            motivo_ext = "Brasil: exige portugués"
        elif NO_PATROCINIO.search(desc_n):
            motivo_ext = "no patrocina visa / exige autorización de trabajo vigente"
    sin_salario_no_directivo = o["salario_estado"] == "no publicado" and not DIRECTIVO.search(norm(o.get("titulo", "")))
    if o.get("fuera_de_colombia") and o["contrato_estado"] == "confirmar":
        o["contrato_estado"] = "confirmar"  # en el exterior el contrato rara vez se publica
    o["descartada"] = o["salario_estado"] == "bajo" or o["contrato_estado"] == "no cumple" or sin_salario_no_directivo or bool(motivo_ext)
    o["motivo_descarte"] = ", ".join(x for x in [
        f"salario {o.get('salario_texto')}" if o["salario_estado"] == "bajo" else "",
        f"contrato {c}" if o["contrato_estado"] == "no cumple" else "",
        "cargo no directivo sin salario publicado" if sin_salario_no_directivo else "",
        motivo_ext] if x)
    return o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vistas", default="")
    ap.add_argument("--salida", default="ofertas.json")
    ap.add_argument("--max-detalles", type=int, default=100)
    ap.add_argument("--portales", default="Computrabajo,Elempleo,Magneto,LinkedIn")
    a = ap.parse_args()
    vistas = set()
    if a.vistas:
        try:
            vistas = {l.strip() for l in open(a.vistas) if l.strip()}
        except FileNotFoundError:
            pass
    portales = a.portales.split(",")
    fuentes = [(n, fn) for n, fn in [("Computrabajo", computrabajo), ("Elempleo", elempleo),
                                     ("Magneto", magneto), ("LinkedIn", linkedin)] if n in portales]
    todas = {}
    # Un hilo por portal: los portales se consultan en paralelo, pero cada uno con pausas entre solicitudes.
    with ThreadPoolExecutor(max_workers=len(fuentes) or 1) as ex:
        for (nombre, _), r in zip(fuentes, ex.map(lambda f: f[1](), fuentes)):
            print(f"[{nombre}] {len(r)} ofertas en listados", file=sys.stderr, flush=True)
            todas.update(r)
    def salario_listado_bajo(o):
        mn, mx = parse_pesos(o.get("salario_texto", ""))
        return mx is not None and mx < SALARIO_MIN
    candidatas = [o for k, o in todas.items() if k not in vistas and titulo_relevante(o.get("titulo", ""))
                  and not salario_listado_bajo(o)]
    # Prioriza Costa Norte primero para los detalles
    def es_ext(o):
        c = norm(o.get("ciudad", ""))
        return o.get("portal") == "LinkedIn" and bool(c) and "colombia" not in c
    candidatas.sort(key=lambda o: (es_ext(o), not any(k in norm(o.get("ciudad", "") + " " + o["titulo"]) for k in COSTA)))
    nac = [o for o in candidatas if not es_ext(o)]
    ext = [o for o in candidatas if es_ext(o) and not re.search(r"\b(brasil|brazil)\b", norm(o.get("ciudad", "")))][:40]
    candidatas = (nac + ext)[: a.max_detalles]
    print(f"[filtro] {len(candidatas)} nuevas con cargo directivo relevante (se revisan en detalle)", file=sys.stderr, flush=True)

    def detalles_de(portal):
        hechas = []
        for o in [c for c in candidatas if c["portal"] == portal]:
            try:
                ok = DETALLE[portal](o)
            except Exception as ex_:
                print(f"[aviso] detalle {o['id']}: {ex_}", file=sys.stderr)
                ok = False
            time.sleep(1.0 if portal != "LinkedIn" else 2.0)
            if ok and titulo_relevante(o.get("titulo", "")):
                hechas.append(clasificar(o))
        return hechas

    res = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        for r in ex.map(detalles_de, [n for n, _ in fuentes]):
            res.extend(r)
    validas = [o for o in res if not o["descartada"]]
    validas.sort(key=lambda o: (not o["costa_norte"], o.get("fuera_de_colombia", False), o["salario_estado"] != "cumple", o["contrato_estado"] != "cumple"))
    salida = dict(generado=datetime.now(timezone.utc).isoformat(), total_listados=len(todas),
                  candidatas_nuevas=len(candidatas), revisadas=len(res),
                  ids_procesados=sorted({o["id"] for o in res} | {o["id"] for o in candidatas}),
                  descartadas=[{k: o.get(k) for k in ("id", "titulo", "empresa", "motivo_descarte")} for o in res if o["descartada"]],
                  ofertas=validas)
    json.dump(salida, open(a.salida, "w"), ensure_ascii=False, indent=1)
    print(f"[resultado] {len(validas)} ofertas válidas, {len(res) - len(validas)} descartadas -> {a.salida}", file=sys.stderr)


if __name__ == "__main__":
    main()
