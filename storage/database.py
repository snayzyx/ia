import sqlite3
import os

class Database:
    def __init__(self, db_path="storage/agent_data.db"):
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """S'assure que la base de données existe"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Création des tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            agent_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE,
            value TEXT,
            source TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_conversation(self, user_input, agent_response):
        """Sauvegarde une conversation dans la base de données"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO conversations (user_input, agent_response) VALUES (?, ?)",
            (user_input, agent_response)
        )
        
        conn.commit()
        conn.close()
    
    def save_knowledge(self, key, value, source="user"):
        """Sauvegarde une connaissance dans la base de données"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT OR REPLACE INTO knowledge_base (key, value, source) VALUES (?, ?, ?)",
            (key, value, source)
        )
        
        conn.commit()
        conn.close()
    
    def get_recent_conversations(self, limit=10):
        """Récupère les conversations récentes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT user_input, agent_response, timestamp FROM conversations ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        
        results = cursor.fetchall()
        conn.close()
        
        return [{"user": row[0], "agent": row[1], "timestamp": row[2]} for row in results]