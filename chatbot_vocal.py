# streamlit_chatbot_vocal_fichier.py

import streamlit as st
import speech_recognition as sr
import re

# ---------- CONFIGURATION STREAMLIT ----------
st.set_page_config(page_title="Chatbot Vocal Data Science", page_icon="🎤")

# ---------- HISTORIQUE DU CHAT ----------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- CHARGEMENT DU FICHIER TEXTE ----------
try:
    with open("chat_data.txt", "r", encoding="utf-8") as f:
        texte_chatbot = f.read()
except FileNotFoundError:
    st.error("⚠️ Le fichier 'chat_data.txt' est introuvable. Créez-le dans le même dossier que ce script.")
    texte_chatbot = ""

# ---------- FONCTION DE RECHERCHE PAR MOTS-CLÉS ----------
def chercher_reponse(question, base_connaissances):
    question = question.lower()
    mots_question = set(re.findall(r"\w+", question))  # découpe en mots

    meilleur_score = 0
    meilleure_reponse = "Désolé, je n'ai pas compris."

    for ligne in base_connaissances.split("\n"):
        if ligne.strip():
            mots_ligne = set(re.findall(r"\w+", ligne.lower()))
            score = len(mots_question.intersection(mots_ligne))  # nb de mots en commun
            if score > meilleur_score:
                meilleur_score = score
                meilleure_reponse = ligne

    return meilleure_reponse

# ---------- FONCTION DE RECONNAISSANCE VOCALE ----------
def transcrire_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Parlez maintenant...")
        audio = recognizer.listen(source)
    try:
        texte = recognizer.recognize_google(audio, language="fr-FR")
        return texte
    except sr.UnknownValueError:
        return "Je n'ai pas compris ce que vous avez dit."
    except sr.RequestError:
        return "Erreur du service de reconnaissance vocale."

# ---------- INTERFACE STREAMLIT ----------
st.title("🤖 Chatbot Vocal Data Science")

# Choix du mode d'entrée
mode = st.radio("Choisissez le mode d'entrée :", ["Texte", "Voix"])

user_input = ""
if mode == "Texte":
    user_input = st.text_input("Tapez votre message :")
elif mode == "Voix":
    if st.button("🎤 Parler"):
        user_input = transcrire_audio()
        st.session_state.history.append(("Utilisateur (voix)", user_input))

# Interaction avec le chatbot
if user_input:
    if mode == "Texte":
        st.session_state.history.append(("Utilisateur", user_input))

    response = chercher_reponse(user_input, texte_chatbot)
    st.session_state.history.append(("Chatbot", response))

# Affichage de l'historique
for speaker, message in st.session_state.history:
    if speaker.startswith("Utilisateur"):
        st.markdown(f"**{speaker}** : {message}")
    else:
        st.markdown(f"**{speaker}** : {message}")
# Le texte suivant est contenu du fichier texte avec lequel j'ai teste mon appli
# La data science est la science des données.
# Un data scientist est un expert qui analyse et interprète des données complexes.
# La data science combine les mathématiques, la statistique, l’informatique et la connaissance métier.
# Les principales étapes de la data science sont la collecte des données, le nettoyage, l’analyse, la modélisation et la visualisation.
# Le langage Python est très utilisé en data science.
# Le langage R est également utilisé pour les statistiques et la visualisation.
# La machine learning est une branche de l’intelligence artificielle qui apprend à partir des données.
# La visualisation de données permet de mieux comprendre les tendances et les relations.
# Un modèle prédictif est un modèle qui permet de prévoir un résultat futur à partir des données passées.
# Les bibliothèques Python populaires en data science sont pandas, numpy, matplotlib, scikit-learn et tensorflow.
# Le big data désigne les ensembles de données trop volumineux pour être traités avec des outils classiques.
# Les domaines d’application de la data science incluent la santé, la finance, le marketing et l’industrie.
# Un algorithme est une suite d’instructions permettant de résoudre un problème.
# L’intelligence artificielle regroupe les techniques qui permettent aux machines d’imiter l’intelligence humaine.
# La régression est une méthode statistique utilisée pour prédire une variable numérique.
# La classification est une technique qui permet de prédire une catégorie.
# Un data engineer prépare et organise les données pour les data scientists.
# La différence entre un data analyst et un data scientist est que le premier décrit les données tandis que le second construit des modèles prédictifs.

