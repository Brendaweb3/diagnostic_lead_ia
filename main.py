import streamlit as st
import requests
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import urllib.parse
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO

st.set_page_config(page_title="Diagnostic Architecte IA", page_icon="🤖", layout="centered")

URL_AGENDA = "https://calendly.com/bernadette-brendaboxia/15mn"

def calculer_score(reponses):
    score = 0
    mapping_points = {
        "Moins de 40%": 10, "Entre 40% et 60%": 5, "Plus de 60%": 1,
        "Plus de 8h/semaine": 10, "Entre 4h et 8h/semaine": 5, "Moins de 4h/semaine": 1,
        "Plus de 60 jours": 10, "Entre 30 et 60 jours": 5, "Moins de 30 jours": 1,
        "Peu ou pas d'automatisation": 10, "Quelques outils IA spécifiques": 5, "Processus IA bien intégré": 1,
        # --- LOGIQUE CORRIGÉE POUR Q5 ---
        "Générer plus de leads qualifiés": 5,
        "Améliorer la vitesse de conversion": 3,
        "Augmenter la marge par client": 1,
    }
    for reponse in reponses.values():
        score += mapping_points.get(reponse, 0)
    return score

def generer_conclusion(score):
    if score > 30:
        return "Votre processus comporte trop de frictions manuelles. Une refonte IA est vivement recommandée."
    elif score > 15:
        return "Des optimisations ciblées via l'IA pourraient considérablement accélérer votre cycle de vente."
    else:
        return "Votre processus est déjà bien optimisé. L'IA pourrait vous aider à atteindre le niveau supérieur."

