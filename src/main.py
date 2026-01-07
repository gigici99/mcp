# src/main.py
from mcp.server.fastmcp import FastMCP
import src

# Initialize FastMCP server
mcp = FastMCP("Universal-Tests-Provider")

# Java Test Junit
@mcp.tool()
def list_java_classes(project_root: str):
    """
    List all production java class in a Spring Boot project.
    """
    analyzer = src.JavaProjectAnalyzer(project_root)
    classes = analyzer.list_production_classes()
    return "\n".join(classes) if classes else "No classes found."

@mcp.tool()
def read_java_classes(project_root: str, file_path: str):
    """
    Reads the source code of Java class to prepare for test generation.
    """
    analyzer = src.JavaProjectAnalyzer(project_root)
    return analyzer.get_class_content(file_path)

@mcp.tool()
def write_java_test(project_root: str, file_path: str, code_content: str):
    """
    Saves a generated JUnit test class to the project filesystem.
    
    :param project_root: Root directory of project.
    :type project_root: str
    :param file_path: Relative path where the test should be saved
    :type file_path: str
    :param code_content: The Java code to write
    :type code_content: str
    """
    analyzer = src.JavaProjectAnalyzer(project_root)
    return analyzer.write_test_file(file_path, code_content)

@mcp.tool()
def run_project_command(work_dir: str, command_type: str):
    """
    Executes a command based on the project type (maven or npm).
    :param work_dir: The root directory of the project.
    :param command_type: The action to perform (e.g., 'test', 'install').
    """
    executor = src.CommandExecutor(work_dir)
    return executor.execute(command_type)

# The rule for llm
@mcp.prompt()
def junit_test_style():
    """Instruction for generating JUnit tests in this project."""
    return """
    when generating JUnit 5 tests:
    1. Use AssertJ for assertions (assertThat)
    2. Use Mockito for mocking dependencies.
    3. Follow the naming convention: 'should_[ExpectedBehavior]_when_[Condition]'.
    4. Always include a test for edge cases (null inputs, empty strings)
    """


# The selenium test
@mcp.tool()
def list_frontend_files() -> list[str]:
    """List of all HTML/Vue/JS file of the project for selenium test"""
    return src.WebProjectAnalyzer.list_web_file()

@mcp.tool()
def analyze_page_elements(file_path: str) -> dict:
    """Catch the Id and selector from web file and generate the selenium Script"""
    return src.WebProjectAnalyzer.get_element_selectors(file_path)

@mcp.prompt()
def create_selenium_suite(page_name: str) -> str:
    """
    Guides the AI to create a standardized Selenium test suite for a specific page.
    """
    standards = src.WebProjectAnalyzer.get_selenium_standards()
    
    return f"""
    You are an expert QA Automation Engineer. Your task is to generate a Selenium test suite for the '{page_name}' page.
    
    ### Guidelines & Standards:
    {standards}
    
    ### Workflow Instructions:
    1. **Analyze**: Use the 'analyze_page_elements' tool to inspect the HTML/Vue file for the '{page_name}' page.
    2. **Design**: Create a Page Object class containing WebElements and action methods (e.g., loginUser, clickSubmit).
    3. **Implement**: Create the Test class using the POM, following the naming convention mentioned above.
    4. **Verify**: Ensure the package declarations and imports (JUnit 5, Selenium, WebDriverManager) are correct.
    5. **Save**: Use 'write_test_file' to store both the Page Object and the Test class in the correct project directory.

    Please start by listing which file you are going to analyze.
    """

@mcp.resource("project://summary")
def get_project_context() -> str: # Rimosso root_path
    """Returns a summary of the project detected in the current working directory."""
    import os
    cwd = os.getcwd()
    return f"Summary of project in: {cwd}"

def main():
    mcp.run()


if __name__ == "__main__":
    main()
