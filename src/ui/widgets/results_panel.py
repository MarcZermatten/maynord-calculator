"""
Results Panel Widget - Responsive display of calculation results
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt

from core.maynord import MaynordResult
from core.gradation import get_complete_gradation_summary
from resources.translations import tr


class ResultCard(QFrame):
    """A card displaying a single result value"""

    def __init__(self, title: str, unit: str = "", color: str = "#1e40af"):
        super().__init__()
        self.setObjectName("resultCard")
        self.color = color

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)

        # Title
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: bold;")
        layout.addWidget(self.title_label)

        # Value
        self.value_label = QLabel("--")
        self.value_label.setObjectName("resultValue")
        self.value_label.setStyleSheet("""
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 20px;
            font-weight: bold;
        """)
        layout.addWidget(self.value_label)

        # Unit
        if unit:
            self.unit_label = QLabel(unit)
            self.unit_label.setStyleSheet("color: #64748b; font-size: 10px;")
            layout.addWidget(self.unit_label)
        else:
            self.unit_label = None

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def set_value(self, value: str, unit: str = None):
        """Set the displayed value"""
        self.value_label.setText(value)
        if unit and self.unit_label:
            self.unit_label.setText(unit)


class ResultsPanel(QWidget):
    """Responsive panel displaying Maynord calculation results"""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Setup the responsive results panel"""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header with title and status
        header = QHBoxLayout()
        header.setSpacing(15)

        title = QLabel("📋 Resultats")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        header.addWidget(title)

        # Status indicator
        self.status_frame = QFrame()
        self.status_frame.setMinimumWidth(120)
        status_layout = QHBoxLayout(self.status_frame)
        status_layout.setContentsMargins(15, 8, 15, 8)

        self.status_icon = QLabel("●")
        self.status_icon.setStyleSheet("font-size: 18px;")
        status_layout.addWidget(self.status_icon)

        self.status_label = QLabel("En attente...")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        status_layout.addWidget(self.status_label)

        self.set_status("waiting", "En attente...")
        header.addWidget(self.status_frame)
        header.addStretch()

        layout.addLayout(header)

        # Main results frame
        results_frame = QFrame()
        results_frame.setObjectName("resultsFrame")
        results_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        results_layout = QVBoxLayout(results_frame)
        results_layout.setSpacing(15)
        results_layout.setContentsMargins(15, 15, 15, 15)

        # Section 1: Diameters (main results)
        diam_section = QLabel("DIAMETRES CARACTERISTIQUES")
        diam_section.setStyleSheet("color: #1e40af; font-weight: bold; font-size: 12px;")
        results_layout.addWidget(diam_section)

        diam_grid = QHBoxLayout()
        diam_grid.setSpacing(15)

        self.d30_card = ResultCard("D30 (calcule)", "mm", "#2563eb")
        self.d50_card = ResultCard("D50 (estime)", "mm", "#16a34a")
        self.d100_card = ResultCard("D100 (max)", "mm", "#dc2626")

        diam_grid.addWidget(self.d30_card)
        diam_grid.addWidget(self.d50_card)
        diam_grid.addWidget(self.d100_card)
        results_layout.addLayout(diam_grid)

        # Section 2: Masses
        mass_section = QLabel("MASSES UNITAIRES")
        mass_section.setStyleSheet("color: #1e40af; font-weight: bold; font-size: 12px;")
        results_layout.addWidget(mass_section)

        mass_grid = QHBoxLayout()
        mass_grid.setSpacing(15)

        self.mass_d30_card = ResultCard("Masse D30", "kg", "#2563eb")
        self.mass_d50_card = ResultCard("Masse D50", "kg", "#16a34a")
        self.mass_d100_card = ResultCard("Masse D100", "kg", "#dc2626")

        mass_grid.addWidget(self.mass_d30_card)
        mass_grid.addWidget(self.mass_d50_card)
        mass_grid.addWidget(self.mass_d100_card)
        results_layout.addLayout(mass_grid)

        # Section 3: Other results
        other_section = QLabel("AUTRES PARAMETRES")
        other_section.setStyleSheet("color: #1e40af; font-weight: bold; font-size: 12px;")
        results_layout.addWidget(other_section)

        other_grid = QHBoxLayout()
        other_grid.setSpacing(15)

        self.thickness_card = ResultCard("Epaisseur couche", "cm", "#f59e0b")
        self.class_card = ResultCard("Classe USACE", "", "#8b5cf6")
        self.froude_card = ResultCard("Nombre Froude", "", "#64748b")
        self.mass_m2_card = ResultCard("Masse/surface", "kg/m²", "#0ea5e9")

        other_grid.addWidget(self.thickness_card)
        other_grid.addWidget(self.class_card)
        other_grid.addWidget(self.froude_card)
        other_grid.addWidget(self.mass_m2_card)
        results_layout.addLayout(other_grid)

        results_layout.addStretch()
        layout.addWidget(results_frame, 1)

        # Warnings frame
        self.warnings_frame = QFrame()
        self.warnings_frame.setObjectName("warningsFrame")
        self.warnings_frame.setMaximumHeight(50)
        warnings_layout = QHBoxLayout(self.warnings_frame)
        warnings_layout.setContentsMargins(15, 10, 15, 10)
        self.warnings_label = QLabel()
        self.warnings_label.setWordWrap(True)
        self.warnings_label.setStyleSheet("font-size: 12px;")
        warnings_layout.addWidget(self.warnings_label)
        self.warnings_frame.hide()
        layout.addWidget(self.warnings_frame)

        # Create label references for compatibility
        self.d30_label = self.d30_card.value_label
        self.d50_label = self.d50_card.value_label
        self.d100_label = self.d100_card.value_label
        self.mass_d30_label = self.mass_d30_card.value_label
        self.mass_d50_label = self.mass_d50_card.value_label
        self.mass_d100_label = self.mass_d100_card.value_label
        self.thickness_label = self.thickness_card.value_label
        self.class_label = self.class_card.value_label
        self.froude_label = self.froude_card.value_label
        self.mass_m2_label = self.mass_m2_card.value_label

    def update_results(self, result: MaynordResult):
        """Update the panel with calculation results"""
        # Status
        if result.froude_number > 1.2:
            self.set_status("warning", "⚠️ LIMITE")
        elif result.d100 > 1500:
            self.set_status("warning", "⚠️ GROS BLOCS")
        else:
            self.set_status("stable", "✅ STABLE")

        # Diameters
        self.d30_card.set_value(f"{result.d30:.1f}")
        self.d50_card.set_value(f"{result.d50:.1f}")
        self.d100_card.set_value(f"{result.d100:.1f}")

        # Masses
        self.mass_d30_card.set_value(*self._format_mass(result.mass_d30))
        self.mass_d50_card.set_value(*self._format_mass(result.mass_d50))
        self.mass_d100_card.set_value(*self._format_mass(result.mass_d100))

        # Other
        self.thickness_card.set_value(f"{result.thickness:.1f}")
        self.froude_card.set_value(f"{result.froude_number:.3f}")

        # Gradation class
        summary = get_complete_gradation_summary(result.d30, result.coefficients.get('Ss', 2.65))
        self.class_card.set_value(summary.usace_class)
        self.mass_m2_card.set_value(f"{summary.mass_per_m2:.0f}")

        # Warnings
        if result.warnings:
            self.warnings_label.setText("⚠️ " + " | ".join(result.warnings))
            self.warnings_frame.setStyleSheet("""
                QFrame#warningsFrame {
                    background: #fef3c7;
                    border: 1px solid #f59e0b;
                    border-radius: 6px;
                }
            """)
            self.warnings_label.setStyleSheet("color: #92400e; font-size: 12px;")
            self.warnings_frame.show()
        else:
            self.warnings_frame.hide()

    def _format_mass(self, mass_kg: float) -> tuple:
        """Format mass with appropriate unit, returns (value, unit)"""
        if mass_kg >= 1000:
            return (f"{mass_kg/1000:.2f}", "t")
        else:
            return (f"{mass_kg:.1f}", "kg")

    def set_status(self, status: str, text: str):
        """Set the status indicator"""
        if status == "stable":
            self.status_frame.setStyleSheet("""
                QFrame {
                    background: #dcfce7;
                    border: 2px solid #16a34a;
                    border-radius: 8px;
                }
            """)
            self.status_icon.setStyleSheet("font-size: 18px; color: #16a34a;")
            self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #16a34a;")
        elif status == "warning":
            self.status_frame.setStyleSheet("""
                QFrame {
                    background: #fef3c7;
                    border: 2px solid #f59e0b;
                    border-radius: 8px;
                }
            """)
            self.status_icon.setStyleSheet("font-size: 18px; color: #f59e0b;")
            self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #d97706;")
        elif status == "error":
            self.status_frame.setStyleSheet("""
                QFrame {
                    background: #fee2e2;
                    border: 2px solid #dc2626;
                    border-radius: 8px;
                }
            """)
            self.status_icon.setStyleSheet("font-size: 18px; color: #dc2626;")
            self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #dc2626;")
        else:  # waiting
            self.status_frame.setStyleSheet("""
                QFrame {
                    background: #f1f5f9;
                    border: 2px solid #cbd5e1;
                    border-radius: 8px;
                }
            """)
            self.status_icon.setStyleSheet("font-size: 18px; color: #94a3b8;")
            self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #64748b;")

        self.status_label.setText(text)

    def show_error(self, message: str):
        """Show error message"""
        self.set_status("error", "❌ ERREUR")
        self.warnings_label.setText(f"❌ {message}")
        self.warnings_frame.setStyleSheet("""
            QFrame#warningsFrame {
                background: #fee2e2;
                border: 1px solid #dc2626;
                border-radius: 6px;
            }
        """)
        self.warnings_label.setStyleSheet("color: #dc2626; font-size: 12px;")
        self.warnings_frame.show()

    def clear(self):
        """Clear all results"""
        self.set_status("waiting", "En attente...")

        for card in [self.d30_card, self.d50_card, self.d100_card,
                     self.mass_d30_card, self.mass_d50_card, self.mass_d100_card,
                     self.thickness_card, self.class_card, self.froude_card, self.mass_m2_card]:
            card.set_value("--")

        self.warnings_frame.hide()
