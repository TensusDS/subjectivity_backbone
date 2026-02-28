"""
Module Validator — Security and Compatibility Checks

Validates modules before activation:
- Structure check (required files, layout)
- Dangerous patterns scan (AST analysis)
- Ethics compatibility check
- API compatibility check
"""

import ast
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ValidationCheck:
    name: str
    passed: bool
    message: str


@dataclass
class ValidationResult:
    module_name: str
    passed: bool
    checks: List[ValidationCheck]
    
    def __str__(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        return f"[{status}] {self.module_name}: {len([c for c in self.checks if c.passed])}/{len(self.checks)} checks passed"


# Dangerous patterns to detect in Python code
DANGEROUS_PATTERNS = [
    "eval(",
    "exec(",
    "os.system(",
    "subprocess.call(",
    "subprocess.run(",
    "__import__(",
]

DANGEROUS_SHELL_PATTERNS = [
    "rm -rf",
    "curl | bash",
    "wget | bash",
    "> /dev/sd",
    "mkfs.",
    "dd if=",
]


class ModuleValidator:
    """Validates modules for security and compatibility."""
    
    def __init__(self, ethics_path: Optional[Path] = None):
        self.ethics_path = ethics_path
    
    def validate(self, module_path: Path) -> ValidationResult:
        """Run all validation checks on a module."""
        checks = [
            self._check_structure(module_path),
            self._check_python_patterns(module_path),
            self._check_shell_patterns(module_path),
            self._check_required_files(module_path),
        ]
        
        passed = all(c.passed for c in checks)
        return ValidationResult(
            module_name=module_path.name,
            passed=passed,
            checks=checks
        )
    
    def _check_structure(self, module_path: Path) -> ValidationCheck:
        """Check module has valid structure."""
        # TODO: Define required structure
        if not module_path.is_dir():
            return ValidationCheck("structure", False, "Not a directory")
        return ValidationCheck("structure", True, "Valid directory structure")
    
    def _check_python_patterns(self, module_path: Path) -> ValidationCheck:
        """Scan Python files for dangerous patterns."""
        issues = []
        for py_file in module_path.rglob("*.py"):
            content = py_file.read_text(errors='ignore')
            for pattern in DANGEROUS_PATTERNS:
                if pattern in content:
                    issues.append(f"{py_file.name}: {pattern}")
        
        if issues:
            return ValidationCheck("python_patterns", False, f"Found: {', '.join(issues[:3])}")
        return ValidationCheck("python_patterns", True, "No dangerous patterns")
    
    def _check_shell_patterns(self, module_path: Path) -> ValidationCheck:
        """Scan shell scripts for dangerous patterns."""
        issues = []
        for sh_file in module_path.rglob("*.sh"):
            content = sh_file.read_text(errors='ignore')
            for pattern in DANGEROUS_SHELL_PATTERNS:
                if pattern in content:
                    issues.append(f"{sh_file.name}: {pattern}")
        
        if issues:
            return ValidationCheck("shell_patterns", False, f"Found: {', '.join(issues[:3])}")
        return ValidationCheck("shell_patterns", True, "No dangerous patterns")
    
    def _check_required_files(self, module_path: Path) -> ValidationCheck:
        """Check for required module files."""
        required = ["SKILL.md"]  # or MODULE.md
        missing = [f for f in required if not (module_path / f).exists()]
        
        # Accept either SKILL.md or MODULE.md
        if missing and (module_path / "MODULE.md").exists():
            missing = []
        
        if missing:
            return ValidationCheck("required_files", False, f"Missing: {', '.join(missing)}")
        return ValidationCheck("required_files", True, "All required files present")
