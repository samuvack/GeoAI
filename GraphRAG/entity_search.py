import spacy
from spacy.pipeline import EntityRuler
from sentence_transformers import SentenceTransformer
import json

# Initialiseer SpaCy en laad het Nederlandse model
nlp = spacy.load("nl_core_news_sm")

# Voeg een EntityRuler toe voor aangepaste entiteiten
def add_custom_entities():
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    patterns = [
        {"label": "PER", "pattern": "Briek"}
    ]
    ruler.add_patterns(patterns)
add_custom_entities()

# Definieer een lijst met bekende organisaties en verenigingen
known_organizations = {"Vlaamse Overheid", "UNICEF", "Google", "Microsoft"}

# Methode om kennisbanken van organisaties en verenigingen te raadplegen (mock implementatie)
def check_knowledge_banks(entity_text):
    # Voorbeeld voor gebruik van een fictieve kennisbank (hier vervangen door lokale check)
    if entity_text in known_organizations:
        return "ORG"
    return None

# Methode om te classificeren of een entiteit een persoon of organisatie is
def classify_entity(entity_text, sentence):
    # 1. Controleer kennisbanken
    entity_class = check_knowledge_banks(entity_text)
    if entity_class:
        return entity_class
    
    # 2. Pre-training kennis van namen en contextueel begrip (Gebruik van SpaCy)
    doc = nlp(sentence)
    for ent in doc.ents:
        if ent.text == entity_text:
            return ent.label_

# Normaliseer de vraag en probeer de entiteiten te classificeren
def normalize_question_with_context(question):
    doc = nlp(question)
    masked_question = question
    entities = {}

    for ent in doc.ents:
        # Classificeer de entiteit op basis van bovenstaande stappen
        label = classify_entity(ent.text, question)
        if label == "PER":
            placeholder = "{naam}"
        elif label == "ORG":
            placeholder = "{organisatie}"
        else:
            placeholder = "{" + ent.label_ + "}"

        masked_question = masked_question.replace(ent.text, placeholder)
        entities[label] = ent.text

    return masked_question, entities

# Voorbeeldvraag
question = "Wat is het telefoonnummer van Briek?"
masked_question, entities = normalize_question_with_context(question)

# Resultaten afdrukken
print("Genormaliseerde vraag:", masked_question)
print("Entiteiten:", entities)

# Output kan er bijvoorbeeld zo uitzien:
# Genormaliseerde vraag: Wat is het telefoonnummer van {naam}?
# Entiteiten: {'PER': 'Briek'}