def generate_pdf_bytes(prenom, entreprise, email, responses, score, conclusion):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    if os.path.exists("logo_brendabox.png"):
        story.append(Image("logo_brendabox.png", width=1.5*inch, height=1.5*inch))
        story.append(Spacer(1, 0.25*inch))
    story.append(Paragraph("Diagnostic de Friction IA", styles['h1']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"Rapport pour : {prenom} ({entreprise})", styles['h2']))
    if email: story.append(Paragraph(f"Email : {email}", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(f"Score de Friction : {score} / 45", styles['h2']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"<b>Conclusion :</b> {conclusion}", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Résumé de vos réponses :", styles['h2']))
    for key, value in responses.items():
        story.append(Paragraph(f"<b>{key} :</b> {value}", styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def post_to_google_sheet(prenom, entreprise, email, score, reponses):
    webhook_url = os.environ.get("GOOGLE_SHEET_WEBHOOK_URL")
    if not webhook_url: return
    sheet_data = { "name": f"{prenom} ({entreprise})", "email": email, "score": score, "q1": reponses.get('Q1', ''), "q2": reponses.get('Q2', ''), "q3": reponses.get('Q3', ''), "q4": reponses.get('Q4', ''), "q5": reponses.get('Q5', '') }
    try: requests.post(webhook_url, data=json.dumps(sheet_data), headers={'Content-Type': 'application/json'})
    except Exception as e: print(f"Erreur Google Sheet: {e}")

def send_email(recipient_email, prenom, score, url_personnalisee):
    if not recipient_email: return
    sender_email = os.environ.get("GMAIL_SENDER_EMAIL")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")
    if not sender_email or not app_password: return
    msg = MIMEMultipart(); msg['From'] = sender_email; msg['To'] = recipient_email; msg['Subject'] = f"Votre Diagnostic de Friction IA, {prenom}"
    body = f"""<html><body><h1>Votre Diagnostic IA est prêt</h1><p>Bonjour {prenom},</p><p>Merci d'avoir complété notre diagnostic. Votre score de friction est de <strong>{score}/45</strong>.</p><p>Pour discuter du plan d'action détaillé, réservez votre audit via ce lien personnalisé :</p><a href="{url_personnalisee}" style="background-color: #4CAF50; color: white; padding: 14px 25px; text-align: center; text-decoration: none; display: inline-block; border-radius: 8px;">Réserver mon Audit</a></body></html>"""
    msg.attach(MIMEText(body, 'html'))
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server: server.login(sender_email, app_password); server.send_message(msg)
    except Exception as e: print(f"Erreur Email: {e}")

# --- INTERFACE PRINCIPALE ---
st.title("Diagnostic Architect IA")
st.header("Évaluez vos frictions et préparez votre entretien")
st.markdown("Répondez aux questions. Vous obtiendrez un score sur 45, un mini-audit, et la possibilité de télécharger un PDF professionnel.")

entreprise = st.text_input("🏢 Nom de l'entreprise (obligatoire)")
prenom = st.text_input("👤 Votre Prénom (obligatoire)")
email = st.text_input("✉️ Adresse email (facultatif)")
st.caption("🔒 Aucun cookie publicitaire n’est utilisé. Des cookies techniques temporaires peuvent être créés pour le bon fonctionnement du diagnostic.")

st.subheader("Répondez aux 5 questions ci‑dessous :")
responses = {}
responses['Q1'] = st.radio("**Q1 : Quel est le taux de qualification de vos leads entrants actuellement ?**", ["Moins de 40%", "Entre 40% et 60%", "Plus de 60%"])
responses['Q2'] = st.radio("**Q2 : Combien de temps manuel consacrez-vous chaque semaine à des tâches répétitives ?**", ["Plus de 8h/semaine", "Entre 4h et 8h/semaine", "Moins de 4h/semaine"])
responses['Q3'] = st.radio("**Q3 : Quelle est la durée moyenne de votre pipeline de vente ?**", ["Plus de 60 jours", "Entre 30 et 60 jours", "Moins de 30 jours"])
responses['Q4'] = st.radio("**Q4 : Quel est votre niveau d’intégration d’outils IA dans votre processus de vente ?**", ["Peu ou pas d'automatisation", "Quelques outils IA spécifiques", "Processus IA bien intégré"])
responses['Q5'] = st.radio("**Q5 : Quel est votre objectif prioritaire pour les 3 prochains mois ?**", ["Augmenter la marge par client", "Améliorer la vitesse de conversion", "Générer plus de leads qualifiés"])

if st.button("Lancer le Diagnostic"):
    if not entreprise or not prenom:
        st.error("Les champs 'Nom de l'entreprise' et 'Votre Prénom' sont obligatoires.")
    else:
        score = calculer_score(responses)
        conclusion = generer_conclusion(score)

        st.success(conclusion)
        if email: st.success("✅ Email envoyé ! Vérifiez votre boîte de réception.")
        
        st.subheader("Mini Audit Personnalisé")
        for key, value in responses.items():
            st.write(f"- {key.split(':')[0].strip()} : {value}")
        
        st.subheader("Résumé à copier-coller pour Calendly :")
        resume_text = f"Score : {score} / 45\nConclusion : {conclusion}\n\nRésumé des réponses :\n"
        for key, value in responses.items():
            resume_text += f"- {key.split(':')[0].strip()} : {value}\n"
        st.code(resume_text)

        pdf_bytes = generate_pdf_bytes(prenom, entreprise, email, responses, score, conclusion)
        st.download_button(
            label="📄 Télécharger mon Audit PDF",
            data=pdf_bytes,
            file_name=f"audit_ia_{entreprise.replace(' ', '_').lower()}.pdf",
            mime="application/pdf"
        )
        
        url_personnalisee = f"{URL_AGENDA}?name={urllib.parse.quote(prenom)}%20({urllib.parse.quote(entreprise)})&email={urllib.parse.quote(email)}"
        
        st.subheader("Étape suivante : votre audit personnalisé")
        st.link_button("👉 Réserver mon créneau Calendly", url_personnalisee, type="primary")

        post_to_google_sheet(prenom, entreprise, email, score, responses)
        send_email(email, prenom, score, url_personnalisee)

st.markdown("---")
st.caption("Mentions RGPD et confidentialité Vos réponses sont analysées dans le cadre du diagnostic BrendaBoxia. Aucun cookie publicitaire, juste le minimum technique pour le bon fonctionnement de l’outil.")
