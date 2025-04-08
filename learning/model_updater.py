from learning.file_processor import FileProcessor
from learning.knowledge_extractor import KnowledgeExtractor

class ModelUpdater:
    def __init__(self):
        self.file_processor = FileProcessor()
        self.knowledge_extractor = KnowledgeExtractor()
    
    def update_from_file(self, file_path):
        """Met à jour le modèle à partir d'un fichier"""
        # Extraction du contenu du fichier
        content = self.file_processor.process_file(file_path)
        
        # Extraction des connaissances
        key_info = self.knowledge_extractor.extract_key_information(content)
        
        # Dans une version plus avancée, nous mettrions à jour un modèle d'IA ici
        # Pour l'exemple, nous retournons simplement les connaissances extraites
        return {
            "file": file_path,
            "extracted_information": len(key_info),
            "sample": key_info[:3] if key_info else []
        }
