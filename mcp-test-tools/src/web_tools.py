# src/web_tools.py
import os
from pathlib import Path
from bs4 import BeautifulSoup

class WebProjectAnalyzer:
    def __init__(self, root_dir: str):
        # Convert the relative path to abs path
        self.root_dir = Path(os.path.abspath(root_dir))
        self.web_extensions = {".html", ".vue", ".jsp", ".js", ".jsx", ".tsx"}

    def _is_web_file(self, filename: str) -> bool:
        """Filtering the web file"""
        return any(filename.endswith(ext) for ext in self.web_extensions)
    
    def list_web_file(self) -> list[str]:
        """Scan the project and return the abs path file of frontend"""
        if not self.root_dir.exists():
            return [f"Error: Path {self.root_dir} does not exist"]
        
        found_files = []
        exclude = {'.git', 'node_modules', 'target', 'dist', 'venv', '.venv'}\
        
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in exclude]

            for file in files:
                if self._is_web_file(file):
                    full_path = Path(root) / file
                    found_files.append(str(full_path.resolve()))

        return found_files
    

    def get_element_selectors(self, file_path: str) -> dict:
        """Analizer a file and map ID, Class and Name for Selenium test."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            soup = BeautifulSoup(content, "html.parser")
            elements = []

            # Search the interactive tag: input, button, a, select, textarea
            for tag in soup.find_all(['input', 'button', 'a', 'select', 'textarea']):
                info = {
                    "tag": tag.name,
                    "id": tag.get('id'),
                    "name": tag.get('name'),
                    "class": tag.get('class'), # return a list
                    "type": tag.get('type'),
                    "text": tag.get_text(strip=True)[:50] # first 50 caracther of text
                }
                # Clean the None value for light Json file
                clean_info = {k: v for k, v in info.items() if v}
                elements.append(clean_info)

            return {
                "file": os.path.basename(file_path),
                "total_elements": len(elements),
                "selectors": elements
            }
        except Exception as e:
            return {"error": f"Could not parse file: {str(e)}"}
        

    def get_selenium_standards(self) -> str:
        """Returns the strict coding standards for Selenium test generation."""
        return """
        SELENIUM TEST STANDARDS:
        - NAMING CONVENTION: Test classes MUST end with the suffix 'SeleniumIT.java' (e.g., LoginSeleniumIT.java).
        - ARCHITECTURE: Implement the Page Object Model (POM) pattern. Separate page elements/actions from the test logic.
        - LIBRARIES: Use JUnit 5 (Jupiter) for assertions and lifecycle hooks (@Test, @BeforeEach, @AfterEach).
        - DRIVER MANAGEMENT: Use 'io.github.bonigarcia.wdm.WebDriverManager' for automated driver setup.
        - CLEANUP: Ensure 'driver.quit()' is always called in the @AfterEach block to prevent memory leaks.
        - SELECTORS: Favor 'By.id' or 'By.cssSelector' over XPath whenever possible for better performance and stability.
        - TARGET DIRECTORY: Save all web tests under 'src/test/java/com/magazine/manager/selenium/'.
        """