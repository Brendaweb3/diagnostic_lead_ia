import streamlit as st
import urllib.parse
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

st.set_page_config(page_title="Diagnostic Architect IA", page_icon="🤖", layout="centered")

URL_AGENDA = "https://calendly.com/bernadette-brendaboxia/15mn"
LOGO_FILENAME = "logo_brendabox.png"

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
    try:
        logo = Image(LOGO_FILENAME, width=70*mm, height=70*mm)
        logo.hAlign = "CENTER"
        elements.append(logo)
    except Exception:
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
    elements.append(Paragraph(f"Score : {score_value} / 45", normal_left))
    elements.append(Spacer(1,2*mm))
    elements.append(Paragraph(f"Conclusion : {conclusion_text}", normal_left))
    elements.append(Spacer(1,5*mm))
    elements.append(Paragraph("Résumé des réponses :", heading))
    for k, v in responses_dict.items():
        elements.append(Paragraph(f"- {k} : {v}", normal_left))
        elements.append(Spacer(1,1*mm))
    axes = []
    if responses_dict.get("Taux de qualification") == "Moins de 40%":
        axes.append("Qualification des leads")
    if responses_dict.get("Temps manuel hebdomadaire") == "Plus de 8h/semaine":
        axes.append("Automatisation des tâches répétitives")
    if responses_dict.get("Durée du pipeline") == "Plus de 60 jours":
        axes.append("Optimisation du pipeline de vente")
    if responses_dict.get("Niveau d’intégration IA") == "Peu ou pas d’automatisation":
        axes.append("Intégration d’outils IA")
    if responses_dict.get("Objectif prioritaire") == "Augmenter la marge par client":
        axes.append("Marge et rentabilité")
    elements.append(Spacer(1,6*mm))
    elements.append(Paragraph("Axes à améliorer :", heading))
    if axes:
        for item in axes:
            elements.append(Paragraph(f"- {item}", normal_left))
    else:
        elements.append(Paragraph("Aucune friction critique détectée.", normal_left))
    elements.append(Spacer(1,6*mm))
    elements.append(Paragraph("Mentions RGPD et confidentialité : Vos réponses sont analysées dans le cadre du diagnostic BrendaBoxia. Aucun cookie publicitaire, juste le minimum technique pour le bon fonctionnement de l’outil.", subtitle_style))
    elements.append(Paragraph("Pour une feuille de route opérationnelle complète, réservez un débrief.", normal_left))
    elements.append(Spacer(1,4*mm))
    elements.append(Paragraph(f"Réserver un débrief de 15 min : {URL_AGENDA}", normal_left))
    elements.append(Spacer(1,10*mm))
    elements.append(Paragraph("© BrendaBoxia – Diagnostic IA Professionnel", subtitle_style))
    doc.build(elements)
    pdf_val = buffer.getvalue()
    buffer.close()
    return pdf_val

# --- Interface utilisateur Streamlit ---

st.title("Diagnostic Architect IA")
st.subheader("Évaluez vos frictions et préparez votre entretien")
st.write("Répondez aux questions. Vous obtiendrez un score sur 45, un mini-audit, et la possibilité de télécharger un PDF professionnel.")

name_or_company = st.text_input("🏢 Nom / Société (obligatoire)", key="name_company").strip()
email = st.text_input("✉️ Adresse email (facultatif)", key="email").strip()
consent = st.checkbox("✅ J’accepte que mes réponses soient utilisées à des fins d’analyse dans le cadre du diagnostic BrendaBoxia.")
st.caption("🔒 Aucun cookie publicitaire n’est utilisé. Des cookies techniques temporaires peuvent être créés pour le bon fonctionnement du diagnostic.")

if not name_or_company:
    st.warning("Merci d'indiquer votre nom ou celui de votre société pour poursuivre le diagnostic.")
    st.stop()

if not consent:
    st.warning("Merci de cocher la case d’acceptation (RGPD) pour continuer.")
    st.stop()

st.markdown("---")
st.markdown("### Répondez aux 5 questions ci‑dessous :")

score = 0
responses = {}

q1 = st.radio("Q1 : Quel est le taux de qualification de vos leads entrants actuellement ?",
              ["Moins de 40%", "Entre 40% et 60%", "Plus de 60%"], index=0)
