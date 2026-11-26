#!/usr/bin/env python3
"""Agente Remoto: recorre portales de trabajo remoto con datos públicos (API o RSS) y LinkedIn
(ofertas públicas con filtro «remoto») y devuelve en JSON las ofertas remotas de logística,
operaciones, supply chain, compras, proyectos y afines que se pueden hacer desde Colombia.

Uso:
  python3 buscar_remoto.py --vistas vistas_remoto.txt --salida remoto.json [--usd-cop 4000]

  --vistas   archivo con IDs ya procesados (uno por línea) para no repetir.
  --usd-cop  tasa del día para convertir salarios (búscala antes de correr).
Solo usa la biblioteca estándar de Python. Cada portal se consulta una vez por ejecución
(respeta los límites de uso y da crédito a la fuente con el enlace original).
"""
import argparse, hashlib, html, json, os, re, sys, time, urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import buscar_ofertas as b  # get(), texto(), norm(), linkedin_detalle()

SAL_MIN_COP = 9_000_000

AREA = re.compile(
    r"(logistic|logistica|supply chain|cadena de (abastecimiento|suministro)|operations|operaciones|procurement|"
    r"purchasing|sourcing|buyer|compras|abastecimiento|transport|fleet|flota|warehouse|almacen|distribution|"
    r"distribucion|fulfil|inventory|inventario|demand plann|supply plann|planeacion|s&op|freight|dispatch|despacho|"
    r"carrier|last mile|ultima milla|import|export|comercio exterior|customs|aduan|project manager|program manager|"
    r"gerente de proyectos|director de proyectos|pmo|continuous improvement|mejora continua|lean|six sigma|"
    r"process improvement|excelencia operacional|industrial engineer|ingenier[oa] industrial|"
    r"customer success|customer experience|servicio al cliente|account manager|key account|cuentas clave|"
    r"business operations|general manager|country manager|gerente general)")
NO = re.compile(
    r"(software|developer|desarrollador|devops|front.?end|back.?end|full.?stack|data engineer|data scien|machine learning|"
    r"\bml\b|\bai engineer|qa engineer|sre\b|site reliability|security engineer|network engineer|cloud|nurse|"
    r"enfermer|teacher|tutor|docente|designer|disenador|copywriter|recruiter|reclutador|intern\b|pasant|"
    r"practicante|sales development|\bsdr\b|\bbdr\b|marketing|seo\b|content|video|editor|accountant|contador|"
    r"bookkeep|legal|attorney|paralegal|medical|clinical|therap|pharm|revops|revenue operations|salesforce)")
SENIOR = re.compile(r"(manager|gerente|director|head|lead|lider|jefe|senior|sr\.?|principal|coordinator|coordinador|specialist|especialista)")

LATAM = re.compile(r"(colombia|latam|latin america|latinoamerica|south america|sudamerica|americas|lat am|"
                   r"worldwide|anywhere|global|world|remote \(any|todo el mundo|cualquier pais)")


def oid(prefijo, clave):
    return f"{prefijo}-{hashlib.sha1(str(clave).encode()).hexdigest()[:10]}"


def elegibilidad(ubic):
    n = b.norm(ubic or "")
    if not n.strip():
        return "desconocida"
    if "colombia" in n:
        return "colombia"
    if LATAM.search(n):
        return "latam_o_mundial"
    if re.fullmatch(r"\s*(remote|remoto)\W*(\(.*\))?\s*", n):
        return "desconocida"
    return "no_elegible"  # nombra otro país o región (EE. UU., Europa, México, Pakistán...)


