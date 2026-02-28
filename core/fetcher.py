"""
Module Fetcher — Download and Validate Modules

Handles:
- Parsing modules.yaml
- Fetching from different sources (clawhub, github, local)
- Running validation before install
- Installing to modules/ directory
"""

import yaml
import shutil
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

from .validator import ModuleValidator, ValidationResult


@dataclass
class ModuleSpec:
    name: str
    source: str
    description: str
    enabled: bool
    
    @property
    def source_type(self) -> str:
        """Extract source type (clawhub, github, local)."""
        if self.source.startswith("clawhub://"):
            return "clawhub"
        elif self.source.startswith("github://"):
            return "github"
        elif self.source.startswith("local://"):
            return "local"
        else:
            return "unknown"


class ModuleFetcher:
    """Fetches and validates modules from external sources."""
    
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.modules_dir = workspace / "modules"
        self.config_path = workspace / "modules.yaml"
        self.validator = ModuleValidator()
    
    def load_config(self) -> List[ModuleSpec]:
        """Load module specifications from config."""
        if not self.config_path.exists():
            return []
        
        with open(self.config_path) as f:
            config = yaml.safe_load(f)
        
        modules = []
        for m in config.get("modules", []):
            modules.append(ModuleSpec(
                name=m["name"],
                source=m["source"],
                description=m.get("description", ""),
                enabled=m.get("enabled", True)
            ))
        return modules
    
    def fetch_all(self, validate: bool = True) -> dict:
        """Fetch all enabled modules."""
        results = {"fetched": [], "failed": [], "skipped": []}
        
        for module in self.load_config():
            if not module.enabled:
                results["skipped"].append(module.name)
                continue
            
            result = self.fetch_module(module, validate=validate)
            if result:
                results["fetched"].append(module.name)
            else:
                results["failed"].append(module.name)
        
        return results
    
    def fetch_module(self, module: ModuleSpec, validate: bool = True) -> bool:
        """Fetch a single module."""
        print(f"Fetching {module.name} from {module.source}...")
        
        # Create temp directory for download
        temp_dir = self.workspace / ".tmp" / module.name
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Download based on source type
            if module.source_type == "clawhub":
                success = self._fetch_clawhub(module, temp_dir)
            elif module.source_type == "github":
                success = self._fetch_github(module, temp_dir)
            elif module.source_type == "local":
                success = self._fetch_local(module, temp_dir)
            else:
                print(f"  Unknown source type: {module.source_type}")
                return False
            
            if not success:
                return False
            
            # Validate if requested
            if validate:
                result = self.validator.validate(temp_dir)
                print(f"  {result}")
                if not result.passed:
                    print(f"  Validation failed, not installing")
                    return False
            
            # Install to modules/
            target_dir = self.modules_dir / module.name
            if target_dir.exists():
                shutil.rmtree(target_dir)
            shutil.move(str(temp_dir), str(target_dir))
            
            print(f"  Installed to modules/{module.name}")
            return True
            
        finally:
            # Cleanup temp
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
    
    def _fetch_clawhub(self, module: ModuleSpec, target: Path) -> bool:
        """Fetch from ClawHub."""
        # Parse: clawhub://name@version
        source = module.source.replace("clawhub://", "")
        if "@" in source:
            name, version = source.split("@", 1)
        else:
            name, version = source, "latest"
        
        # Use clawhub CLI
        try:
            result = subprocess.run(
                ["clawhub", "install", name, "--version", version, "--path", str(target)],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"  ClawHub fetch failed: {e}")
            return False
    
    def _fetch_github(self, module: ModuleSpec, target: Path) -> bool:
        """Fetch from GitHub."""
        # TODO: Implement GitHub fetching
        print("  GitHub fetching not yet implemented")
        return False
    
    def _fetch_local(self, module: ModuleSpec, target: Path) -> bool:
        """Copy from local path."""
        source = module.source.replace("local://", "")
        source_path = Path(source).expanduser()
        
        if not source_path.exists():
            print(f"  Local path not found: {source_path}")
            return False
        
        shutil.copytree(source_path, target, dirs_exist_ok=True)
        return True
