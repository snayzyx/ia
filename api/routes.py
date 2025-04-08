from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename

api_bp = Blueprint('api', __name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@api_bp.route('/chat', methods=['POST'])
def chat():
    """Point d'accès pour les messages de chat"""
    from app import agent
    
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "Message manquant"}), 400
        
    response = agent.process_message(data['message'])
    return jsonify({"response": response})

@api_bp.route('/learning/toggle', methods=['POST'])
def toggle_learning():
    """Active ou désactive le mode apprentissage"""
    from app import agent
    
    data = request.json
    active = data.get('active') if data else None
    
    mode_status = agent.toggle_learning_mode(active)
    return jsonify({"learning_mode": mode_status})

@api_bp.route('/learning/upload', methods=['POST'])
def upload_file():
    """Upload et traitement d'un fichier pour l'apprentissage"""
    from app import agent
    
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
    """Récupère l'historique des conversations"""
    from app import agent
    
    limit = request.args.get('limit', 10, type=int)
    history = agent.memory.conversation_history[-limit:] if agent.memory.conversation_history else []
    return jsonify({"history": history})