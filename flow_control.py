from fuzzywuzzy import fuzz

keywords = {
    "tecnologia": ["computador", "internet", "IA", "software"],
    "forense": ["autópsia", "investigação", "crime"],
    # Adicione mais tópicos e palavras
}

def maintain_flow(user_input, current_topic):
    for topic, words in keywords.items():
        if any(fuzz.ratio(word, user_input.lower()) > 70 for word in words):  # Fuzzy matching para mais flexibilidade
            return topic
    return current_topic

def clarify_question(user_input):
    clarifying_phrases = ["não entendi", "explique melhor", "pode clarificar"]
    return any(phrase in user_input.lower() for phrase in clarifying_phrases)