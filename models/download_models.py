import spacy
from sentence_transformers import SentenceTransformer

def download_models():
    print("Downloading spaCy model...")
    spacy.cli.download("en_core_web_sm")
    
    print("Downloading sentence transformer model...")
    SentenceTransformer('all-MiniLM-L6-v2')
    
    print("All models downloaded successfully!")

if __name__ == "__main__":
    download_models()
