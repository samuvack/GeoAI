# indexer.py

import json
import spacy
from sentence_transformers import SentenceTransformer
import numpy as np

# Laad modellen
nlp = spacy.load('nl_core_news_sm')
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')  # Aangepaste modelnaam

# Synoniemwoordenboek
synonym_dict = {

    # Voeg indien nodig meer synoniemen toe
}

# Normalisatie- en maskeringsfunctie
def normalize_question(question):
    # Mask entiteiten
    doc = nlp(question)
    masked_question = question
    for ent in doc.ents:
        masked_question = masked_question.replace(ent.text, '{' + ent.label_ + '}')
    # Vervang synoniemen
    for word, synonym in synonym_dict.items():
        masked_question = masked_question.replace(word, synonym)
    return masked_question

# Laad de JSON-trainingsdata
with open('trainingsdata.json', 'r', encoding='utf-8') as f:
    training_data = json.load(f)

# Haal de vragen en SPARQL-query's op
indexed_questions = [item['vraag'] for item in training_data]
sparql_queries = [item['sparql'] for item in training_data]

# Normaliseer en encode de geïndexeerde vragen
normalized_indexed = []
for q in indexed_questions:
    normalized_q = normalize_question(q)
    normalized_indexed.append(normalized_q)

indexed_embeddings = model.encode(normalized_indexed)

# Sla de benodigde data op
np.save('indexed_embeddings.npy', indexed_embeddings)
with open('normalized_indexed_questions.json', 'w', encoding='utf-8') as f:
    json.dump(normalized_indexed, f, ensure_ascii=False, indent=2)
with open('sparql_queries.json', 'w', encoding='utf-8') as f:
    json.dump(sparql_queries, f, ensure_ascii=False, indent=2)

print("Indexering voltooid. Data is opgeslagen.")
