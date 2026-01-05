# src/java_tools.py
import os
from pathlib import Path

class JavaProjectAnalyzer:
    """
    Provides tools for analyzing Java Spring Boot projects,
    focusing on JUnit test generation and codebase exploration.
    """

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)

    def list_production_classes(self) -> list[str]:
        """
        Scans the project for Java files, skipping common build/vcs folders.
        """
        if not self.root_dir.exists():
            return [f"Error: Path {self.root_dir} does not exist"]

        found_classes = []
        # Folders to ignore to speed up search and avoid noise
        exclude = {'.git', 'target', '.idea', 'build', 'node_modules'}

        for root, dirs, files in os.walk(self.root_dir):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if d not in exclude]
            
            for file in files:
                if file.endswith(".java"):
                    full_path = Path(root) / file
                    # Return path relative to the project root
                    found_classes.append(str(full_path.relative_to(self.root_dir)))
        
        return found_classes

    def get_class_content(self, relative_path: str) -> str:
        """
        Reads the content of a specific Java class.
        :param relative_path: Path relative to the project root.
        """
        full_path = self.root_dir / relative_path
        try:
            return full_path.read_text(encoding="utf-8")
        except Exception as e:
            return f"Error reading java file: {str(e)}"

    def find_existing_test(self, class_name: str) -> str:
        """
        Attempts to find an existing test for a given class name.
        Example: If class is 'UserService", it looks for 'UserServiceTest'.
        """
        test_path = self.root_dir / "src" / "test" / "java"
        if not test_path.exists():
            return "Test folder not found"
        
        target_test = f"{class_name.replace('.java', '')} + Test.java"
        for p in test_path.rglob('*.java'):
            if p.name == target_test:
                return str(p.relative_to(self.root_dir))
            
        return "No existing test found."

    def write_test_file(self, relative_path: str, content: str) -> str:
        """
        Writes a test class to the specified path.
        
        :param relative_path: e.g., 'src/test/java/com/..../MyTest.java'
        :type relative_path: str
        :param content: The full source code of the class.
        :type content: str
        """

        full_path = self.root_dir / relative_path
        try:
            # Ensure the directory exists (mkdir -p)
            full_path.parent.mkdir(parents=True, exist_ok=True)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            return f"Successfully written to {relative_path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"