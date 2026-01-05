# src/executor.py
import subprocess
import os
import platform

class CommandExecutor:
    def __init__(self, work_dir):
        self.work_dir = work_dir
        # Determine if we are on Windows to handle shell commands correctly
        self.is_windows = platform.system() == "Windows"

    def execute(self, action):
        """Detects the build tool and runs the requested action."""
        if os.path.exists(os.path.join(self.work_dir, "pom.xml")):
            return self._run_maven(action)
        elif os.path.exists(os.path.join(self.work_dir, "package.json")):
            return self._run_npm(action)
        else:
            return "Error: No supported build tool (Maven/NPM) detected in the specified directory."

    def _run_maven(self, action):
        """Executes Maven commands. Uses mvnw if present, otherwise system mvn."""
        # Use Maven Wrapper (mvnw) if available, otherwise fallback to global 'mvn'
        mvn_cmd = "mvnw" if os.path.exists(os.path.join(self.work_dir, "mvnw")) else "mvn"
        
        # On Windows, wrappers and commands often need the .cmd extension or shell=True
        if self.is_windows and mvn_cmd == "mvnw":
            mvn_cmd = "mvnw.cmd"
            
        return self._invoke_process([mvn_cmd, action])

    def _run_npm(self, action):
        """Executes NPM commands."""
        npm_cmd = "npm.cmd" if self.is_windows else "npm"
        return self._invoke_process([npm_cmd, action])

    def _invoke_process(self, command_list):
        """Helper to run the actual subprocess and capture output."""
        try:
            # shell=True is often required on Windows to find .cmd or .exe in PATH
            process = subprocess.run(
                command_list,
                cwd=self.work_dir,
                capture_output=True,
                text=True,
                shell=self.is_windows
            )
            
            output = f"Command: {' '.join(command_list)}\n"
            output += f"--- STDOUT ---\n{process.stdout}\n"
            
            if process.stderr:
                output += f"--- STDERR ---\n{process.stderr}\n"
                
            return output
        except Exception as e:
            return f"Execution failed: {str(e)}"