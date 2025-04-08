# app.py - Version simplifiée
from flask import Flask, render_template, request, jsonify, Blueprint
from werkzeug.utils import secure_filename
import os
import json
import time
import nltk
import random

# Télécharger les ressources NLTK nécessaires
nltk.download('punkt_tab')
nltk.download('stopwords', quiet=True)

# Configuration de l'application
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Classe NLPProcessor simplifiée
class NLPProcessor:
    def __init__(self):
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
            "default": [
                "Je comprends votre message.",
                "Merci pour cette information.",
                "Je traite votre demande."
            ]
        }
        self.keywords = {
            "salutation": ["bonjour", "salut", "hey", "hello", "coucou"],
            "question": ["quoi", "comment", "pourquoi", "qui", "où", "quand", "?"]
        }
    
    def process_input(self, text):
        tokens = nltk.word_tokenize(text.lower())
        
        # Classification simple de l'intention
        intent = "default"
        for category, words in self.keywords.items():
            if any(word in tokens for word in words):
                intent = category
                break
                
        return {"text": text, "intent": intent}
    
    def generate_response(self, processed_input):
        intent = processed_input.get("intent", "default")
        base_response = random.choice(self.responses[intent])
        
        if intent == "question":
            return f"{base_response} Je suis en apprentissage et j'améliore mes connaissances."
        
        return base_response

# Classe MemoryManager simplifiée
class MemoryManager:
    def __init__(self):
        self.conversation_history = []
    
    def add_to_history(self, user_input, agent_response):
        self.conversation_history.append({
            "user": user_input,
            "agent": agent_response,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    def get_context(self):
        recent_history = self.conversation_history[-5:] if self.conversation_history else []
        return "\n".join([f"{h['user']} {h['agent']}" for h in recent_history])

# Classe AgentCore simplifiée
class AgentCore:
    def __init__(self):
        self.nlp = NLPProcessor()
        self.memory = MemoryManager()
        self.learning_mode = False
        self.learned_files = []
    
    def process_message(self, message):
        processed_input = self.nlp.process_input(message)
        response = self.nlp.generate_response(processed_input)
        self.memory.add_to_history(message, response)
        return response
    
    def toggle_learning_mode(self, active=None):
        if active is not None:
            self.learning_mode = active
        else:
            self.learning_mode = not self.learning_mode
        return self.learning_mode
    
    def learn_from_file(self, file_path):
        if not self.learning_mode:
            return {"success": False, "message": "Mode apprentissage désactivé"}
        
        try:
            # Simulation simple d'apprentissage
            file_name = os.path.basename(file_path)
            self.learned_files.append(file_name)
            return {
                "success": True, 
                "message": f"Apprentissage réussi du fichier: {file_name}"
            }
        except Exception as e:
            return {"success": False, "message": f"Erreur d'apprentissage: {str(e)}"}

# Création de l'agent
agent = AgentCore()

# Routes API
api_bp = Blueprint('api', __name__)

@api_bp.route('/chat', methods=['POST'])
def chat():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "Message manquant"}), 400
        
    response = agent.process_message(data['message'])
    return jsonify({"response": response})

@api_bp.route('/learning/toggle', methods=['POST'])
def toggle_learning():
    data = request.json
    active = data.get('active') if data else None
    
    mode_status = agent.toggle_learning_mode(active)
    return jsonify({"learning_mode": mode_status})

@api_bp.route('/learning/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Aucun fichier sélectionné"}), 400
        
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    result = agent.learn_from_file(file_path)
    return jsonify(result)

@api_bp.route('/history', methods=['GET'])
def get_history():
    limit = request.args.get('limit', 10, type=int)
    history = agent.memory.conversation_history[-limit:] if agent.memory.conversation_history else []
    return jsonify({"history": history})

# Enregistrement du blueprint API
app.register_blueprint(api_bp, url_prefix='/api')

# Route principale
@app.route('/')
def index():
    return render_template('index.html')

# Point d'entrée
if __name__ == '__main__':
    app.run(debug=True)