"""
Project Management for Maynord Calculator
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


@dataclass
class Project:
    """Project data model"""
    name: str = "Sans titre"
    engineer: str = ""
    date: str = ""
    location: str = ""
    notes: str = ""
    calculations: List[Dict] = field(default_factory=list)
    created_at: str = ""
    modified_at: str = ""

    def __post_init__(self):
        if not self.date:
            self.date = datetime.now().strftime("%Y-%m-%d")
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        """Create from dictionary"""
        return cls(**data)


class ProjectManager:
    """Manages project loading, saving, and state"""

    def __init__(self):
        self.project = Project()
        self.filepath: Optional[str] = None
        self.is_modified: bool = False

    def new_project(self):
        """Create a new empty project"""
        self.project = Project()
        self.filepath = None
        self.is_modified = False

    def load(self, filepath: str):
        """Load project from file"""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Fichier non trouvé: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.project = Project.from_dict(data)
        self.filepath = filepath
        self.is_modified = False

    def save(self, filepath: Optional[str] = None):
        """Save project to file"""
        if filepath:
            self.filepath = filepath

        if not self.filepath:
            raise ValueError("Aucun chemin de fichier spécifié")

        # Update modified timestamp
        self.project.modified_at = datetime.now().isoformat()

        # Ensure .maynord extension
        if not self.filepath.endswith('.maynord'):
            self.filepath += '.maynord'

        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.project.to_dict(), f, indent=2, ensure_ascii=False)

        self.is_modified = False

    def add_calculation(self, calc_data: dict):
        """Add a calculation to history"""
        calc_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.project.calculations.append(calc_data)
        self.is_modified = True

        # Keep only last 100 calculations
        if len(self.project.calculations) > 100:
            self.project.calculations = self.project.calculations[-100:]

    def get_last_calculation(self) -> Optional[dict]:
        """Get the most recent calculation"""
        if self.project.calculations:
            return self.project.calculations[-1]
        return None

    def clear_calculations(self):
        """Clear all calculations"""
        self.project.calculations = []
        self.is_modified = True
