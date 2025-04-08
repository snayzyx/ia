# agent/nlp.py - Version simplifiée sans dépendances lourdes
import nltk
import random
from nltk.tokenize import word_tokenize

class NLPProcessor:
    def __init__(self):
        # Réponses simples pour différents types de requêtes
        self.responses = {
            "salutation": [
                "Bonjour ! Comment puis-je vous aider aujourd'hui ?",
                "Salut ! Je suis votre assistant virtuel.",
                "Bienvenue ! Que puis-je faire pour vous ?"
            ],
            "question": [
                "Je vais chercher cette information pour vous.",
                "Bonne question ! Voici ce que je peux vous dire...",
                "D'après mes connaissances actuelles, "
            ],
            "remerciement": [
                "Je vous en prie !",
                "Avec plaisir !",
                "Pas de problème, je suis là pour aider."
            ],
            "apprentissage": [
                "J'ai bien enregistré cette information.",
                "Merci pour cette connaissance, je l'ai ajoutée à ma base.",
                "J'apprends continuellement grâce à vos contributions."
            ],
            "default": [
                "Je comprends votre message.",
                "Merci pour cette information.",
                "Je traite votre demande."
            ]
        }
        
        # Mots-clés simples pour la classification
        self.keywords = {
            "salutation": ["bonjour", "salut", "hey", "hello", "coucou", "bonsoir"],
            "question": ["quoi", "comment", "pourquoi", "qui", "où", "quand", "?", "combien", "est-ce"],
            "remerciement": ["merci", "thanks", "thx", "remercie", "grateful"],
            "apprentissage": ["apprendre", "apprends", "enseigne", "savoir", "connaissance"]
        }
        
        # Mémoire de conversation simple pour un contexte
        self.memory = []
    
    def process_input(self, text, context=None):
        """Traite l'entrée utilisateur de façon simplifiée"""
        tokens = word_tokenize(text.lower()) if text else []
        
        # Classification basique de l'intention
        intent = "default"
        for category, words in self.keywords.items():
            if any(word in tokens for word in words):
                intent = category
                break
                
        # Ajouter à la mémoire
        if len(self.memory) > 10:
            self.memory.pop(0)
        self.memory.append(text)
            
        return {"text": text, "intent": intent, "tokens": tokens}
    
    def generate_response(self, processed_input, context=None):
        """Génère une réponse simple basée sur l'intention détectée"""
        intent = processed_input.get("intent", "default")
        text = processed_input.get("text", "")
        tokens = processed_input.get("tokens", [])
        
        # Personnaliser la réponse en fonction du contexte
        if context and "apprendre" in context.lower():
            intent = "apprentissage"
        
        # Sélectionner une réponse aléatoire appropriée
        base_response = random.choice(self.responses[intent])
        
        # Personnaliser la réponse en fonction de l'intention
        if intent == "question":
            if any(word in tokens for word in ["faire", "peux-tu", "capable"]):
                return "Je peux vous aider à organiser des informations, répondre à des questions simples, et apprendre de nouveaux documents si vous me les fournissez."
            elif any(word in tokens for word in ["tu", "toi", "ton"]):
                return "Je suis un assistant virtuel conçu pour apprendre et vous aider avec différentes tâches."
            else:
                return base_response + " Je suis encore en apprentissage sur ce sujet."
        
        elif intent == "salutation":
            return base_response + " Je suis votre assistant IA personnel."
        
        elif intent == "apprentissage":
            return base_response + " Plus vous m'enseignez, plus je deviens utile."
        
        return base_response