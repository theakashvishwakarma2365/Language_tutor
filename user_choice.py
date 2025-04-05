import streamlit as st

# Translations for the supported languages
translations = {
    "English": {
        "Your Current Language": "Your Current Language",
        "Language You Want to Learn": "Language You Want to Learn",
        "Proficiency Level": "Proficiency Level",
        "Select a Scenario": "Select a Scenario",
        "What you want to discuss today": "What you want to discuss today",
        "Beginner": "Beginner",
        "Intermediate": "Intermediate",
        "Practice": "Practice"
    },
    "Hindi": {
        "Your Current Language": "आपकी वर्तमान भाषा",
        "Language You Want to Learn": "आप कौन सी भाषा सीखना चाहते हैं",
        "Proficiency Level": "प्रवीणता स्तर",
        "Select a Scenario": "एक परिदृश्य चुनें",
        "What you want to discuss today": "आज आप क्या चर्चा करना चाहते हैं",
        "Beginner": "शुरुआती",
        "Intermediate": "मध्यम",
        "Practice": "अभ्यास"
    },
    "Spanish": {
        "Your Current Language": "Tu idioma actual",
        "Language You Want to Learn": "Idioma que deseas aprender",
        "Proficiency Level": "Nivel de competencia",
        "Select a Scenario": "Selecciona un escenario",
        "What you want to discuss today": "¿De qué quieres hablar hoy?",
        "Beginner": "Principiante",
        "Intermediate": "Intermedio",
        "Practice": "Práctica"
    },
    "French": {
        "Your Current Language": "Votre langue actuelle",
        "Language You Want to Learn": "Langue que vous souhaitez apprendre",
        "Proficiency Level": "Niveau de compétence",
        "Select a Scenario": "Sélectionnez un scénario",
        "What you want to discuss today": "De quoi voulez-vous discuter aujourd'hui ?",
        "Beginner": "Débutant",
        "Intermediate": "Intermédiaire",
        "Practice": "Pratique"
    }
}

# Beginner scenario translations
beginner_translations = {
    "English": [
        "Introducing yourself", "Asking for directions", "Ordering food",
        "Buying groceries", "Talking about weather", "Making a simple request",
        "Talking about family", "Booking a ticket", "Basic greetings",
        "Talking about hobbies"
    ],
    "Hindi": [
        "अपना परिचय देना", "दिशा पूछना", "खाना ऑर्डर करना",
        "किराने का सामान खरीदना", "मौसम के बारे में बात करना", "एक सरल अनुरोध करना",
        "परिवार के बारे में बात करना", "टिकट बुक करना", "मूल अभिवादन",
        "शौक के बारे में बात करना"
    ],
    "Spanish": [
        "Presentarte", "Pedir direcciones", "Pedir comida",
        "Comprar comestibles", "Hablar sobre el clima", "Hacer una solicitud simple",
        "Hablar sobre la familia", "Reservar un billete", "Saludos básicos",
        "Hablar sobre pasatiempos"
    ],
    "French": [
        "Se présenter", "Demander son chemin", "Commander à manger",
        "Acheter des provisions", "Parler de la météo", "Faire une demande simple",
        "Parler de la famille", "Réserver un billet", "Salutations de base",
        "Parler des passe-temps"
    ]
}

# Intermediate scenario translations
intermediate_translations = {
    "English": [
        "Debating a topic", "Explaining a problem", "Job interview",
        "Discussing travel plans", "Talking about health", "Making a complaint",
        "Describing an event", "Sharing opinions on movies/books",
        "Discussing current events", "Talking about technology"
    ],
    "Hindi": [
        "किसी विषय पर बहस करना", "समस्या समझाना", "नौकरी साक्षात्कार",
        "यात्रा योजनाओं पर चर्चा करना", "स्वास्थ्य के बारे में बात करना", "शिकायत करना",
        "किसी घटना का वर्णन करना", "फिल्मों/किताबों पर राय साझा करना",
        "वर्तमान घटनाओं पर चर्चा करना", "प्रौद्योगिकी के बारे में बात करना"
    ],
    "Spanish": [
        "Debatir un tema", "Explicar un problema", "Entrevista de trabajo",
        "Discutir planes de viaje", "Hablar sobre la salud", "Hacer una queja",
        "Describir un evento", "Compartir opiniones sobre películas/libros",
        "Discutir eventos actuales", "Hablar sobre tecnología"
    ],
    "French": [
        "Débattre d’un sujet", "Expliquer un problème", "Entretien d’embauche",
        "Discuter des projets de voyage", "Parler de la santé", "Faire une réclamation",
        "Décrire un événement", "Partager des avis sur des films/livres",
        "Discuter de l’actualité", "Parler de technologie"
    ]
}


def get_user_selection_ui():
    st.sidebar.header("User Preferences")

    current_language = st.sidebar.selectbox("🌐 Your Current Language", ["English", "Hindi", "Spanish", "French"])
    t = translations[current_language]  # get translation dict

    learning_language = st.sidebar.selectbox(t["Language You Want to Learn"], ["English", "Hindi", "Spanish", "French"])
    user_level = st.sidebar.radio(t["Proficiency Level"], [t["Beginner"], t["Intermediate"], t["Practice"]])

    # Map UI language-level to internal logic
    level_map = {
        t["Beginner"]: "Beginner",
        t["Intermediate"]: "Intermediate",
        t["Practice"]: "Practice"
    }
    real_level = level_map[user_level]

    # Select scenarios with translation
    if real_level == "Beginner":
        scenario = st.sidebar.selectbox(t["Select a Scenario"], beginner_translations[current_language])
    elif real_level == "Intermediate":
        scenario = st.sidebar.selectbox(t["Select a Scenario"], intermediate_translations[current_language])
    else:
        scenario = st.sidebar.text_area(t["What you want to discuss today"])

    return {
        "current_language": current_language,
        "learning_language": learning_language,
        "user_level": real_level,
        "scenario": scenario
    }
