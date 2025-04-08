class MemoryManager:
    def __init__(self):
        self.conversation_history = []
        self.knowledge_base = {}
    
    def add_to_history(self, user_input, agent_response):
        """Ajoute une paire d'échanges à l'historique"""
        self.conversation_history.append({
            "user": user_input,
            "agent": agent_response,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        })
    
    def get_context(self, limit=5):
        """Récupère le contexte récent de la conversation"""
        recent_history = self.conversation_history[-limit:] if self.conversation_history else []
        context = ""
        for exchange in recent_history:
            context += f"Utilisateur: {exchange['user']}\nAgent: {exchange['agent']}\n"
        return context
    
    def save_knowledge(self, key, value):
        """Sauvegarde une connaissance dans la base"""
        self.knowledge_base[key] = value
        
    def get_knowledge(self, key, default=None):
        """Récupère une connaissance de la base"""
        return self.knowledge_base.get(key, default)