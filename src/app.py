"""
Maynord Calculator - Main Application Window
Refactored with proper UI, dark mode, and complete features
"""

import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QLabel, QStatusBar,
    QMenuBar, QMenu, QMessageBox, QFileDialog, QFrame
)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QAction, QIcon, QPixmap, QFont

from ui.calculator_tab import CalculatorTab
from ui.comparison_tab import ComparisonTab
from ui.settings_dialog import SettingsDialog
from resources.translations import tr, set_language, Language, get_language
from data.project import ProjectManager
from data.export import export_calculation_to_excel, export_calculation_to_pdf


class MaynordApp(QMainWindow):
    """Main application window"""

    theme_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.project_manager = ProjectManager()
        self.current_theme = "light"
        self.setup_ui()
        self.setup_menu()
        self.setup_statusbar()
        self.apply_theme("light")

    def setup_ui(self):
        """Setup the main UI"""
        self.setWindowTitle(f"{tr('app.title')} - {tr('app.subtitle')}")
        self.setMinimumSize(1100, 750)
        self.resize(1250, 850)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = self.create_header()
        layout.addWidget(header)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(False)
        self.tabs.setTabPosition(QTabWidget.North)

        # Create tabs
        self.calculator_tab = CalculatorTab(self.project_manager)
        self.comparison_tab = ComparisonTab(self.project_manager)

        # Connect export signals from calculator tab
        self.calculator_tab.export_excel_requested.connect(self.export_excel)
        self.calculator_tab.export_pdf_requested.connect(self.export_pdf)

        # Connect add to comparison signal
        self.calculator_tab.add_to_comparison_requested.connect(self.add_to_comparison)

        # Connect theme change to update all tabs
        self.theme_changed.connect(self.calculator_tab.on_theme_changed)
        self.theme_changed.connect(self.comparison_tab.set_theme)

        self.tabs.addTab(self.calculator_tab, "  Calculateur  ")
        self.tabs.addTab(self.comparison_tab, "  Comparaison  ")

        layout.addWidget(self.tabs, 1)

    def create_header(self) -> QWidget:
        """Create the header bar"""
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(60)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 10, 20, 10)

        # Logo/Title
        title_layout = QHBoxLayout()
        title_layout.setSpacing(10)

        icon_label = QLabel("🪨")
        icon_label.setStyleSheet("font-size: 24px;")
        title_layout.addWidget(icon_label)

        title = QLabel(tr('app.title'))
        title.setObjectName("headerTitle")
        title_layout.addWidget(title)

        layout.addLayout(title_layout)
        layout.addStretch()

        # Theme toggle button
        self.theme_btn = QPushButton("🌙")
        self.theme_btn.setObjectName("themeButton")
        self.theme_btn.setFixedSize(40, 40)
        self.theme_btn.setToolTip("Basculer mode sombre/clair")
        self.theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_btn)

        # Language toggle
        self.lang_btn = QPushButton("FR | EN")
        self.lang_btn.setObjectName("headerButton")
        self.lang_btn.setFixedWidth(80)
        self.lang_btn.clicked.connect(self.toggle_language)
        layout.addWidget(self.lang_btn)

        # Settings button
        settings_btn = QPushButton("⚙ Paramètres")
        settings_btn.setObjectName("headerButton")
        settings_btn.clicked.connect(self.show_settings)
        layout.addWidget(settings_btn)

        return header

    def setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&Fichier")

        new_action = QAction("Nouveau projet", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)

        open_action = QAction("Ouvrir...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)

        save_action = QAction("Sauvegarder", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)

        save_as_action = QAction("Sauvegarder sous...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        export_excel = QAction("Exporter Excel...", self)
        export_excel.triggered.connect(self._menu_export_excel)
        file_menu.addAction(export_excel)

        export_pdf = QAction("Exporter PDF...", self)
        export_pdf.triggered.connect(self._menu_export_pdf)
        file_menu.addAction(export_pdf)

        file_menu.addSeparator()

        quit_action = QAction("Quitter", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # Help menu
        help_menu = menubar.addMenu("&Aide")

        about_action = QAction("À propos...", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        refs_action = QAction("Références...", self)
        refs_action.triggered.connect(self.show_references)
        help_menu.addAction(refs_action)

    def setup_statusbar(self):
        """Setup status bar"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.status_label = QLabel("Prêt")
        self.statusbar.addWidget(self.status_label, 1)

        self.statusbar.addPermanentWidget(QLabel("Maynord Calculator v1.0"))

    def toggle_theme(self):
        """Toggle between light and dark theme"""
        new_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(new_theme)

    def apply_theme(self, theme: str):
        """Apply the specified theme"""
        self.current_theme = theme

        if theme == "dark":
            self.theme_btn.setText("☀️")
            self.setStyleSheet(DARK_THEME)
        else:
            self.theme_btn.setText("🌙")
            self.setStyleSheet(LIGHT_THEME)

        self.theme_changed.emit(theme)

    def toggle_language(self):
        """Toggle between FR and EN"""
        current = get_language()
        new_lang = Language.EN if current == Language.FR else Language.FR
        set_language(new_lang)
        self.refresh_ui()

    def refresh_ui(self):
        """Refresh UI after language change"""
        self.setWindowTitle(f"{tr('app.title')} - {tr('app.subtitle')}")
        self.tabs.setTabText(0, "  " + tr('tabs.calculator') + "  ")
        self.tabs.setTabText(1, "  " + tr('tabs.comparison') + "  ")
        self.calculator_tab.refresh_labels()
        self.comparison_tab.refresh_labels()

    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self, self.current_theme)
        if dialog.exec():
            self.refresh_ui()

    def new_project(self):
        """Create new project"""
        if self.project_manager.is_modified:
            reply = QMessageBox.question(
                self, "Nouveau projet",
                "Le projet actuel n'est pas sauvegardé. Continuer?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        self.project_manager.new_project()
        self.calculator_tab.reset()
        self.status_label.setText("Nouveau projet créé")

    def open_project(self):
        """Open existing project"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir un projet",
            "", "Projets Maynord (*.maynord *.json)"
        )
        if filename:
            try:
                self.project_manager.load(filename)
                self.status_label.setText(f"Projet chargé: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de charger: {e}")

    def save_project(self):
        """Save current project"""
        if self.project_manager.filepath:
            self.project_manager.save()
            self.status_label.setText("Projet sauvegardé")
        else:
            self.save_project_as()

    def save_project_as(self):
        """Save project with new filename"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Sauvegarder le projet",
            "", "Projets Maynord (*.maynord)"
        )
        if filename:
            if not filename.endswith('.maynord'):
                filename += '.maynord'
            self.project_manager.save(filename)
            self.status_label.setText(f"Projet sauvegardé: {filename}")

    def export_excel(self, result, input_params):
        """Export current calculation to Excel"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Exporter le rapport en Excel",
            "rapport_maynord.xlsx", "Fichiers Excel (*.xlsx)"
        )
        if filename:
            if not filename.endswith('.xlsx'):
                filename += '.xlsx'
            try:
                export_calculation_to_excel(result, input_params, filename)
                self.status_label.setText(f"Rapport exporte: {filename}")
                QMessageBox.information(self, "Export", "Rapport Excel exporte avec succes!")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur d'export: {e}")

    def export_pdf(self, result, input_params, chart_path):
        """Export current calculation to PDF"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Exporter le rapport en PDF",
            "rapport_maynord.pdf", "Fichiers PDF (*.pdf)"
        )
        if filename:
            if not filename.endswith('.pdf'):
                filename += '.pdf'
            try:
                export_calculation_to_pdf(result, input_params, filename, chart_path)
                self.status_label.setText(f"Rapport exporte: {filename}")
                QMessageBox.information(self, "Export", "Rapport PDF exporte avec succes!")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur d'export: {e}")

    def add_to_comparison(self, calc_data):
        """Add calculation to comparison tab"""
        self.comparison_tab.add_calculation_from_calculator(calc_data)
        self.tabs.setCurrentWidget(self.comparison_tab)
        self.status_label.setText("Calcul ajoute a la comparaison")

    def _menu_export_excel(self):
        """Export from menu - uses current calculator state"""
        if self.calculator_tab.last_result:
            self.export_excel(
                self.calculator_tab.last_result,
                self.calculator_tab.get_input_params()
            )
        else:
            QMessageBox.warning(self, "Export", "Effectuez d'abord un calcul.")

    def _menu_export_pdf(self):
        """Export from menu - uses current calculator state"""
        if self.calculator_tab.last_result:
            import tempfile
            import os
            temp_chart = os.path.join(tempfile.gettempdir(), 'maynord_chart.png')
            self.calculator_tab.save_chart_image(temp_chart)
            self.export_pdf(
                self.calculator_tab.last_result,
                self.calculator_tab.get_input_params(),
                temp_chart
            )
        else:
            QMessageBox.warning(self, "Export", "Effectuez d'abord un calcul.")

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "À propos",
            f"""<h2>🪨 Maynord Calculator</h2>
            <p><b>Version:</b> 1.0.0</p>
            <p>Application de dimensionnement d'enrochements<br>
            selon la méthode USACE/Maynord.</p>
            <hr>
            <p><b>Développé par:</b> Marc Zermatten</p>
            <p>© 2025</p>
            """
        )

    def show_references(self):
        """Show technical references"""
        QMessageBox.information(
            self,
            "Références techniques",
            """<h3>Équation de Maynord</h3>
            <p><code>d30 = SF × Cs × Cv × CT × D × [V/√(gD(Ss-1))]^2.5 / K1</code></p>

            <h4>Références:</h4>
            <ul>
                <li>Maynord, S.T. (1988) - Technical Report HL-88-4</li>
                <li>USACE EM 1110-2-1601</li>
                <li>HEC-RAS Hydraulic Reference Manual</li>
            </ul>
            """
        )


# ============== THEMES ==============

LIGHT_THEME = """
QMainWindow {
    background-color: #f0f4f8;
}
QMenuBar {
    background: #1e40af;
    color: white;
    padding: 2px;
}
QMenuBar::item {
    background: transparent;
    padding: 4px 10px;
}
QMenuBar::item:selected {
    background: #3b82f6;
}
QMenu {
    background: white;
    color: #1e293b;
    border: 1px solid #e2e8f0;
}
QMenu::item:selected {
    background: #2563eb;
    color: white;
}
QScrollArea {
    background: transparent;
    border: none;
}
QScrollArea > QWidget > QWidget {
    background: transparent;
}
#header {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #1e40af, stop:1 #3b82f6);
    border-bottom: 3px solid #1e3a8a;
}
#headerTitle {
    color: white;
    font-size: 20px;
    font-weight: bold;
}
#headerButton, #themeButton {
    background-color: rgba(255,255,255,0.2);
    color: white;
    border: 1px solid rgba(255,255,255,0.3);
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: bold;
}
#headerButton:hover, #themeButton:hover {
    background-color: rgba(255,255,255,0.3);
}
#themeButton {
    font-size: 18px;
    padding: 0;
}
QTabWidget::pane {
    border: none;
    background: #f0f4f8;
    padding: 10px;
}
QTabBar::tab {
    background: #e2e8f0;
    color: #475569;
    padding: 12px 24px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: bold;
    font-size: 13px;
}
QTabBar::tab:selected {
    background: white;
    color: #1e40af;
    border-bottom: 3px solid #2563eb;
}
QTabBar::tab:hover:!selected {
    background: #cbd5e1;
}
QGroupBox {
    font-weight: bold;
    font-size: 13px;
    border: 2px solid #e2e8f0;
    border-radius: 10px;
    margin-top: 12px;
    padding: 15px;
    padding-top: 25px;
    background: white;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 8px;
    color: #1e40af;
    background: white;
}
QLabel {
    color: #334155;
    font-size: 13px;
}
QDoubleSpinBox, QSpinBox, QComboBox, QLineEdit {
    padding: 8px 12px;
    border: 2px solid #cbd5e1;
    border-radius: 6px;
    background: white;
    color: #1e293b;
    font-size: 13px;
    min-width: 120px;
    selection-background-color: #2563eb;
    selection-color: white;
}
QDoubleSpinBox:focus, QSpinBox:focus, QComboBox:focus, QLineEdit:focus {
    border-color: #2563eb;
}
QDoubleSpinBox::up-button, QSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #cbd5e1;
    background: #f1f5f9;
}
QDoubleSpinBox::down-button, QSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 20px;
    border-left: 1px solid #cbd5e1;
    background: #f1f5f9;
}
QDoubleSpinBox::up-arrow, QSpinBox::up-arrow {
    width: 8px;
    height: 8px;
}
QDoubleSpinBox::down-arrow, QSpinBox::down-arrow {
    width: 8px;
    height: 8px;
}
QComboBox::drop-down {
    border: none;
    width: 30px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #64748b;
    margin-right: 10px;
}
QPushButton {
    padding: 10px 20px;
    border: 2px solid #cbd5e1;
    border-radius: 6px;
    background: white;
    font-weight: bold;
    font-size: 13px;
    color: #475569;
}
QPushButton:hover {
    background: #f1f5f9;
    border-color: #94a3b8;
}
QPushButton#primaryButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3b82f6, stop:1 #2563eb);
    color: white;
    border: none;
    padding: 12px 30px;
    font-size: 14px;
}
QPushButton#primaryButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #2563eb, stop:1 #1d4ed8);
}
QPushButton#dangerButton {
    background: #fee2e2;
    color: #dc2626;
    border-color: #fecaca;
}
QPushButton#dangerButton:hover {
    background: #fecaca;
}
QRadioButton {
    spacing: 8px;
    font-size: 13px;
    color: #334155;
}
QRadioButton::indicator {
    width: 18px;
    height: 18px;
}
QSlider::groove:horizontal {
    height: 8px;
    background: #e2e8f0;
    border-radius: 4px;
}
QSlider::handle:horizontal {
    background: #2563eb;
    width: 20px;
    margin: -6px 0;
    border-radius: 10px;
}
QSlider::sub-page:horizontal {
    background: #2563eb;
    border-radius: 4px;
}
QStatusBar {
    background: #e2e8f0;
    border-top: 1px solid #cbd5e1;
    color: #475569;
    padding: 5px;
}
QTableWidget {
    background: white;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    gridline-color: #f1f5f9;
}
QTableWidget::item {
    padding: 8px;
}
QHeaderView::section {
    background: #f1f5f9;
    padding: 10px;
    border: none;
    border-bottom: 2px solid #e2e8f0;
    font-weight: bold;
    color: #475569;
}
QTextEdit {
    border: 2px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px;
    background: white;
}
QListWidget {
    border: 2px solid #e2e8f0;
    border-radius: 6px;
    background: white;
}
QListWidget::item {
    padding: 10px;
    border-bottom: 1px solid #f1f5f9;
}
QListWidget::item:selected {
    background: #dbeafe;
    color: #1e40af;
}
QScrollBar:vertical {
    background: #f1f5f9;
    width: 12px;
    border-radius: 6px;
}
QScrollBar::handle:vertical {
    background: #cbd5e1;
    border-radius: 6px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #94a3b8;
}
QSplitter::handle {
    background: #e2e8f0;
    border-radius: 2px;
}
QSplitter::handle:horizontal {
    width: 6px;
    margin: 20px 2px;
}
QSplitter::handle:vertical {
    height: 6px;
    margin: 2px 20px;
}
QSplitter::handle:hover {
    background: #2563eb;
}
QFrame#resultsFrame {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
}
QFrame#coeffDisplay {
    background: #f1f5f9;
    border-radius: 6px;
}
QFrame#resultCard {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 4px;
}
QFrame#resultCard:hover {
    border-color: #2563eb;
    background: #f8fafc;
}
QLabel#resultValue {
    color: #1e293b;
}
QFrame#warningsFrame {
    background: #fef3c7;
    border: 1px solid #f59e0b;
    border-radius: 6px;
}
QFrame#comparisonSummary {
    background: #dbeafe;
    border: 1px solid #3b82f6;
    border-radius: 6px;
    padding: 8px;
}
QFrame#comparisonSummary QLabel {
    color: #1e40af;
    font-weight: bold;
    font-size: 11px;
}
"""

DARK_THEME = """
QMainWindow {
    background-color: #0f172a;
}
#header {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #1e293b, stop:1 #334155);
    border-bottom: 3px solid #0ea5e9;
}
#headerTitle {
    color: #0ea5e9;
    font-size: 20px;
    font-weight: bold;
}
#headerButton, #themeButton {
    background-color: rgba(14, 165, 233, 0.2);
    color: #0ea5e9;
    border: 1px solid rgba(14, 165, 233, 0.3);
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: bold;
}
#headerButton:hover, #themeButton:hover {
    background-color: rgba(14, 165, 233, 0.3);
}
#themeButton {
    font-size: 18px;
    padding: 0;
}
QTabWidget::pane {
    border: none;
    background: #0f172a;
    padding: 10px;
}
QTabBar::tab {
    background: #1e293b;
    color: #64748b;
    padding: 12px 24px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: bold;
    font-size: 13px;
}
QTabBar::tab:selected {
    background: #334155;
    color: #0ea5e9;
    border-bottom: 3px solid #0ea5e9;
}
QTabBar::tab:hover:!selected {
    background: #293548;
}
QGroupBox {
    font-weight: bold;
    font-size: 13px;
    border: 2px solid #334155;
    border-radius: 10px;
    margin-top: 12px;
    padding: 15px;
    padding-top: 25px;
    background: #1e293b;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 8px;
    color: #0ea5e9;
    background: #1e293b;
}
QLabel {
    color: #cbd5e1;
    font-size: 13px;
}
QDoubleSpinBox, QSpinBox, QComboBox, QLineEdit {
    padding: 8px 12px;
    border: 2px solid #334155;
    border-radius: 6px;
    background: #1e293b;
    color: #e2e8f0;
    font-size: 13px;
    min-width: 120px;
    selection-background-color: #0ea5e9;
    selection-color: white;
}
QDoubleSpinBox:focus, QSpinBox:focus, QComboBox:focus, QLineEdit:focus {
    border-color: #0ea5e9;
}
QDoubleSpinBox::up-button, QSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #334155;
    background: #334155;
}
QDoubleSpinBox::down-button, QSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 20px;
    border-left: 1px solid #334155;
    background: #334155;
}
QDoubleSpinBox::up-arrow, QSpinBox::up-arrow {
    width: 8px;
    height: 8px;
}
QDoubleSpinBox::down-arrow, QSpinBox::down-arrow {
    width: 8px;
    height: 8px;
}
QComboBox::drop-down {
    border: none;
    width: 30px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #64748b;
    margin-right: 10px;
}
QComboBox QAbstractItemView {
    background: #1e293b;
    color: #e2e8f0;
    selection-background-color: #0ea5e9;
}
QPushButton {
    padding: 10px 20px;
    border: 2px solid #334155;
    border-radius: 6px;
    background: #1e293b;
    font-weight: bold;
    font-size: 13px;
    color: #cbd5e1;
}
QPushButton:hover {
    background: #334155;
    border-color: #475569;
}
QPushButton#primaryButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #0ea5e9, stop:1 #0284c7);
    color: white;
    border: none;
    padding: 12px 30px;
    font-size: 14px;
}
QPushButton#primaryButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #0284c7, stop:1 #0369a1);
}
QPushButton#dangerButton {
    background: #7f1d1d;
    color: #fca5a5;
    border-color: #991b1b;
}
QRadioButton {
    spacing: 8px;
    font-size: 13px;
    color: #cbd5e1;
}
QRadioButton::indicator {
    width: 18px;
    height: 18px;
}
QSlider::groove:horizontal {
    height: 8px;
    background: #334155;
    border-radius: 4px;
}
QSlider::handle:horizontal {
    background: #0ea5e9;
    width: 20px;
    margin: -6px 0;
    border-radius: 10px;
}
QSlider::sub-page:horizontal {
    background: #0ea5e9;
    border-radius: 4px;
}
QStatusBar {
    background: #1e293b;
    border-top: 1px solid #334155;
    color: #94a3b8;
    padding: 5px;
}
QTableWidget {
    background: #1e293b;
    border: 2px solid #334155;
    border-radius: 8px;
    gridline-color: #334155;
    color: #e2e8f0;
}
QTableWidget::item {
    padding: 8px;
}
QHeaderView::section {
    background: #334155;
    padding: 10px;
    border: none;
    border-bottom: 2px solid #475569;
    font-weight: bold;
    color: #cbd5e1;
}
QTextEdit {
    border: 2px solid #334155;
    border-radius: 6px;
    padding: 8px;
    background: #1e293b;
    color: #e2e8f0;
}
QListWidget {
    border: 2px solid #334155;
    border-radius: 6px;
    background: #1e293b;
    color: #e2e8f0;
}
QListWidget::item {
    padding: 10px;
    border-bottom: 1px solid #334155;
}
QListWidget::item:selected {
    background: #0c4a6e;
    color: #0ea5e9;
}
QScrollBar:vertical {
    background: #1e293b;
    width: 12px;
    border-radius: 6px;
}
QScrollBar::handle:vertical {
    background: #475569;
    border-radius: 6px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #64748b;
}
QMenuBar {
    background: #1e293b;
    color: #cbd5e1;
}
QMenuBar::item:selected {
    background: #334155;
}
QMenu {
    background: #1e293b;
    color: #cbd5e1;
    border: 1px solid #334155;
}
QMenu::item:selected {
    background: #0ea5e9;
    color: white;
}
QScrollArea {
    background: transparent;
    border: none;
}
QScrollArea > QWidget > QWidget {
    background: transparent;
}
QSplitter::handle {
    background: #334155;
    border-radius: 2px;
}
QSplitter::handle:horizontal {
    width: 6px;
    margin: 20px 2px;
}
QSplitter::handle:vertical {
    height: 6px;
    margin: 2px 20px;
}
QSplitter::handle:hover {
    background: #0ea5e9;
}
QFrame#resultsFrame {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
}
QFrame#coeffDisplay {
    background: #334155;
    border-radius: 6px;
}
QFrame#resultCard {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 4px;
}
QFrame#resultCard:hover {
    border-color: #0ea5e9;
    background: #293548;
}
QLabel#resultValue {
    color: #e2e8f0;
}
QFrame#warningsFrame {
    background: #422006;
    border: 1px solid #f59e0b;
    border-radius: 6px;
}
QFrame#comparisonSummary {
    background: #1e3a5f;
    border: 1px solid #0ea5e9;
    border-radius: 6px;
    padding: 8px;
}
QFrame#comparisonSummary QLabel {
    color: #7dd3fc;
    font-weight: bold;
    font-size: 11px;
}
"""
