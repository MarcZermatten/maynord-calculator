"""
Calculator Tab - Main calculation interface (Refactored)
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QDoubleSpinBox, QComboBox, QGroupBox,
    QPushButton, QFrame, QSlider, QRadioButton,
    QButtonGroup, QSplitter, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, Signal

from core.maynord import MaynordCalculator, MaynordResult
from core.coefficients import (
    calculate_cv, calculate_k1, COMMON_SLOPES
)
from core.gradation import get_complete_gradation_summary
from resources.translations import tr
from ui.widgets.results_panel import ResultsPanel
from ui.widgets.chart_widget import GradationChart


class CalculatorTab(QWidget):
    """Main calculator tab"""

    calculation_done = Signal(object)
    export_excel_requested = Signal(object, dict)  # result, input_params
    export_pdf_requested = Signal(object, dict, str)  # result, input_params, chart_path
    save_requested = Signal()
    add_to_comparison_requested = Signal(dict)  # calculation data for comparison

    def __init__(self, project_manager):
        super().__init__()
        self.project_manager = project_manager
        self.calculator = MaynordCalculator()
        self.last_result = None
        self.setup_ui()
        self.connect_signals()
        self.update_coefficients()

    def setup_ui(self):
        """Setup the calculator UI"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(0)

        # Use QSplitter for resizable panels
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(8)
        self.splitter.setChildrenCollapsible(False)

        # ===== LEFT PANEL - Inputs in ScrollArea =====
        # Create scroll area for sidebar
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        left_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        left_scroll.setMinimumWidth(360)
        left_scroll.setMaximumWidth(500)
        left_scroll.setFrameShape(QFrame.NoFrame)

        # Content widget inside scroll area
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(8)
        left_layout.setContentsMargins(8, 8, 8, 8)

        # Set minimum height for content to prevent shrinking
        left_widget.setMinimumHeight(620)

        # Hydraulic parameters
        self.hydraulic_group = self.create_hydraulic_group()
        left_layout.addWidget(self.hydraulic_group)

        # Configuration
        self.config_group = self.create_config_group()
        left_layout.addWidget(self.config_group)

        # Coefficients
        self.coeff_group = self.create_coefficients_group()
        left_layout.addWidget(self.coeff_group)

        # Buttons - Calculate/Reset
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.calc_btn = QPushButton("🔬 Calculer")
        self.calc_btn.setObjectName("primaryButton")
        self.calc_btn.setMinimumHeight(42)
        self.calc_btn.setToolTip("Lancer le calcul de dimensionnement (Ctrl+Enter)")
        self.calc_btn.clicked.connect(self.calculate)
        btn_layout.addWidget(self.calc_btn, 2)

        self.reset_btn = QPushButton("↺ Reset")
        self.reset_btn.setMinimumHeight(42)
        self.reset_btn.setToolTip("Remettre tous les parametres par defaut")
        self.reset_btn.clicked.connect(self.reset)
        btn_layout.addWidget(self.reset_btn, 1)

        left_layout.addLayout(btn_layout)

        # Export buttons
        export_layout = QHBoxLayout()
        export_layout.setSpacing(8)

        self.export_excel_btn = QPushButton("📊 Excel")
        self.export_excel_btn.setMinimumHeight(36)
        self.export_excel_btn.setToolTip("Exporter le rapport en Excel (.xlsx)")
        export_layout.addWidget(self.export_excel_btn)

        self.export_pdf_btn = QPushButton("📄 PDF")
        self.export_pdf_btn.setMinimumHeight(36)
        self.export_pdf_btn.setToolTip("Exporter le rapport en PDF")
        export_layout.addWidget(self.export_pdf_btn)

        left_layout.addLayout(export_layout)

        # Add to comparison button
        self.add_comparison_btn = QPushButton("➕ Ajouter a comparaison")
        self.add_comparison_btn.setMinimumHeight(36)
        self.add_comparison_btn.setToolTip("Stocker ce calcul dans l'onglet Comparaison")
        self.add_comparison_btn.setEnabled(False)
        left_layout.addWidget(self.add_comparison_btn)

        left_layout.addStretch()

        # Set content widget in scroll area
        left_scroll.setWidget(left_widget)

        # ===== RIGHT PANEL - Results with vertical splitter =====
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(0)
        right_layout.setContentsMargins(8, 8, 8, 8)

        # Vertical splitter for results and chart
        self.v_splitter = QSplitter(Qt.Vertical)
        self.v_splitter.setHandleWidth(8)
        self.v_splitter.setChildrenCollapsible(False)

        # Results panel (compact)
        self.results_panel = ResultsPanel()
        self.v_splitter.addWidget(self.results_panel)

        # Chart
        self.chart = GradationChart()
        self.chart.setMinimumHeight(200)
        self.chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.v_splitter.addWidget(self.chart)

        # Set initial vertical sizes
        self.v_splitter.setSizes([280, 400])

        right_layout.addWidget(self.v_splitter)

        # Add panels to horizontal splitter
        self.splitter.addWidget(left_scroll)
        self.splitter.addWidget(right_widget)

        # Set initial sizes (left: 380px, right: remaining)
        self.splitter.setSizes([380, 800])

        main_layout.addWidget(self.splitter)

    def create_hydraulic_group(self) -> QGroupBox:
        """Create hydraulic parameters group (compact)"""
        group = QGroupBox("📊 Parametres hydrauliques")
        layout = QGridLayout(group)
        layout.setSpacing(6)
        layout.setContentsMargins(8, 12, 8, 8)

        # Velocity
        v_label = QLabel("Vitesse V")
        v_label.setToolTip("Vitesse moyenne (0.5-6 m/s typique)")
        layout.addWidget(v_label, 0, 0)

        self.velocity_spin = QDoubleSpinBox()
        self.velocity_spin.setRange(0.1, 15.0)
        self.velocity_spin.setValue(2.0)
        self.velocity_spin.setSingleStep(0.1)
        self.velocity_spin.setDecimals(2)
        self.velocity_spin.setSuffix(" m/s")
        self.velocity_spin.setToolTip("Plage: 0.1 - 15.0 m/s")
        layout.addWidget(self.velocity_spin, 0, 1)

        self.velocity_slider = QSlider(Qt.Horizontal)
        self.velocity_slider.setRange(1, 150)
        self.velocity_slider.setValue(20)
        self.velocity_slider.setMaximumHeight(20)
        layout.addWidget(self.velocity_slider, 1, 0, 1, 2)

        # Depth
        d_label = QLabel("Profondeur D")
        d_label.setToolTip("Profondeur d'eau au-dessus de l'enrochement")
        layout.addWidget(d_label, 2, 0)

        self.depth_spin = QDoubleSpinBox()
        self.depth_spin.setRange(0.1, 30.0)
        self.depth_spin.setValue(1.5)
        self.depth_spin.setSingleStep(0.1)
        self.depth_spin.setDecimals(2)
        self.depth_spin.setSuffix(" m")
        self.depth_spin.setToolTip("Plage: 0.1 - 30.0 m")
        layout.addWidget(self.depth_spin, 2, 1)

        self.depth_slider = QSlider(Qt.Horizontal)
        self.depth_slider.setRange(1, 300)
        self.depth_slider.setValue(15)
        self.depth_slider.setMaximumHeight(20)
        layout.addWidget(self.depth_slider, 3, 0, 1, 2)

        return group

    def create_config_group(self) -> QGroupBox:
        """Create configuration group (responsive)"""
        group = QGroupBox("⚙️ Configuration")
        layout = QGridLayout(group)
        layout.setSpacing(6)
        layout.setContentsMargins(8, 12, 8, 8)

        # Row 0: Section type
        layout.addWidget(QLabel("Section"), 0, 0)

        self.section_group = QButtonGroup(self)
        self.bed_radio = QRadioButton("Lit")
        self.bed_radio.setChecked(True)
        self.bed_radio.setToolTip("Fond plat du cours d'eau (K1=1.0)")
        self.side_radio = QRadioButton("Talus")
        self.side_radio.setToolTip("Berges inclinees (K1 selon pente)")
        self.section_group.addButton(self.bed_radio, 0)
        self.section_group.addButton(self.side_radio, 1)
        layout.addWidget(self.bed_radio, 0, 1)
        layout.addWidget(self.side_radio, 0, 2)

        self.slope_combo = QComboBox()
        self.slope_combo.addItems(['3:1', '2.5:1', '2:1', '1.5:1'])
        self.slope_combo.setCurrentIndex(2)
        self.slope_combo.setEnabled(False)
        self.slope_combo.setToolTip("Pente du talus (H:V)")
        layout.addWidget(self.slope_combo, 0, 3)

        # Row 1: Channel config
        layout.addWidget(QLabel("Chenal"), 1, 0)

        self.channel_group = QButtonGroup(self)
        self.straight_radio = QRadioButton("Droit")
        self.straight_radio.setChecked(True)
        self.straight_radio.setToolTip("Chenal droit (Cv=1.0)")
        self.transition_radio = QRadioButton("Trans")
        self.transition_radio.setToolTip("Zone de transition (Cv=1.25)")
        self.bend_radio = QRadioButton("Courbe")
        self.bend_radio.setToolTip("Courbe (Cv selon R/W)")
        self.channel_group.addButton(self.straight_radio, 0)
        self.channel_group.addButton(self.transition_radio, 1)
        self.channel_group.addButton(self.bend_radio, 2)
        layout.addWidget(self.straight_radio, 1, 1)
        layout.addWidget(self.transition_radio, 1, 2)
        layout.addWidget(self.bend_radio, 1, 3)

        # Row 2: R/W ratio (only when bend selected)
        self.rw_label = QLabel("R/W")
        self.rw_label.setToolTip("Ratio rayon/largeur pour courbes")
        layout.addWidget(self.rw_label, 2, 0)
        self.rw_spin = QDoubleSpinBox()
        self.rw_spin.setRange(2.0, 50.0)
        self.rw_spin.setValue(10.0)
        self.rw_spin.setSingleStep(0.5)
        self.rw_spin.setEnabled(False)
        self.rw_spin.setToolTip("Plus petit = courbe serree")
        layout.addWidget(self.rw_spin, 2, 1, 1, 2)

        # Hidden label for compatibility
        self.slope_label = QLabel("")
        self.slope_label.hide()

        return group

    def create_coefficients_group(self) -> QGroupBox:
        """Create coefficients group (compact)"""
        group = QGroupBox("🔢 Coefficients")
        layout = QGridLayout(group)
        layout.setSpacing(4)
        layout.setContentsMargins(8, 12, 8, 8)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)

        # Row 0: SF and Rock type side by side
        sf_label = QLabel("SF")
        sf_label.setToolTip("Facteur de securite (1.1 standard)")
        layout.addWidget(sf_label, 0, 0)
        self.sf_spin = QDoubleSpinBox()
        self.sf_spin.setRange(1.0, 2.0)
        self.sf_spin.setValue(1.1)
        self.sf_spin.setSingleStep(0.05)
        self.sf_spin.setDecimals(2)
        self.sf_spin.setToolTip("1.1 = USACE standard")
        layout.addWidget(self.sf_spin, 0, 1)

        # Row 1: Rock type
        rock_label = QLabel("Type roche")
        rock_label.setToolTip("Affecte Cs")
        layout.addWidget(rock_label, 1, 0)
        self.rock_combo = QComboBox()
        self.rock_combo.addItem("🔷 Angulaire (concasse)", 0.375)
        self.rock_combo.addItem("⚪ Arrondi (galets)", 0.30)
        self.rock_combo.setToolTip("Angulaire: Cs=0.375, Arrondi: Cs=0.30")
        layout.addWidget(self.rock_combo, 1, 1)

        # Row 2: Coefficients display (compact inline)
        coef_frame = QFrame()
        coef_frame.setObjectName("coeffDisplay")
        coef_layout = QHBoxLayout(coef_frame)
        coef_layout.setContentsMargins(6, 4, 6, 4)
        coef_layout.setSpacing(12)

        self.cs_label = QLabel("Cs=0.375")
        self.cs_label.setToolTip("Coefficient de stabilite")
        coef_layout.addWidget(self.cs_label)

        self.cv_label = QLabel("Cv=1.000")
        self.cv_label.setToolTip("Coefficient de vitesse")
        self.cv_info = QLabel("")  # Hidden, for compatibility
        self.cv_info.hide()
        coef_layout.addWidget(self.cv_label)

        self.k1_label = QLabel("K1=1.000")
        self.k1_label.setToolTip("Facteur pente laterale")
        self.k1_info = QLabel("")  # Hidden, for compatibility
        self.k1_info.hide()
        coef_layout.addWidget(self.k1_label)

        coef_layout.addStretch()
        layout.addWidget(coef_frame, 2, 0, 1, 2)

        # Row 3: Ss and CT side by side
        ss_label = QLabel("Ss (densite)")
        ss_label.setToolTip("Densite relative roche (2.65 granite)")
        layout.addWidget(ss_label, 3, 0)
        self.ss_spin = QDoubleSpinBox()
        self.ss_spin.setRange(2.0, 3.5)
        self.ss_spin.setValue(2.65)
        self.ss_spin.setSingleStep(0.05)
        self.ss_spin.setDecimals(2)
        self.ss_spin.setToolTip("2.65 = granite standard")
        layout.addWidget(self.ss_spin, 3, 1)

        ct_label = QLabel("CT (epaisseur)")
        ct_label.setToolTip("Coef. epaisseur couche (1.0 standard)")
        layout.addWidget(ct_label, 4, 0)
        self.ct_spin = QDoubleSpinBox()
        self.ct_spin.setRange(0.5, 1.5)
        self.ct_spin.setValue(1.0)
        self.ct_spin.setSingleStep(0.05)
        self.ct_spin.setDecimals(2)
        self.ct_spin.setToolTip("1.0 = standard, <1.0 = couche epaisse")
        layout.addWidget(self.ct_spin, 4, 1)

        return group

    def connect_signals(self):
        """Connect UI signals"""
        # Sliders <-> spinboxes
        self.velocity_slider.valueChanged.connect(
            lambda v: self.velocity_spin.setValue(v / 10)
        )
        self.velocity_spin.valueChanged.connect(
            lambda v: self.velocity_slider.setValue(int(v * 10))
        )

        self.depth_slider.valueChanged.connect(
            lambda v: self.depth_spin.setValue(v / 10)
        )
        self.depth_spin.valueChanged.connect(
            lambda v: self.depth_slider.setValue(int(v * 10))
        )

        # Section type
        self.section_group.buttonClicked.connect(self.on_section_changed)

        # Channel config
        self.channel_group.buttonClicked.connect(self.on_channel_changed)

        # Rock type
        self.rock_combo.currentIndexChanged.connect(self.on_rock_changed)

        # Auto-update coefficients
        self.slope_combo.currentIndexChanged.connect(self.update_coefficients)
        self.rw_spin.valueChanged.connect(self.update_coefficients)

        # Export buttons
        self.export_excel_btn.clicked.connect(self._on_export_excel)
        self.export_pdf_btn.clicked.connect(self._on_export_pdf)

        # Add to comparison
        self.add_comparison_btn.clicked.connect(self._on_add_to_comparison)

    def on_section_changed(self):
        """Handle section type change"""
        is_side = self.side_radio.isChecked()
        self.slope_combo.setEnabled(is_side)
        self.slope_label.setEnabled(is_side)
        self.update_coefficients()

    def on_channel_changed(self):
        """Handle channel config change"""
        is_bend = self.bend_radio.isChecked()
        self.rw_spin.setEnabled(is_bend)
        self.rw_label.setEnabled(is_bend)
        self.update_coefficients()

    def on_rock_changed(self):
        """Handle rock type change"""
        cs = self.rock_combo.currentData()
        self.cs_label.setText(f"Cs={cs:.3f}")

    def update_coefficients(self):
        """Update coefficient displays"""
        # Cs
        cs = self.rock_combo.currentData()
        self.cs_label.setText(f"Cs={cs:.3f}")

        # Cv
        if self.straight_radio.isChecked():
            cv = 1.0
        elif self.transition_radio.isChecked():
            cv = 1.25
        else:  # bend
            cv = calculate_cv("bend", self.rw_spin.value(), 1.0)

        self.cv_label.setText(f"Cv={cv:.3f}")

        # K1
        if self.bed_radio.isChecked():
            k1 = 1.0
        else:
            slope_str = self.slope_combo.currentText()
            angle = COMMON_SLOPES.get(slope_str, {}).get('angle', 26.57)
            k1 = calculate_k1(angle)

        self.k1_label.setText(f"K1={k1:.3f}")

    def calculate(self):
        """Perform the Maynord calculation"""
        velocity = self.velocity_spin.value()
        depth = self.depth_spin.value()
        sf = self.sf_spin.value()
        cs = self.rock_combo.currentData()
        ss = self.ss_spin.value()
        ct = self.ct_spin.value()

        # Cv
        if self.straight_radio.isChecked():
            cv = 1.0
        elif self.transition_radio.isChecked():
            cv = 1.25
        else:
            cv = calculate_cv("bend", self.rw_spin.value(), 1.0)

        # K1
        if self.bed_radio.isChecked():
            k1 = 1.0
        else:
            slope_text = self.slope_combo.currentText()
            slope_str = slope_text.split(' ')[0]
            angle = COMMON_SLOPES.get(slope_str, {}).get('angle', 26.57)
            k1 = calculate_k1(angle)

        try:
            result = self.calculator.calculate(
                velocity=velocity,
                depth=depth,
                safety_factor=sf,
                stability_coef=cs,
                velocity_coef=cv,
                thickness_coef=ct,
                side_slope_factor=k1,
                specific_gravity=ss
            )

            self.last_result = result
            self.results_panel.update_results(result)
            self.chart.update_chart(result)
            self.calculation_done.emit(result)
            self._enable_export_buttons()

            # Add to project history
            self.project_manager.add_calculation({
                'velocity': velocity,
                'depth': depth,
                'result': result.get_summary_dict(),
                'coefficients': result.coefficients,
            })

        except Exception as e:
            self.results_panel.show_error(str(e))

    def reset(self):
        """Reset to default values"""
        self.velocity_spin.setValue(2.0)
        self.depth_spin.setValue(1.5)
        self.sf_spin.setValue(1.1)
        self.rock_combo.setCurrentIndex(0)
        self.ss_spin.setValue(2.65)
        self.ct_spin.setValue(1.0)
        self.bed_radio.setChecked(True)
        self.straight_radio.setChecked(True)
        self.slope_combo.setEnabled(False)
        self.rw_spin.setEnabled(False)
        self.rw_spin.setValue(10.0)
        self.slope_combo.setCurrentIndex(2)
        self.update_coefficients()
        self.results_panel.clear()
        self.chart.clear()

    def refresh_labels(self):
        """Refresh labels after language change"""
        self.hydraulic_group.setTitle("📊 " + tr('input.title'))
        self.calc_btn.setText("🔬  " + tr('buttons.calculate'))
        self.reset_btn.setText("↺  " + tr('buttons.reset'))

    def on_theme_changed(self, theme: str):
        """Handle theme change - update chart"""
        self.chart.set_theme(theme)

    def get_input_params(self) -> dict:
        """Get current input parameters as dict"""
        params = {
            'velocity': self.velocity_spin.value(),
            'depth': self.depth_spin.value(),
            'section_type': 'Talus' if self.side_radio.isChecked() else 'Lit',
            'channel_type': 'Courbe' if self.bend_radio.isChecked() else (
                'Transition' if self.transition_radio.isChecked() else 'Droit'
            ),
        }
        if self.side_radio.isChecked():
            params['slope'] = self.slope_combo.currentText()
        if self.bend_radio.isChecked():
            params['rw_ratio'] = self.rw_spin.value()
        return params

    def save_chart_image(self, filepath: str):
        """Save current chart as image"""
        self.chart.save_image(filepath)

    def _on_export_excel(self):
        """Handle Excel export request"""
        if self.last_result:
            self.export_excel_requested.emit(self.last_result, self.get_input_params())

    def _on_export_pdf(self):
        """Handle PDF export request"""
        if self.last_result:
            import tempfile
            import os
            # Save chart to temp file
            temp_chart = os.path.join(tempfile.gettempdir(), 'maynord_chart.png')
            self.save_chart_image(temp_chart)
            self.export_pdf_requested.emit(self.last_result, self.get_input_params(), temp_chart)

    def _on_add_to_comparison(self):
        """Add current calculation to comparison tab"""
        if self.last_result:
            calc_data = {
                'velocity': self.velocity_spin.value(),
                'depth': self.depth_spin.value(),
                'result': self.last_result,
                'input_params': self.get_input_params(),
            }
            self.add_to_comparison_requested.emit(calc_data)

    def _enable_export_buttons(self):
        """Enable export buttons after calculation"""
        self.add_comparison_btn.setEnabled(True)
