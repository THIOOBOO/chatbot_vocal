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
