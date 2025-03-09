# matcher.py

import json
import spacy
from sentence_transformers import SentenceTransformer, util
import numpy as np

# Laad modellen
nlp = spacy.load('nl_core_news_sm')
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')  # Aangepaste modelnaam

# Synoniemwoordenboek
synonym_dict = {
    "nummer": "telefoonnummer",
    "mobiel": "telefoon",
    "geven": "verstrekken",
    # Voeg indien nodig meer synoniemen toe
}

# Normalisatie- en maskeringsfunctie
def normalize_question(question):
    # Mask entiteiten
    doc = nlp(question)
    masked_question = question
    entities = {}
    for ent in doc.ents:
        masked_question = masked_question.replace(ent.text, '{' + ent.label_ + '}')
        entities[ent.label_] = ent.text
    # Vervang synoniemen
    for word, synonym in synonym_dict.items():
        masked_question = masked_question.replace(word, synonym)
    return masked_question, entities

# Laad de opgeslagen data
indexed_embeddings = np.load('indexed_embeddings.npy')
with open('normalized_indexed_questions.json', 'r', encoding='utf-8') as f:
    normalized_indexed = json.load(f)
with open('sparql_queries.json', 'r', encoding='utf-8') as f:
    sparql_queries = json.load(f)

# Gebruikersvraag
user_question = input("Voer je vraag in: ")

# Normaliseer de gebruikersvraag en haal entiteiten op
normalized_user_question, entities = normalize_question(user_question)
user_embedding = model.encode([normalized_user_question])

# Bereken de cosine similarity met alle geïndexeerde vragen
cosine_scores = util.cos_sim(user_embedding, indexed_embeddings)[0]

# Vind de beste match en bereken het percentage
max_score = cosine_scores.max().item()
max_idx = cosine_scores.argmax().item()
percentage_match = max_score * 100  # Bereken het percentage

if max_score > 0.7:
    # Beste match gevonden
    best_matched_question = normalized_indexed[max_idx]
    corresponding_sparql = sparql_queries[max_idx]

    # Vervang placeholders in SPARQL-query met entiteiten
    for placeholder, value in entities.items():
        placeholder_tag = f'{{{placeholder}}}'
        corresponding_sparql = corresponding_sparql.replace(placeholder_tag, value)

    print("\nResultaat:")
    print("Gebruikersvraag:", user_question)
    print("Genormaliseerde vraag:", normalized_user_question)
    print("Beste match:", best_matched_question)
    print(f"Percentage match: {percentage_match:.2f}%")
    print("SPARQL-query:")
    print(corresponding_sparql)
else:
    print("Geen voldoende match gevonden.")
