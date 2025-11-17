import streamlit as st
import requests
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import urllib.parse
import os  # <-- CET IMPORT EST TRÈS IMPORTANT

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Diagnostic Architecte IA",
    page_icon="🤖",
    layout="centered"
)

# --- CONSTANTES ---
URL_AGENDA = "https://calendly.com/bernadette-brendaboxia/15mn"

# --- FONCTIONS ---

def calculer_score(reponses):
    score = 0
    mapping_points = {
        "Moins de 40%": 5, "Entre 40% et 60%": 3, "Plus de 60%": 1,
        "Plus de 8h/semaine": 5, "Entre 4h et 8h/semaine": 3, "Moins de 4h/semaine": 1,
        "Plus de 60 jours": 5, "Entre 30 et 60 jours": 3, "Moins de 30 jours": 1,
        "Peu ou pas d'automatisation (ex: Zapier basique)": 5,
        "Quelques outils IA spécifiques (ex: rédaction)": 3,
        "Processus IA bien intégré (ex: CRM intelligent)": 1,
        "Augmenter radicalement la marge par client": 5,
        "Améliorer la vitesse de conversion": 3,
        "Générer plus de leads qualifiés": 1,
    }
    for reponse in reponses.values():
        score += mapping_points.get(reponse, 0)
    return score

def post_to_google_sheet(prenom, nom, email, score, reponses):
    # ON UTILISE os.environ.get AU LIEU DE st.secrets
    webhook_url = os.environ.get("GOOGLE_SHEET_WEBHOOK_URL")
    if not webhook_url:
        return
    sheet_data = {
        "name": f"{prenom} {nom}", "email": email, "score": score,
        "q1": reponses.get('q1', ''), "q2": reponses.get('q2', ''), "q3": reponses.get('q3', ''),
        "q4": reponses.get('q4', ''), "q5": reponses.get('q5', '')
    }
    try:
        requests.post(webhook_url, data=json.dumps(sheet_data), headers={'Content-Type': 'application/json'})
    except Exception as e:
        st.error(f"Erreur Google Sheet: {e}")

def send_email(recipient_email, prenom, score, url_personnalisee):
    # ON UTILISE os.environ.get AU LIEU DE st.secrets
    sender_email = os.environ.get("GMAIL_SENDER_EMAIL")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")
    if not sender_email or not app_password:
        st.warning("⚠️ L'envoi d'email n'est pas configuré.")
        return

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"Votre Diagnostic de Friction IA Personnalisé, {prenom}"

    body = f"""
    <html><body>
        <h1>Votre Diagnostic de Friction IA</h1>
        <p>Bonjour {prenom},</p>
        <p>Merci d'avoir complété notre diagnostic. Votre score de friction est de <strong>{score}/25</strong>.</p>
        <p>Réservez votre audit de 15 minutes ici :</p>
        <a href="{url_personnalisee}" style="background-color: #4CAF50; color: white; padding: 14px 25px; text-align: center; text-decoration: none; display: inline-block; border-radius: 8px;">
            Réserver mon Audit Stratégique
        </a>
    </body></html>
    """
    msg.attach(MIMEText(body, 'html'))
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
    except Exception as e:
        st.error(f"Erreur lors de l'envoi de l'email: {e}")

# --- INTERFACE PRINCIPALE ---
# (Le reste du code est identique et correct)

if 'score' not in st.session_state:
    st.title("🤖 Diagnostic de Friction IA")

    with st.form("quiz_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Votre Prénom", key="prenom")
        with col2:
            st.text_input("Votre Nom", key="nom")
        st.text_input("Votre E-mail Professionnel", key="email")
        st.markdown("---")

        reponses = {}
        reponses['q1'] = st.radio("**Q1 : Quel est le taux de qualification de vos leads entrants actuellement ?**",
                                  ["Moins de 40%", "Entre 40% et 60%", "Plus de 60%"], index=0)
        reponses['q2'] = st.radio("**Q2 : Combien de temps manuel consacrez-vous chaque semaine à des tâches répétitives ?**",
                                  ["Plus de 8h/semaine", "Entre 4h et 8h/semaine", "Moins de 4h/semaine"], index=0)
        reponses['q3'] = st.radio("**Q3 : Quelle est la durée moyenne de votre pipeline de vente ?**",
                                  ["Plus de 60 jours", "Entre 30 et 60 jours", "Moins de 30 jours"], index=0)
        reponses['q4'] = st.radio("**Q4 : Quel est votre niveau d'intégration d'outils IA ?**",
                                  ["Peu ou pas d'automatisation (ex: Zapier basique)", "Quelques outils IA spécifiques (ex: rédaction)",
                                   "Processus IA bien intégré (ex: CRM intelligent)"], index=0)
        reponses['q5'] = st.radio("**Q5 : Quel est votre objectif prioritaire pour les 3 prochains mois ?**",
                                  ["Augmenter radicalement la marge par client", "Améliorer la vitesse de conversion", "Générer plus de leads qualifiés"], index=0)

        submitted = st.form_submit_button("Calculer mon Score de Friction")
        if submitted:
            if not all([st.session_state.prenom, st.session_state.nom, st.session_state.email]):
                st.error("Merci de remplir tous les champs.") # Message simplifié
            else:
                st.session_state.score = calculer_score(reponses)
                st.session_state.reponses = reponses
                
                url_personnalisee = f"{URL_AGENDA}?name={urllib.parse.quote(st.session_state.prenom)}%20{urllib.parse.quote(st.session_state.nom)}&email={urllib.parse.quote(st.session_state.email)}"

                post_to_google_sheet(st.session_state.prenom, st.session_state.nom, st.session_state.email, st.session_state.score, reponses)
                send_email(st.session_state.email, st.session_state.prenom, st.session_state.score, url_personnalisee)
                st.rerun()

else:
    # (Cette partie reste identique et correcte)
    st.title("DIAGNOSTIC FLASH : Votre Résultat")
    st.markdown("---")
    st.write(f"Bonjour **{st.session_state.prenom}**,")
    
    score_utilisateur = st.session_state.score
    if score_utilisateur >= 15:
        st.error(f"### Votre Score de Friction IA est de : **{score_utilisateur}/25**")
    else:
        st.warning(f"### Votre Score de Friction IA est de : **{score_utilisateur}/25**")
    
    st.markdown("---")
    st.subheader("Action Requise")
    st.markdown("Un email de confirmation contenant votre lien de réservation personnalisé vient de vous être envoyé. Veuillez consulter votre boîte de réception (et votre dossier spam).")
    
    url_personnalisee = f"{URL_AGENDA}?name={urllib.parse.quote(st.session_state.prenom)}%20{urllib.parse.quote(st.session_state.nom)}&email={urllib.parse.quote(st.session_state.email)}"
    
    st.link_button("Cliquez ici pour réserver votre Audit", url_personnalisee, type="primary")
