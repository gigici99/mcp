import json
from pathlib import Path

class ProjectAnalyzer:
    @staticmethod
    def get_info(root_path: Path):
        pkg_json = root_path / "package.json"
        if not pkg_json.exists():
            return {"framework": "unknown"}
        
        with open(pkg_json) as f:
            data = json.load(f)
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            
            if "vue" in deps: return "vue"
            if "@angular/core" in deps: return "angular"
            return "generic"