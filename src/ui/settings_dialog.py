"""
Settings Dialog with Easter Egg
"""

import os
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QComboBox, QSpinBox, QGroupBox,
    QPushButton, QDialogButtonBox, QTabWidget, QWidget,
    QFrame
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QImage, QColor

from resources.translations import tr, set_language, get_language, Language


class ClickableLabel(QLabel):
    """Label that tracks consecutive clicks"""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.click_count = 0
        self.click_timer = QTimer()
        self.click_timer.timeout.connect(self.reset_clicks)
        self.click_timer.setSingleShot(True)
        self.on_easter_egg = None
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.click_count += 1
            self.click_timer.start(1500)  # Reset after 1.5s of no clicks

            if self.click_count >= 7 and self.on_easter_egg:
                self.on_easter_egg()
                self.click_count = 0
        super().mousePressEvent(event)

    def reset_clicks(self):
        self.click_count = 0


class SettingsDialog(QDialog):
    """Settings dialog with Easter egg"""

    def __init__(self, parent=None, current_theme="light"):
        super().__init__(parent)
        self.current_theme = current_theme
        self.easter_egg_active = False
        self.setWindowTitle(tr('settings.title'))
        self.setMinimumWidth(450)
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        tabs = QTabWidget()

        # General tab
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        general_layout.setSpacing(15)

        # Language
        lang_group = QGroupBox(tr('settings.language'))
        lang_layout = QHBoxLayout(lang_group)

        self.lang_combo = QComboBox()
        self.lang_combo.addItem("Francais", Language.FR)
        self.lang_combo.addItem("English", Language.EN)
        current = get_language()
        self.lang_combo.setCurrentIndex(0 if current == Language.FR else 1)
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()

        general_layout.addWidget(lang_group)

        # Precision
        precision_group = QGroupBox(tr('settings.precision'))
        precision_layout = QGridLayout(precision_group)
        precision_layout.setSpacing(10)

        precision_layout.addWidget(QLabel("Decimales diametres:"), 0, 0)
        self.diameter_precision = QSpinBox()
        self.diameter_precision.setRange(0, 3)
        self.diameter_precision.setValue(1)
        precision_layout.addWidget(self.diameter_precision, 0, 1)

        precision_layout.addWidget(QLabel("Decimales masses:"), 1, 0)
        self.mass_precision = QSpinBox()
        self.mass_precision.setRange(0, 3)
        self.mass_precision.setValue(2)
        precision_layout.addWidget(self.mass_precision, 1, 1)

        general_layout.addWidget(precision_group)
        general_layout.addStretch()

        tabs.addTab(general_tab, "General")

        # Defaults tab
        defaults_tab = QWidget()
        defaults_layout = QVBoxLayout(defaults_tab)
        defaults_layout.setSpacing(15)

        defaults_group = QGroupBox(tr('settings.default_values'))
        defaults_grid = QGridLayout(defaults_group)
        defaults_grid.setSpacing(10)

        defaults_grid.addWidget(QLabel("SF par defaut:"), 0, 0)
        self.default_sf = QComboBox()
        self.default_sf.addItems(["1.1", "1.15", "1.2", "1.25"])
        defaults_grid.addWidget(self.default_sf, 0, 1)

        defaults_grid.addWidget(QLabel("Ss par defaut:"), 1, 0)
        self.default_ss = QComboBox()
        self.default_ss.addItems(["2.5", "2.65", "2.7", "2.8"])
        self.default_ss.setCurrentIndex(1)
        defaults_grid.addWidget(self.default_ss, 1, 1)

        defaults_grid.addWidget(QLabel("Type de roche:"), 2, 0)
        self.default_rock = QComboBox()
        self.default_rock.addItem("Angulaire (0.375)")
        self.default_rock.addItem("Arrondi (0.30)")
        defaults_grid.addWidget(self.default_rock, 2, 1)

        defaults_layout.addWidget(defaults_group)
        defaults_layout.addStretch()

        tabs.addTab(defaults_tab, "Valeurs par defaut")

        # About tab
        about_tab = QWidget()
        about_layout = QVBoxLayout(about_tab)
        about_layout.setSpacing(15)

        # App info
        app_info = QLabel(f"""
        <h2>Maynord Calculator</h2>
        <p><b>Version:</b> 1.0.0</p>
        <p>Application de dimensionnement d'enrochements selon la methode USACE/Maynord
        pour les projets de renaturation de cours d'eau et d'ingenierie hydraulique.</p>
        """)
        app_info.setWordWrap(True)
        about_layout.addWidget(app_info)

        # References
        refs_frame = QFrame()
        refs_frame.setObjectName("refsFrame")
        refs_layout = QVBoxLayout(refs_frame)

        refs_title = QLabel("<b>References:</b>")
        refs_layout.addWidget(refs_title)

        refs_text = QLabel("""
        <ul style="margin-left: -20px;">
            <li>Maynord, S.T. (1988) - Technical Report HL-88-4</li>
            <li>USACE EM 1110-2-1601</li>
            <li>HEC-RAS Hydraulic Reference Manual</li>
        </ul>
        """)
        refs_text.setWordWrap(True)
        refs_layout.addWidget(refs_text)

        about_layout.addWidget(refs_frame)

        # Credits section with Easter egg
        credits_frame = QFrame()
        credits_frame.setObjectName("creditsFrame")
        credits_layout = QVBoxLayout(credits_frame)
        credits_layout.setAlignment(Qt.AlignCenter)

        # Easter egg image (hidden by default)
        self.easter_egg_image = QLabel()
        self.easter_egg_image.setAlignment(Qt.AlignCenter)
        self.easter_egg_image.setMinimumSize(200, 200)
        self.easter_egg_image.setScaledContents(False)
        self.easter_egg_image.hide()
        credits_layout.addWidget(self.easter_egg_image)

        # Easter egg title (hidden by default)
        self.easter_egg_title = QLabel("<h1 style='color: #f59e0b;'>LORD Z</h1>")
        self.easter_egg_title.setAlignment(Qt.AlignCenter)
        self.easter_egg_title.hide()
        credits_layout.addWidget(self.easter_egg_title)

        # Developer credit (clickable)
        self.credit_label = ClickableLabel()
        self.credit_label.setText("<p style='font-size: 14px;'>Developpe par <b>Marc Zermatten</b></p>")
        self.credit_label.setAlignment(Qt.AlignCenter)
        self.credit_label.on_easter_egg = self.show_easter_egg
        credits_layout.addWidget(self.credit_label)

        # Year
        self.year_label = QLabel("<p style='color: #64748b;'>2025 GeoMind</p>")
        self.year_label.setAlignment(Qt.AlignCenter)
        credits_layout.addWidget(self.year_label)

        about_layout.addWidget(credits_frame)
        about_layout.addStretch()

        tabs.addTab(about_tab, "A propos")

        layout.addWidget(tabs)

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def show_easter_egg(self):
        """Show the Lord Z Easter egg"""
        if self.easter_egg_active:
            return

        self.easter_egg_active = True

        # Hide normal credit
        self.credit_label.hide()

        # Load and show image
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                 "resources", "icons", "lord_z.png")

        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)

            # If dark mode, invert the black lines to white
            if self.current_theme == "dark":
                image = pixmap.toImage()
                # Invert colors for visibility in dark mode
                image.invertPixels()
                pixmap = QPixmap.fromImage(image)

            # Scale to reasonable size while keeping aspect ratio
            # Use a larger size to avoid cropping
            scaled = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.easter_egg_image.setPixmap(scaled)
            self.easter_egg_image.setFixedSize(scaled.size())
            self.easter_egg_image.show()

        # Show Lord Z title
        self.easter_egg_title.show()

        # Update year label
        self.year_label.setText("<p style='color: #f59e0b;'>The Legend Lives On</p>")

    def apply_theme(self):
        """Apply theme styling"""
        if self.current_theme == "dark":
            self.setStyleSheet("""
                QDialog {
                    background-color: #1e293b;
                    color: #e2e8f0;
                }
                QTabWidget::pane {
                    border: 1px solid #334155;
                    background-color: #1e293b;
                }
                QTabBar::tab {
                    background-color: #334155;
                    color: #e2e8f0;
                    padding: 8px 16px;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                }
                QTabBar::tab:selected {
                    background-color: #2563eb;
                    color: white;
                }
                QGroupBox {
                    font-weight: bold;
                    border: 1px solid #334155;
                    border-radius: 6px;
                    margin-top: 10px;
                    padding-top: 10px;
                    background-color: #0f172a;
                    color: #e2e8f0;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                    color: #60a5fa;
                }
                QLabel {
                    color: #e2e8f0;
                }
                QComboBox, QSpinBox {
                    background-color: #334155;
                    color: #e2e8f0;
                    border: 1px solid #475569;
                    border-radius: 4px;
                    padding: 5px;
                    min-width: 100px;
                }
                QComboBox:hover, QSpinBox:hover {
                    border-color: #60a5fa;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox QAbstractItemView {
                    background-color: #334155;
                    color: #e2e8f0;
                    selection-background-color: #2563eb;
                }
                QPushButton {
                    background-color: #334155;
                    color: #e2e8f0;
                    border: 1px solid #475569;
                    border-radius: 4px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #475569;
                    border-color: #60a5fa;
                }
                QPushButton:pressed {
                    background-color: #2563eb;
                }
                QFrame#creditsFrame, QFrame#refsFrame {
                    background-color: #0f172a;
                    border: 1px solid #334155;
                    border-radius: 8px;
                    padding: 15px;
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    background-color: #f8fafc;
                    color: #1e293b;
                }
                QTabWidget::pane {
                    border: 1px solid #e2e8f0;
                    background-color: #ffffff;
                }
                QTabBar::tab {
                    background-color: #e2e8f0;
                    color: #334155;
                    padding: 8px 16px;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                }
                QTabBar::tab:selected {
                    background-color: #2563eb;
                    color: white;
                }
                QGroupBox {
                    font-weight: bold;
                    border: 1px solid #e2e8f0;
                    border-radius: 6px;
                    margin-top: 10px;
                    padding-top: 10px;
                    background-color: #ffffff;
                    color: #1e293b;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                    color: #2563eb;
                }
                QLabel {
                    color: #334155;
                }
                QComboBox, QSpinBox {
                    background-color: #ffffff;
                    color: #1e293b;
                    border: 1px solid #cbd5e1;
                    border-radius: 4px;
                    padding: 5px;
                    min-width: 100px;
                }
                QComboBox:hover, QSpinBox:hover {
                    border-color: #2563eb;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox QAbstractItemView {
                    background-color: #ffffff;
                    color: #1e293b;
                    selection-background-color: #2563eb;
                    selection-color: white;
                }
                QPushButton {
                    background-color: #e2e8f0;
                    color: #334155;
                    border: 1px solid #cbd5e1;
                    border-radius: 4px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #cbd5e1;
                    border-color: #2563eb;
                }
                QPushButton:pressed {
                    background-color: #2563eb;
                    color: white;
                }
                QFrame#creditsFrame, QFrame#refsFrame {
                    background-color: #ffffff;
                    border: 1px solid #e2e8f0;
                    border-radius: 8px;
                    padding: 15px;
                }
            """)

    def accept(self):
        """Save settings and close"""
        # Apply language
        lang = self.lang_combo.currentData()
        set_language(lang)

        super().accept()
