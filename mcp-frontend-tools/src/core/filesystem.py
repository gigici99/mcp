import os
from pathlib import Path

class FileSystemAccess:
    def __init__(self, project_root: str):
        """Inizializza l'accesso convertendo la stringa in un oggetto Path."""
        self.project_root = Path(project_root).resolve()

    def list_project_component(self) -> list[str]:
        """Scansiona il progetto e ritorna la lista dei file rilevanti."""
        if not self.project_root.exists():
            return [f"Error: the project path {self.project_root} does not exist"]
        
        found_files = []
        # Cartelle da ignorare
        exclude = {'.git', 'public', 'build', 'node_modules', 'dist', '__pycache__'}

        # Usiamo rglob per una scansione più moderna ed efficiente
        for ext in ["*.vue", "*.json", "*.js", "*.css", "*.ts"]:
            for path in self.project_root.rglob(ext):
                # Filtra se il percorso contiene cartelle escluse
                if not any(ex in path.parts for ex in exclude):
                    # Restituiamo il percorso relativo per non confondere l'LLM
                    found_files.append(str(path.relative_to(self.project_root)))
        
        return found_files
    
    def get_class_content(self, relative_path: str) -> str:
        """Legge il contenuto di un file specifico."""
        # Uniamo i percorsi in sicurezza
        full_path = (self.project_root / relative_path).resolve()
        
        try:
            return full_path.read_text(encoding="utf-8")
        except Exception as e:
            return f"Error reading file {relative_path}: {str(e)}"
        
    def write_new_component(self, relative_path: str, content: str) -> str:
        """Scrive un componente nel file system."""
        full_path = (self.project_root / relative_path).resolve()
        
        try:
            # Crea le cartelle genitrici se mancano
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")
            
            return f"Successfully written to {relative_path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"