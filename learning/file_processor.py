import os
import mimetypes
import PyPDF2
import docx
import csv

class FileProcessor:
    def __init__(self):
        self.supported_types = {
            'text/plain': self._process_text,
            'application/pdf': self._process_pdf,
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': self._process_docx,
            'text/csv': self._process_csv,
        }
    
    def process_file(self, file_path):
        """Traite un fichier et en extrait le contenu"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")
            
        mime_type, _ = mimetypes.guess_type(file_path)
        
        if mime_type not in self.supported_types:
            raise ValueError(f"Type de fichier non supporté: {mime_type}")
            
        return self.supported_types[mime_type](file_path)
    
    def _process_text(self, file_path):
        """Traite un fichier texte"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _process_pdf(self, file_path):
        """Traite un fichier PDF"""
        text = ""
        try:
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Erreur lors du traitement du PDF: {str(e)}")
        return text
    
    def _process_docx(self, file_path):
        """Traite un fichier DOCX"""
        try:
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            raise Exception(f"Erreur lors du traitement du DOCX: {str(e)}")
    
    def _process_csv(self, file_path):
        """Traite un fichier CSV"""
        data = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                csv_reader = csv.reader(f)
                headers = next(csv_reader)
                for row in csv_reader:
                    row_data = {}
                    for i, value in enumerate(row):
                        if i < len(headers):
                            row_data[headers[i]] = value
                    data.append(row_data)
        except Exception as e:
            raise Exception(f"Erreur lors du traitement du CSV: {str(e)}")
        return json.dumps(data)
