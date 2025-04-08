from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import sent_tokenize

class KnowledgeExtractor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
    
    def extract_key_information(self, text):
        """Extrait les informations clés du texte"""
        sentences = sent_tokenize(text)
        if not sentences:
            return []
            
        # Créer une matrice TF-IDF
        tfidf_matrix = self.vectorizer.fit_transform(sentences)
        
        # Identifier les phrases les plus importantes
        important_sentences = []
        for i, sentence in enumerate(sentences):
            score = tfidf_matrix[i].sum()
            important_sentences.append((sentence, score))
            
        # Trier et retourner les phrases les plus importantes
        important_sentences.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in important_sentences[:min(10, len(important_sentences))]]