def salario_usd_mes(txt, minimo=None, maximo=None, periodo=""):
    """Devuelve (min, max) en USD al mes, o (None, None)."""
    vals = []
    if minimo or maximo:
        vals = [v for v in (minimo, maximo) if v]
    elif txt:
        t = txt.lower().replace(",", "")
        for m in re.finditer(r"\$?\s?(\d+(?:\.\d+)?)\s*(k)?", t):
            v = float(m.group(1)) * (1000 if m.group(2) else 1)
            if v >= 10:
                vals.append(v)
        if "hour" in t or "hora" in t or "/hr" in t:
            periodo = "hour"
        elif "month" in t or "mes" in t:
            periodo = "month"
        elif vals:
            periodo = "year" if max(vals) > 15000 else "month"
    if not vals:
        return None, None
    f = {"hour": 160, "hourly": 160, "month": 1, "monthly": 1}.get(str(periodo).lower(), 1 / 12)
    return round(min(vals) * f), round(max(vals) * f)


REMOTO = re.compile(r"(remoto|remote|teletrabajo|trabajo desde casa|home office|work from home|wfh|100% virtual|anywhere)")


def relevante(titulo):
    n = b.norm(titulo)
    if re.search(r"\bengineer", n) and "industrial" not in n:
        return False
    return bool(AREA.search(n)) and not NO.search(n) and not re.search(r"(security|graduate|trainee|junior|\bjr\b)", n)


def base(id_, fuente, titulo, empresa, ubic, url, fecha="", tipo="", sal_txt="", smin=None, smax=None, desc=""):
    e = elegibilidad(ubic)
    return dict(id=id_, portal=fuente, titulo=html.unescape(titulo or "").strip(), empresa=html.unescape(empresa or "").strip(),
                ciudad="Remoto", ubicacion_permitida=(ubic or "").strip()[:200], elegibilidad=e, url=url,
                publicada=fecha, tipo=tipo, salario_texto=sal_txt or "", salario_usd_mes_min=smin, salario_usd_mes_max=smax,
                descripcion=b.texto(desc or "")[:3000], modalidad="remoto")


def remotive():
    d = json.loads(b.get("https://remotive.com/api/remote-jobs") or "{}")
    out = []
    for j in d.get("jobs", []):
        smin, smax = salario_usd_mes(j.get("salary", ""))
        out.append(base(f"rmt-{j['id']}", "Remotive", j.get("title"), j.get("company_name"), j.get("candidate_required_location"),
                        j.get("url"), j.get("publication_date", ""), j.get("job_type", ""), j.get("salary", ""), smin, smax, j.get("description", "")))
    return out


def remoteok():
    d = json.loads(b.get("https://remoteok.com/api") or "[]")
    out = []
    for j in d[1:] if isinstance(d, list) else []:
        smin, smax = salario_usd_mes("", j.get("salary_min"), j.get("salary_max"), "year")
        out.append(base(f"rok-{j.get('id')}", "Remote OK", j.get("position"), j.get("company"), j.get("location") or "Worldwide",
                        j.get("url") or f"https://remoteok.com/remote-jobs/{j.get('slug')}", j.get("date", ""), "",
                        f"USD {j.get('salary_min')}-{j.get('salary_max')}/año" if j.get("salary_min") else "", smin, smax, j.get("description", "")))
    return out


def weworkremotely():
    x = b.get("https://weworkremotely.com/remote-jobs.rss")
    out = []
    try:
        root = ET.fromstring(x)
    except Exception:
        return out
    for it in root.iter("item"):
        g = lambda k: (it.findtext(k) or "").strip()
        tit = g("title")
        emp, _, cargo = tit.partition(": ")
        out.append(base(oid("wwr", g("link")), "We Work Remotely", cargo or tit, emp if cargo else "", g("region") or g("country"),
                        g("link"), g("pubDate"), g("type"), "", None, None, html.unescape(g("description"))))
    return out