if q1 == "Moins de 40%":
    score += 9
elif q1 == "Entre 40% et 60%":
    score += 6
else:
    score += 3
responses["Taux de qualification"] = q1

q2 = st.radio("Q2 : Combien de temps manuel consacrez-vous chaque semaine à des tâches répétitives ?",
              ["Plus de 8h/semaine", "Entre 4h et 8h/semaine", "Moins de 4h/semaine"], index=0)
if q2 == "Plus de 8h/semaine":
    score += 9
elif q2 == "Entre 4h et 8h/semaine":
    score += 6
else:
    score += 3
responses["Temps manuel hebdomadaire"] = q2

q3 = st.radio("Q3 : Quelle est la durée moyenne de votre pipeline de vente ?",
              ["Plus de 60 jours", "Entre 30 et 60 jours", "Moins de 30 jours"], index=0)
if q3 == "Plus de 60 jours":
    score += 9
elif q3 == "Entre 30 et 60 jours":
    score += 6
else:
    score += 3
responses["Durée du pipeline"] = q3

q4 = st.radio("Q4 : Quel est votre niveau d’intégration d’outils IA dans votre processus de vente ?",
              ["Peu ou pas d’automatisation", "Quelques outils IA spécifiques", "Processus IA bien intégré"], index=0)
if q4 == "Peu ou pas d’automatisation":
    score += 9
elif q4 == "Quelques outils IA spécifiques":
    score += 6
else:
    score += 3
responses["Niveau d’intégration IA"] = q4

q5 = st.radio("Q5 : Quel est votre objectif prioritaire pour les 3 prochains mois ?",
              ["Augmenter la marge par client", "Améliorer la vitesse de conversion", "Générer plus de leads qualifiés"], index=0)
if q5 == "Augmenter la marge par client":
    score += 3
elif q5 == "Améliorer la vitesse de conversion":
    score += 6
else:
    score += 9
responses["Objectif prioritaire"] = q5

st.markdown("---")

conclusion = ""
if score <= 15:
    st.success("Excellent ! Votre cycle de vente est fluide et déjà performant.")
    conclusion = "Excellent ! Votre cycle de vente est fluide et déjà performant."
elif score <= 30:
    st.warning("Vous avez déjà quelques intégrations efficaces, mais il reste des points d’optimisation importants.")
    conclusion = "Vous avez déjà quelques intégrations efficaces, mais il reste des points d’optimisation importants."
else:
    st.error("Votre processus comporte trop de frictions manuelles. Une refonte IA est vivement recommandée.")
    conclusion = "Votre processus comporte trop de frictions manuelles. Une refonte IA est vivement recommandée."

st.markdown("### Mini Audit Personnalisé")
for k, v in responses.items():
    st.markdown(f"- **{k}** : {v}")

# ✅ Ajoute le bloc ici :
resume_str = f"Score : {score} / 45\nConclusion : {conclusion}\n\nRésumé des réponses :"
for k, v in responses.items():
    resume_str += f"\n- {k} : {v}"
st.markdown("### Résumé à copier-coller pour Calendly :")
st.code(resume_str, language="text")

st.markdown("---")
st.markdown("### Étape suivante : votre audit personnalisé")
name_enc = urllib.parse.quote(name_or_company)
email_enc = urllib.parse.quote(email)
url_cal = f"{URL_AGENDA}?name={name_enc}&email={email_enc}&score={score}"
st.markdown(f"[👉 Réserver mon créneau Calendly]({url_cal})")
st.markdown("---")


# RGPD + cookies en bas
st.markdown('''
> *Mentions RGPD et confidentialité*
> Vos réponses sont analysées dans le cadre du diagnostic BrendaBoxia. Aucun cookie publicitaire, juste le minimum technique pour le bon fonctionnement de l’outil.
''')

# --- Génération PDF ---
if st.button("📄 Télécharger mon mini‑audit PDF"):
    pdf_bytes = generate_pdf_bytes(name_or_company, email, responses, score, conclusion)
    st.download_button("Télécharger le PDF", data=pdf_bytes, file_name="diagnostic.pdf", mime="application/pdf")
