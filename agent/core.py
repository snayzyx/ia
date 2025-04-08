import os
import json
from agent.nlp import NLPProcessor
from agent.memory import MemoryManager
from learning.model_updater import ModelUpdater

class AgentCore:
    def __init__(self):
        self.nlp = NLPProcessor()
        self.memory = MemoryManager()
        self.model_updater = ModelUpdater()
        self.learning_mode = False
    
    def process_message(self, message):
        """Traite un message de l'utilisateur et génère une réponse"""
        context = self.memory.get_context()
        processed_input = self.nlp.process_input(message, context)
        response = self.nlp.generate_response(processed_input, context)
        self.memory.add_to_history(message, response)
        return response
    
    def toggle_learning_mode(self, active=None):
        """Active ou désactive le mode apprentissage"""
        if active is not None:
            self.learning_mode = active
        else:
            self.learning_mode = not self.learning_mode
        return self.learning_mode
    
    def learn_from_file(self, file_path):
        """Apprend à partir d'un fichier"""
        if not self.learning_mode:
            return {"success": False, "message": "Mode apprentissage désactivé"}
        
        try:
            result = self.model_updater.update_from_file(file_path)
            return {"success": True, "message": f"Apprentissage réussi: {result}"}
        except Exception as e:
            return {"success": False, "message": f"Erreur d'apprentissage: {str(e)}"}