def himalayas(paginas=5):
    out = []
    for p in range(paginas):
        h = b.get(f"https://himalayas.app/jobs/api?limit=20&offset={p * 20}")
        try:
            d = json.loads(h or "{}")
        except Exception:
            break
        for j in d.get("jobs", []):
            smin, smax = salario_usd_mes("", j.get("minSalary"), j.get("maxSalary"), j.get("salaryPeriod", "annual").replace("annual", "year"))
            ubic = ", ".join(j.get("locationRestrictions") or []) or "Worldwide"
            out.append(base(oid("him", j.get("applicationLink") or j.get("guid") or j.get("title")), "Himalayas", j.get("title"), j.get("companyName"),
                            ubic, j.get("applicationLink") or j.get("guid", ""), str(j.get("pubDate", "")), j.get("employmentType", ""),
                            f"{j.get('currency', '')} {j.get('minSalary')}-{j.get('maxSalary')} ({j.get('salaryPeriod')})" if j.get("minSalary") else "",
                            smin, smax, j.get("description") or j.get("excerpt", "")))
        time.sleep(3)
    return out


def jobicy():
    out = []
    for geo in ("latam", "anywhere"):
        d = json.loads(b.get(f"https://jobicy.com/api/v2/remote-jobs?count=100&geo={geo}") or "{}")
        for j in d.get("jobs", []):
            smin, smax = salario_usd_mes("", j.get("salaryMin") or j.get("annualSalaryMin"), j.get("salaryMax") or j.get("annualSalaryMax"),
                                         j.get("salaryPeriod", "year").replace("yearly", "year").replace("annual", "year"))
            out.append(base(f"jcy-{j.get('id')}", "Jobicy", j.get("jobTitle"), j.get("companyName"), j.get("jobGeo"), j.get("url"),
                            j.get("pubDate", ""), ", ".join(j.get("jobType") or []), "", smin, smax, j.get("jobDescription") or j.get("jobExcerpt", "")))
        time.sleep(2)
    return out


def getonbrd():
    out = []
    for q in ("logistica", "operaciones", "supply chain", "compras", "proyectos", "abastecimiento", "customer success"):
        d = json.loads(b.get("https://www.getonbrd.com/api/v0/search/jobs?" + urllib.parse.urlencode({"query": q, "per_page": 50, "expand": '["company"]'})) or "{}")
        for j in d.get("data", []):
            a = j.get("attributes", {})
            if not a.get("remote"):
                continue
            paises = ", ".join(a.get("countries") or []) or ("Remote (" + str(a.get("remote_modality", "")) + ")")
            comp = ((a.get("company") or {}).get("data") or {}).get("attributes", {}).get("name", "")
            smin, smax = salario_usd_mes("", a.get("min_salary"), a.get("max_salary"), "month")
            out.append(base(f"gob-{j.get('id')}", "Get on Board", a.get("title"), comp, paises, f"https://www.getonbrd.com/jobs/{j.get('id')}",
                            str(a.get("published_at", "")), str(a.get("modality", "")),
                            f"USD {a.get('min_salary')}-{a.get('max_salary')}/mes" if a.get("min_salary") else "", smin, smax,
                            (a.get("description") or "") + " " + (a.get("functions") or "")))
        time.sleep(2)
    return out


def workingnomads():
    d = json.loads(b.get("https://www.workingnomads.com/api/exposed_jobs/") or "[]")
    return [base(oid("wn", j.get("url")), "Working Nomads", j.get("title"), j.get("company_name"), j.get("location") or "",
                 j.get("url"), j.get("pub_date", ""), "", "", None, None, j.get("description", "")) for j in d]


