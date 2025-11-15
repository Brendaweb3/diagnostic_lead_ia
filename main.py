import streamlit as st
import urllib.parse
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

st.set_page_config(page_title="Diagnostic Architect IA", page_icon="🤖", layout="centered")

URL_AGENDA = "https://calendly.com/bernadette-brendaboxia/15mn"
LOGO_FILENAME = "assets/logo_brendabox.png"

class VerticalGradient(Flowable):
    def __init__(self, height, width=6*mm, colors_list=None):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.colors_list = colors_list or [(0.15,0.2,0.6),(0.9,0.5,0.6),(0.9,0.78,0.4)]
    def draw(self):
        step = self.height / len(self.colors_list)
        y = 0
        for c in self.colors_list:
            self.canv.setFillColorRGB(c, c, c)
            self.canv.rect(0, y, self.width, step, stroke=0, fill=1)
            y += step

def generate_pdf_bytes(name_or_company, email, responses_dict, score_value, conclusion_text):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
        rightMargin=18*mm, leftMargin=18*mm,
        topMargin=18*mm, bottomMargin=18*mm)
    elements = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("Title", parent=styles["Title"], alignment=TA_CENTER, fontSize=18, leading=22)
    subtitle_style = ParagraphStyle("Subtitle", parent=styles["Normal"], alignment=TA_CENTER, fontSize=10, leading=12)
    normal_left = ParagraphStyle("NormalLeft", parent=styles["Normal"], alignment=TA_LEFT, fontSize=10, leading=14)
    heading = ParagraphStyle("Heading", parent=styles["Heading2"], alignment=TA_LEFT, fontSize=12, leading=14)
    
    grad = VerticalGradient(height=200*mm)
    elements.append(grad)
    elements.append(Spacer(1,4*mm))
    
    elements.append(Paragraph("BrendaBoxia", title_style))
    elements.append(Spacer(1,4*mm))
    elements.append(Paragraph("Diagnostic Architect IA", title_style))
    elements.append(Spacer(1,2*mm))
    elements.append(Paragraph("Mini-audit professionnel", subtitle_style))
    elements.append(Spacer(1,6*mm))
    
    client_info = f"Nom / Société : {name_or_company}"
    if email:
        client_info += f" • Email : {email}"
    elements.append(Paragraph(client_info, normal_left))
    elements.append(Spacer(1,4*mm))
    elements.append(Paragraph(f"Score : {score_value} / 30", normal_left))
    elements.append(Spacer(1,2*mm))
    elements.append(Paragraph(f"Conclusion : {conclusion_text}", normal_left))
    elements.append(Spacer(1,5*mm))
    elements.append(Paragraph("Résumé des réponses :", heading))
    for k,v in responses_dict.items():
        elements.append(Paragraph(f"- {k} : {v}", normal_left))
        elements.append(Spacer(1,1*mm))
    elements.append(Spacer(1,6*mm))
    elements.append(Paragraph("Pistes d'action"))

