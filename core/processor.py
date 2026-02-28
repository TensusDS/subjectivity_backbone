"""
Central Processor — Orchestration Hub

Responsibilities:
- Load enabled modules
- Route data between modules
- Provide unified API for adapters
- Manage module lifecycle
"""

from pathlib import Path
from typing import Dict, List, Any


class CentralProcessor:
    """Main orchestration hub for Subjectivity Backbone."""
    
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.modules: Dict[str, Any] = {}
    
    def load_modules(self, config_path: Path) -> List[str]:
        """Load enabled modules from config."""
        # TODO: Parse modules.yaml, load enabled modules
        raise NotImplementedError
    
    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run all modules and aggregate results."""
        # TODO: Call each module's evaluate(), combine results
        raise NotImplementedError
    
    def update(self, module_name: str, action: str, params: Dict[str, Any]) -> bool:
        """Update specific module state."""
        # TODO: Route update to specific module
        raise NotImplementedError
    
    def get_state(self) -> Dict[str, Any]:
        """Get combined state from all modules."""
        # TODO: Aggregate state from all modules
        raise NotImplementedError
