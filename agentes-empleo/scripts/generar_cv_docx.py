#!/usr/bin/env python3
"""Genera la versión Word (.docx) del CV en formato ATS a partir del mismo JSON que generar_cv.js.

Uso: python3 generar_cv_docx.py cv.json salida.docx
Una sola columna, sin tablas, sin encabezados/pies de página, fuente Arial, estilos estándar de Word.
Requiere python-docx (pip install python-docx).
"""
import json
import re
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt


def texto_con_negritas(parrafo, texto):
    """Escribe el texto respetando **negritas**."""
    partes = re.split(r"(\*\*.+?\*\*)", texto or "")
    for p in partes:
        if not p:
            continue
        run = parrafo.add_run(p[2:-2] if p.startswith("**") else p)
        run.bold = p.startswith("**")


def lista(x):
    return ", ".join(x) if isinstance(x, list) else (x or "")


def main():
    entrada, salida = sys.argv[1], sys.argv[2]
    cv = json.load(open(entrada, encoding="utf-8"))
    doc = Document()
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Cm(1.6)
        s.left_margin = s.right_margin = Cm(1.8)
    base = doc.styles["Normal"]
    base.font.name = "Arial"
    base.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    base.font.size = Pt(10.5)
    base.paragraph_format.space_after = Pt(2)

    def titulo_seccion(t):
        h = doc.add_heading(t.upper(), level=2)
        for r in h.runs:
            r.font.name = "Arial"
            r.font.size = Pt(11)
            r.font.bold = True
            r.font.color.rgb = None
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(3)

    def vineta(t):
        p = doc.add_paragraph(style="List Bullet")
        texto_con_negritas(p, t)
        p.paragraph_format.space_after = Pt(1)

    en = cv.get("idioma") == "en"
    L = dict(tel="Phone", mail="Email", ubi="Location", doc="Resume", perfil="Professional Summary", logros="Key Achievements",
             comp="Core Competencies", exp="Professional Experience", otras="Other Experience", edu="Education",
             hab="Technical Skills", herr="Tools", met="Methodologies", idi="Languages", info="Additional Information") if en else \
        dict(tel="Teléfono", mail="Correo", ubi="Ubicación", doc="Hoja de vida", perfil="Perfil profesional", logros="Logros destacados",
             comp="Competencias clave", exp="Experiencia laboral", otras="Otras experiencias", edu="Educación",
             hab="Habilidades técnicas", herr="Herramientas", met="Metodologías", idi="Idiomas", info="Información adicional")

    h = doc.add_heading(cv["nombre"], level=1)
    for r in h.runs:
        r.font.name = "Arial"
        r.font.size = Pt(18)
        r.font.color.rgb = None
    h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p = doc.add_paragraph()
    r = p.add_run(cv.get("titular", ""))
    r.bold = True
    c = cv.get("contacto", {})
    contacto = " | ".join(x for x in [
        c.get("telefono") and f"{L['tel']}: {c['telefono']}",
        c.get("email") and f"{L['mail']}: {c['email']}",
        c.get("linkedin") and f"LinkedIn: {c['linkedin']}",
        c.get("ubicacion") and f"{L['ubi']}: {c['ubicacion']}"] if x)
    doc.add_paragraph(contacto)

    titulo_seccion(L["perfil"])
    texto_con_negritas(doc.add_paragraph(), cv.get("perfil", ""))

    if cv.get("logros_clave"):
        titulo_seccion(L["logros"])
        for l in cv["logros_clave"]:
            vineta(l)

    if cv.get("competencias"):
        titulo_seccion(L["comp"])
        doc.add_paragraph(lista(cv["competencias"]))

    titulo_seccion(L["exp"])
    for x in cv.get("experiencia", []):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(5)
        r = p.add_run(f"{x['cargo']} | {x['fechas']}")
        r.bold = True
        doc.add_paragraph(x["empresa"] + (f", {x['lugar']}" if x.get("lugar") else ""))
        if x.get("resumen"):
            texto_con_negritas(doc.add_paragraph(), x["resumen"])
        for l in x.get("logros", []):
            vineta(l)

    if cv.get("otras_experiencias"):
        titulo_seccion(L["otras"])
        for x in cv["otras_experiencias"]:
            vineta(f"**{x['cargo']}** | {x['empresa']} | {x['fechas']}")

    titulo_seccion(L["edu"])
    for x in cv.get("educacion", []):
        vineta(f"**{x['titulo']}** | {x['institucion']} | {x['anio']}")

    titulo_seccion(L["hab"])
    if cv.get("herramientas"):
        doc.add_paragraph(L["herr"] + ": " + lista(cv["herramientas"]))
    if cv.get("metodologias"):
        doc.add_paragraph(L["met"] + ": " + lista(cv["metodologias"]))
    if cv.get("idiomas"):
        titulo_seccion(L["idi"])
        doc.add_paragraph(lista(cv["idiomas"]))
    if cv.get("informacion_adicional"):
        titulo_seccion(L["info"])
        doc.add_paragraph(lista(cv["informacion_adicional"]))
    if cv.get("nota_final"):
        doc.add_paragraph(cv["nota_final"])

    doc.core_properties.title = f"{cv['nombre']} - {L['doc']}"
    doc.core_properties.author = cv["nombre"]
    doc.save(salida)
    print("DOCX generado:", salida)


if __name__ == "__main__":
    main()
