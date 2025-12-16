"""
Project Tab - Project management and history
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QTextEdit, QGroupBox,
    QListWidget, QListWidgetItem, QPushButton
)
from PySide6.QtCore import Qt
from datetime import datetime

from resources.translations import tr


class ProjectTab(QWidget):
    """Tab for project management"""

    def __init__(self, project_manager):
        super().__init__()
        self.project_manager = project_manager
        self.current_theme = "light"
        self.setup_ui()

    def set_theme(self, theme: str):
        """Set the current theme"""
        self.current_theme = theme

    def setup_ui(self):
        """Setup the project UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Left panel - Project info
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # Project details group
        info_group = QGroupBox(tr('project.title'))
        info_layout = QGridLayout(info_group)

        info_layout.addWidget(QLabel(tr('project.name')), 0, 0)
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Nom du projet")
        self.name_edit.textChanged.connect(self.on_info_changed)
        info_layout.addWidget(self.name_edit, 0, 1)

        info_layout.addWidget(QLabel(tr('project.engineer')), 1, 0)
        self.engineer_edit = QLineEdit()
        self.engineer_edit.setPlaceholderText("Nom de l'ingénieur")
        self.engineer_edit.textChanged.connect(self.on_info_changed)
        info_layout.addWidget(self.engineer_edit, 1, 1)

        info_layout.addWidget(QLabel(tr('project.date')), 2, 0)
        self.date_edit = QLineEdit()
        self.date_edit.setText(datetime.now().strftime("%Y-%m-%d"))
        self.date_edit.textChanged.connect(self.on_info_changed)
        info_layout.addWidget(self.date_edit, 2, 1)

        info_layout.addWidget(QLabel(tr('project.location')), 3, 0)
        self.location_edit = QLineEdit()
        self.location_edit.setPlaceholderText("Localisation du projet")
        self.location_edit.textChanged.connect(self.on_info_changed)
        info_layout.addWidget(self.location_edit, 3, 1)

        left_layout.addWidget(info_group)

        # Notes group
        notes_group = QGroupBox(tr('project.notes'))
        notes_layout = QVBoxLayout(notes_group)
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Notes et commentaires...")
        self.notes_edit.textChanged.connect(self.on_info_changed)
        notes_layout.addWidget(self.notes_edit)
        left_layout.addWidget(notes_group)

        layout.addWidget(left_panel, 1)

        # Right panel - History
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        history_group = QGroupBox(tr('project.history'))
        history_layout = QVBoxLayout(history_group)

        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.on_history_clicked)
        history_layout.addWidget(self.history_list)

        # History buttons
        btn_layout = QHBoxLayout()
        self.export_history_btn = QPushButton("Exporter")
        self.export_history_btn.clicked.connect(self.export_history)
        btn_layout.addWidget(self.export_history_btn)

        self.clear_history_btn = QPushButton("Effacer")
        self.clear_history_btn.clicked.connect(self.clear_history)
        btn_layout.addWidget(self.clear_history_btn)
        history_layout.addLayout(btn_layout)

        right_layout.addWidget(history_group)

        # Selected calculation details
        details_group = QGroupBox("Détails du calcul sélectionné")
        details_layout = QVBoxLayout(details_group)
        self.details_label = QLabel("Sélectionnez un calcul dans l'historique")
        self.details_label.setWordWrap(True)
        self.details_label.setStyleSheet("color: #64748b;")
        details_layout.addWidget(self.details_label)
        right_layout.addWidget(details_group)

        layout.addWidget(right_panel, 1)

        self.apply_styles()
        self.refresh()

    def on_info_changed(self):
        """Handle project info changes"""
        project = self.project_manager.project
        project.name = self.name_edit.text()
        project.engineer = self.engineer_edit.text()
        project.date = self.date_edit.text()
        project.location = self.location_edit.text()
        project.notes = self.notes_edit.toPlainText()
        self.project_manager.is_modified = True

    def refresh(self):
        """Refresh project data"""
        project = self.project_manager.project

        # Block signals to prevent triggering on_info_changed
        self.name_edit.blockSignals(True)
        self.engineer_edit.blockSignals(True)
        self.date_edit.blockSignals(True)
        self.location_edit.blockSignals(True)
        self.notes_edit.blockSignals(True)

        self.name_edit.setText(project.name or "")
        self.engineer_edit.setText(project.engineer or "")
        self.date_edit.setText(project.date or datetime.now().strftime("%Y-%m-%d"))
        self.location_edit.setText(project.location or "")
        self.notes_edit.setPlainText(project.notes or "")

        self.name_edit.blockSignals(False)
        self.engineer_edit.blockSignals(False)
        self.date_edit.blockSignals(False)
        self.location_edit.blockSignals(False)
        self.notes_edit.blockSignals(False)

        # Refresh history
        self.history_list.clear()
        for i, calc in enumerate(project.calculations):
            timestamp = calc.get('timestamp', 'N/A')
            v = calc.get('velocity', 0)
            d = calc.get('depth', 0)
            d30 = calc.get('result', {}).get('d30_mm', 0)

            item = QListWidgetItem(f"#{i+1} | V={v}m/s D={d}m → D30={d30:.0f}mm | {timestamp}")
            item.setData(Qt.UserRole, calc)
            self.history_list.addItem(item)

    def on_history_clicked(self, item):
        """Show details of selected calculation"""
        calc = item.data(Qt.UserRole)
        if calc:
            result = calc.get('result', {})
            coeffs = calc.get('coefficients', {})

            details = f"""
<b>Paramètres d'entrée:</b><br>
• Vitesse: {calc.get('velocity', 'N/A')} m/s<br>
• Profondeur: {calc.get('depth', 'N/A')} m<br>
<br>
<b>Coefficients:</b><br>
• SF: {coeffs.get('SF', 'N/A')}<br>
• Cs: {coeffs.get('Cs', 'N/A')}<br>
• Cv: {coeffs.get('Cv', 'N/A')}<br>
• K1: {coeffs.get('K1', 'N/A')}<br>
<br>
<b>Résultats:</b><br>
• D30: {result.get('d30_mm', 'N/A')} mm<br>
• D50: {result.get('d50_mm', 'N/A')} mm<br>
• D100: {result.get('d100_mm', 'N/A')} mm<br>
• Épaisseur: {result.get('thickness_cm', 'N/A')} cm<br>
• Froude: {result.get('froude', 'N/A')}<br>
            """
            self.details_label.setText(details)
            self.details_label.setStyleSheet("color: #1e293b;")

    def export_history(self):
        """Export calculation history"""
        # Will be implemented with export module
        pass

    def clear_history(self):
        """Clear calculation history"""
        self.project_manager.project.calculations = []
        self.history_list.clear()
        self.details_label.setText("Sélectionnez un calcul dans l'historique")
        self.details_label.setStyleSheet("color: #64748b;")

    def refresh_labels(self):
        """Refresh labels after language change"""
        pass  # TODO: Implement i18n for all labels

    def apply_styles(self):
        """Apply styles - styles are inherited from main app theme"""
        # Styles are now handled by the main app theme
        pass
