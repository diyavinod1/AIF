import re
import spacy
from typing import List, Tuple

class NLPUtils:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            import spacy.cli
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
    
    def extract_entities(self, text: str) -> List[Tuple[str, str]]:
        """Extract named entities from text"""
        doc = self.nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities
    
    def sentence_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        doc1 = self.nlp(text1)
        doc2 = self.nlp(text2)
        return doc1.similarity(doc2)
    
    def extract_phrases(self, text: str, pattern_type: str = "noun_chunks") -> List[str]:
        """Extract phrases from text"""
        doc = self.nlp(text)
        
        if pattern_type == "noun_chunks":
            return [chunk.text for chunk in doc.noun_chunks]
        elif pattern_type == "verbs":
            return [token.lemma_ for token in doc if token.pos_ == "VERB"]
        else:
            return [token.text for token in doc if token.is_alpha]
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:]', '', text)
        
        return text.strip()