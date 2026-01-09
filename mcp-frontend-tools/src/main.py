from .core.filesystem import FileSystemAccess
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("frontend-architect")

@mcp.tool()
def list_component_vue(project_root: str):
    """Return the list of all component in vue.js project"""
    analyzer = FileSystemAccess(project_root)
    return analyzer.list_project_component()

@mcp.tool()
def read_component_vue(project_root: str, file_path: str):
    """
    Reads the source code of Vue.js Components.
    """
    analyzer = FileSystemAccess(project_root)
    return analyzer.get_class_content(file_path)

@mcp.tool()
def write_new_component(project_root: str, file_path: str, code_content: str):
    """
    Saves a generated Component to the project filesystem.
    
    :param project_root: Root directory of project.
    :type project_root: str
    :param file_path: Relative path where the component should be saved
    :type file_path: str
    :param code_content: The Component.vue code to write
    :type code_content: str
    """
    analyzer = FileSystemAccess(project_root)
    return analyzer.write_new_component(file_path, code_content)

def main():
    mcp.run()


if __name__ == "__main__":
    main()