def linkedin_remoto():
    out = []
    kws = ["logistics manager", "supply chain manager", "operations manager", "procurement manager", "gerente de logistica",
           "gerente de operaciones", "project manager logistics", "transportation manager", "director de operaciones"]
    for kw in kws:
        for loc in ("Colombia", "Latin America"):
            q = urllib.parse.urlencode({"keywords": kw, "location": loc, "f_WT": "2", "f_TPR": "r604800", "start": 0})
            h = b.get("https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?" + q) or ""
            for c in re.findall(r'<div class="base-card.*?</li>', h, re.S) or re.findall(r"<li>.*?</li>", h, re.S):
                href = re.search(r'href="(https://[a-z]+\.linkedin\.com/jobs/view/[^"?]*?-(\d+))[?"]', c)
                if not href:
                    continue
                tit = re.search(r'base-search-card__title[^>]*>\s*(.*?)\s*</h3>', c, re.S)
                emp = re.search(r'base-search-card__subtitle[^>]*>.*?(?:<a[^>]*>)?\s*([^<]+?)\s*(?:</a>)?\s*</h4>', c, re.S)
                ciu = re.search(r'job-search-card__location[^>]*>\s*(.*?)\s*</span>', c, re.S)
                fec = re.search(r'<time[^>]*datetime="([^"]+)"', c)
                o = base("li-" + href.group(2), "LinkedIn (remoto)", tit.group(1) if tit else "", emp.group(1) if emp else "",
                         (ciu.group(1) if ciu else loc), f"https://www.linkedin.com/jobs/view/{href.group(2)}", fec.group(1) if fec else "")
                if o["elegibilidad"] in ("desconocida", "no_elegible"):
                    # la ciudad es donde se publicó; si es remoto, el agente confirma desde qué países contrata
                    o["elegibilidad"] = "colombia" if loc == "Colombia" else "desconocida"
                out.append(o)
            time.sleep(2)
    return out


FUENTES = [remotive, remoteok, weworkremotely, himalayas, jobicy, getonbrd, workingnomads, linkedin_remoto]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vistas", default="")
    ap.add_argument("--salida", required=True)
    ap.add_argument("--usd-cop", type=float, default=4000)
    a = ap.parse_args()
    vistas = set(open(a.vistas).read().split()) if a.vistas and os.path.exists(a.vistas) else set()
    todas, estado = {}, {}
    for f in FUENTES:
        try:
            r = f()
            estado[f.__name__] = len(r)
            for o in r:
                todas.setdefault(o["id"], o)
        except Exception as e:  # un portal caído no detiene la búsqueda
            estado[f.__name__] = f"error: {e}"[:200]
        print(f.__name__, estado[f.__name__], file=sys.stderr)
    sel = []
    for o in todas.values():
        if o["id"] in vistas or not o["titulo"] or not relevante(o["titulo"]) or o["elegibilidad"] == "no_elegible":
            continue
        if o["portal"] == "LinkedIn (remoto)":
            # el filtro «remoto» de LinkedIn sin sesión no es confiable: se exige que el aviso diga que es remoto
            try:
                b.linkedin_detalle(o)
                time.sleep(1)
            except Exception:
                pass
            txt = b.norm(o["titulo"] + " " + o.get("descripcion", "") + " " + o.get("criterios", ""))
            if not REMOTO.search(txt) or re.search(r"(hibrido|hybrid|presencial|on-site|onsite)", b.norm(o["titulo"])):
                continue
        o["nivel"] = "directivo_o_senior" if SENIOR.search(b.norm(o["titulo"])) else "otro"
        mx = o.get("salario_usd_mes_max")
        o["salario_cop_mes_max"] = round(mx * a.usd_cop) if mx else None
        o["cumple_salario"] = (o["salario_cop_mes_max"] >= SAL_MIN_COP) if mx else None
        sel.append(o)
    sel.sort(key=lambda o: (o["elegibilidad"] != "colombia", o["elegibilidad"] != "latam_o_mundial", o["nivel"] != "directivo_o_senior"))
    json.dump(dict(fecha=datetime.now(timezone.utc).isoformat(), usd_cop=a.usd_cop, fuentes=estado,
                   total_revisadas=len(todas), ofertas=sel), open(a.salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if a.vistas:
        with open(a.vistas, "a") as fh:
            for i in todas:
                if i not in vistas:
                    fh.write(i + "\n")
    print(f"revisadas {len(todas)} · relevantes nuevas {len(sel)}", file=sys.stderr)


if __name__ == "__main__":
    main()
