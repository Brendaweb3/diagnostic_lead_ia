Diagnostic IA Lead Qualifié
📋 Présentation
Ce projet est un diagnostic interactif pour évaluer la maturité digitale d’une entreprise et générer un PDF personnalisé.
L’utilisateur renseigne son nom/société, son email, répond à quelques questions puis télécharge son audit d’intelligence artificielle.

🗂 Structure du projet
text
diagnostic_lead_ia/
│
├── main.py                  # Script principal Streamlit
├── requirements.txt         # Dépendances Python
├── README.md                # Ce guide d’utilisation
└── assets/
    └── logo_brendabox.png   # Image/Logo pour le rapport PDF
🚀 Installation rapide
Télécharge le projet (ou clone-le sur ton poste).

Vérifie que le dossier assets contient bien logo_brendabox.png

Tu peux mettre n’importe quelle image au début pour tester, mais le fichier doit exister et se nommer comme ça.

Ouvre un terminal (PowerShell, Console, etc.) dans le dossier du projet.

Installe les dépendances nécessaires avec la commande :

text
pip install -r requirements.txt
Lance l’application en tapant :

text
python -m streamlit run main.py
Va à l’adresse donnée (en général http://localhost:8501) pour utiliser le formulaire en ligne.

🧩 Fonctionnalités
Formulaire interactif sur Streamlit

Validation email et société

Génération rapport PDF avec logo

Boutique : Téléchargement direct du rapport

Option de prise de rendez-vous Calendly

📌 Notes & Conseils
Si le logo n’apparaît pas : vérifie le nom (il doit être exactement logo_brendabox.png), et la présence dans le dossier assets.

Si tu veux personnaliser les questions : modifie la section du formulaire dans main.py.

Pour partager ce diagnostic en ligne : déploie sur Streamlit Cloud ou sur n'importe quel serveur Python.

🧑‍💻 Dépannage
Si tu rencontres une erreur “ModuleNotFoundError” : vérifie que streamlit et reportlab sont bien installés via pip.

En cas de bug “logo manquant”, vérifie le chemin et le nom du fichier logo.

En cas de souci sur Windows, assure-toi que les extensions .py, .txt et .png sont affichées correctement.

💡 Pour aller plus loin
Ajoute une base de données pour sauvegarder les audits.

Connecte un service d’email pour envoi automatique.

Personnalise le template PDF pour plus de branding.