#!/usr/bin/env python3
"""Genera la versión Word (.docx) de la carta de presentación a partir del mismo JSON que generar_carta.js.

Uso: python3 generar_carta_docx.py carta.json salida.docx
Una página, fuente Arial, sin tablas ni imágenes. Requiere python-docx (pip install python-docx).
"""
import json
import re
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt


def texto_con_negritas(parrafo, texto):
    for p in re.split(r"(\*\*.+?\*\*)", texto or ""):
        if p:
            run = parrafo.add_run(p[2:-2] if p.startswith("**") else p)
            run.bold = p.startswith("**")


def main():
    entrada, salida = sys.argv[1], sys.argv[2]
    k = json.load(open(entrada, encoding="utf-8"))
    ingles = k.get("idioma", "es") == "en"
    doc = Document()
    for s in doc.sections:
        s.top_margin, s.bottom_margin = Cm(2.0), Cm(1.8)
        s.left_margin = s.right_margin = Cm(2.2)
    base = doc.styles["Normal"]
    base.font.name = "Arial"
    base.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    base.font.size = Pt(10.5)
    base.paragraph_format.space_after = Pt(6)

    def p(texto="", negrita=False, justificar=True, despues=6):
        par = doc.add_paragraph()
        if negrita:
            par.add_run(texto).bold = True
        else:
            texto_con_negritas(par, texto)
        if justificar:
            par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        par.paragraph_format.space_after = Pt(despues)
        return par

    nombre = doc.add_paragraph()
    r = nombre.add_run(k["nombre"])
    r.bold = True
    r.font.size = Pt(16)
    nombre.paragraph_format.space_after = Pt(0)
    if k.get("titulo_profesional"):
        p(k["titulo_profesional"], justificar=False, despues=0)
    c = k.get("contacto", {})
    p(" | ".join(x for x in [c.get("telefono"), c.get("email"), c.get("linkedin"), c.get("ubicacion")] if x),
      justificar=False, despues=12)

    p(k.get("lugar_fecha", ""), justificar=False, despues=10)
    for i, linea in enumerate(k.get("destinatario", [])):
        p(linea, justificar=False, despues=0)
    if k.get("referencia"):
        doc.add_paragraph().paragraph_format.space_after = Pt(0)
        p(("Re: " if ingles else "Referencia: ") + k["referencia"], negrita=True, justificar=False, despues=10)

    p(k.get("saludo", ""), justificar=False)
    for x in k.get("parrafos", []):
        p(x)
    if k.get("vinetas"):
        if k.get("vinetas_titulo"):
            p(k["vinetas_titulo"])
        for v in k["vinetas"]:
            par = doc.add_paragraph(style="List Bullet")
            texto_con_negritas(par, v)
            par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            par.paragraph_format.space_after = Pt(3)
    for x in k.get("parrafos_finales", []):
        p(x)

    p(k.get("despedida") or ("Sincerely," if ingles else "Cordialmente,"), justificar=False, despues=22)
    p(k["nombre"], negrita=True, justificar=False, despues=0)
    if k.get("titulo_profesional"):
        p(k["titulo_profesional"], justificar=False, despues=0)
    p(" | ".join(x for x in [c.get("telefono"), c.get("email")] if x), justificar=False, despues=0)

    doc.core_properties.title = f"{k['nombre']} - " + ("Cover letter" if ingles else "Carta de presentación")
    doc.core_properties.author = k["nombre"]
    doc.save(salida)
    print("DOCX generado:", salida)


if __name__ == "__main__":
    main()
