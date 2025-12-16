"""
Comparison Tab - Multi-scenario comparison with enhanced features
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView, QLabel,
    QFileDialog, QMessageBox, QSplitter, QFrame, QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from core.maynord import MaynordCalculator
from resources.translations import tr
from ui.widgets.chart_widget import GradationChart


class ComparisonTab(QWidget):
    """Tab for comparing multiple scenarios"""

    def __init__(self, project_manager):
        super().__init__()
        self.project_manager = project_manager
        self.calculator = MaynordCalculator()
        self.scenarios = []
        self.current_theme = "light"
        self.setup_ui()

    def set_theme(self, theme: str):
        """Set the current theme and refresh display"""
        self.current_theme = theme
        self.chart.set_theme(theme)
        self.update_title_style()
        self.update_table_colors()
        # Redraw chart with existing data
        self.update_chart()

    def update_title_style(self):
        """Update title style based on theme"""
        if self.current_theme == "dark":
            self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #0ea5e9;")
        else:
            self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e40af;")

    def update_table_colors(self):
        """Update table colors based on theme"""
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    if col >= 8:  # Results columns
                        if col == 11:  # Status column
                            status_text = item.text()
                            if "OK" in status_text:
                                if self.current_theme == "dark":
                                    item.setBackground(QColor("#14532d"))
                                    item.setForeground(QColor("#86efac"))
                                else:
                                    item.setBackground(QColor("#dcfce7"))
                                    item.setForeground(QColor("#166534"))
                            else:
                                if self.current_theme == "dark":
                                    item.setBackground(QColor("#422006"))
                                    item.setForeground(QColor("#fcd34d"))
                                else:
                                    item.setBackground(QColor("#fef3c7"))
                                    item.setForeground(QColor("#92400e"))
                        else:
                            if self.current_theme == "dark":
                                item.setBackground(QColor("#334155"))
                                item.setForeground(QColor("#e2e8f0"))
                            else:
                                item.setBackground(QColor("#f1f5f9"))
                                item.setForeground(QColor("#1e293b"))
                    else:
                        # Input columns
                        if self.current_theme == "dark":
                            item.setForeground(QColor("#e2e8f0"))
                        else:
                            item.setForeground(QColor("#1e293b"))

    def setup_ui(self):
        """Setup the comparison UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        # Header
        header = QHBoxLayout()
        self.title_label = QLabel(tr('comparison.title'))
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e40af;")
        header.addWidget(self.title_label)
        header.addStretch()

        self.add_btn = QPushButton("+ Scenario")
        self.add_btn.setToolTip("Ajouter un scenario vide")
        self.add_btn.clicked.connect(self.add_scenario)
        header.addWidget(self.add_btn)

        self.import_btn = QPushButton("Import Excel")
        self.import_btn.setToolTip("Importer des scenarios depuis Excel")
        self.import_btn.clicked.connect(self.import_from_excel)
        header.addWidget(self.import_btn)

        self.delete_btn = QPushButton("Supprimer")
        self.delete_btn.setToolTip("Supprimer le scenario selectionne")
        self.delete_btn.clicked.connect(self.delete_selected_scenario)
        header.addWidget(self.delete_btn)

        self.clear_btn = QPushButton("Tout effacer")
        self.clear_btn.setToolTip("Effacer tous les scenarios")
        self.clear_btn.clicked.connect(self.clear_scenarios)
        header.addWidget(self.clear_btn)

        layout.addLayout(header)

        # Splitter for table and chart
        splitter = QSplitter(Qt.Vertical)

        # Table container
        table_widget = QWidget()
        table_layout = QVBoxLayout(table_widget)
        table_layout.setContentsMargins(0, 0, 0, 0)

        # Table with 13 columns (added delete button column)
        self.table = QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels([
            '#', 'Description', 'V (m/s)', 'D (m)', 'SF', 'Cs', 'Cv', 'K1',
            'D30 (mm)', 'D50 (mm)', 'Masse (kg)', 'Status'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        table_layout.addWidget(self.table)

        splitter.addWidget(table_widget)

        # Chart with summary panel
        chart_container = QWidget()
        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(0, 0, 0, 0)
        chart_layout.setSpacing(8)

        # Summary frame for comparison stats
        self.summary_frame = QFrame()
        self.summary_frame.setObjectName("comparisonSummary")
        summary_layout = QGridLayout(self.summary_frame)
        summary_layout.setContentsMargins(10, 8, 10, 8)
        summary_layout.setSpacing(15)

        # Summary labels
        self.min_d30_label = QLabel("D30 min: --")
        self.max_d30_label = QLabel("D30 max: --")
        self.min_d50_label = QLabel("D50 min: --")
        self.max_d50_label = QLabel("D50 max: --")
        self.avg_mass_label = QLabel("Masse moy: --")
        self.scenario_count_label = QLabel("Scenarios: 0")

        summary_layout.addWidget(self.min_d30_label, 0, 0)
        summary_layout.addWidget(self.max_d30_label, 0, 1)
        summary_layout.addWidget(self.min_d50_label, 0, 2)
        summary_layout.addWidget(self.max_d50_label, 0, 3)
        summary_layout.addWidget(self.avg_mass_label, 0, 4)
        summary_layout.addWidget(self.scenario_count_label, 0, 5)

        chart_layout.addWidget(self.summary_frame)

        # Chart
        self.chart = GradationChart()
        chart_layout.addWidget(self.chart, 1)

        splitter.addWidget(chart_container)
        splitter.setSizes([250, 350])
        layout.addWidget(splitter)

    def add_calculation_from_calculator(self, calc_data):
        """Add a calculation from the calculator tab"""
        row = self.table.rowCount()
        self.table.insertRow(row)

        result = calc_data['result']
        params = calc_data['input_params']
        coeffs = result.coefficients

        # Build description from params
        desc = f"V={params['velocity']:.1f} D={params['depth']:.1f}"
        if params.get('slope'):
            desc += f" {params['slope']}"

        values = [
            str(row + 1),  # #
            desc,  # Description
            f"{params['velocity']:.2f}",  # V
            f"{params['depth']:.2f}",  # D
            f"{coeffs.get('SF', 1.1):.2f}",  # SF
            f"{coeffs.get('Cs', 0.375):.3f}",  # Cs
            f"{coeffs.get('Cv', 1.0):.3f}",  # Cv
            f"{coeffs.get('K1', 1.0):.3f}",  # K1
            f"{result.d30:.1f}",  # D30
            f"{result.d50:.1f}",  # D50
            f"{result.mass_d50:.1f}",  # Mass
            "OK" if result.froude_number <= 1.2 else "LIMITE",  # Status
        ]

        for col, value in enumerate(values):
            item = QTableWidgetItem(value)
            if col >= 8:  # Results columns (read-only)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, col, item)

        # Store result
        while len(self.scenarios) <= row:
            self.scenarios.append(None)
        self.scenarios[row] = result

        # Apply colors and update
        self.update_table_colors()
        self.update_chart()
        self.update_summary()

    def add_scenario(self):
        """Add a new scenario row"""
        # Disconnect to avoid multiple triggers
        try:
            self.table.cellChanged.disconnect(self.on_cell_changed)
        except:
            pass

        row = self.table.rowCount()
        self.table.insertRow(row)

        # Default values
        defaults = [
            str(row + 1),  # #
            f"Scenario {row + 1}",  # Description
            "2.0",  # V
            "1.5",  # D
            "1.1",  # SF
            "0.375",  # Cs
            "1.0",  # Cv
            "1.0",  # K1
            "--",  # D30
            "--",  # D50
            "--",  # Mass
            "--",  # Status
        ]

        for col, value in enumerate(defaults):
            item = QTableWidgetItem(value)
            if col >= 8:  # Results columns (read-only)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, col, item)

        # Reconnect and apply colors
        self.table.cellChanged.connect(self.on_cell_changed)
        self.update_table_colors()

    def delete_selected_scenario(self):
        """Delete the currently selected scenario"""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.information(self, "Suppression", "Selectionnez une ligne a supprimer")
            return

        row = selected_rows[0].row()

        # Remove from scenarios list
        if row < len(self.scenarios):
            self.scenarios.pop(row)

        # Remove row from table
        self.table.removeRow(row)

        # Renumber remaining rows
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)
            if item:
                item.setText(str(i + 1))

        self.update_chart()
        self.update_summary()

    def on_cell_changed(self, row, col):
        """Handle cell value changes"""
        if col in [2, 3, 4, 5, 6, 7]:  # Input columns
            self.calculate_row(row)
            self.update_chart()
            self.update_summary()

    def calculate_row(self, row):
        """Calculate results for a specific row"""
        try:
            v = float(self.table.item(row, 2).text())
            d = float(self.table.item(row, 3).text())
            sf = float(self.table.item(row, 4).text())
            cs = float(self.table.item(row, 5).text())
            cv = float(self.table.item(row, 6).text())
            k1 = float(self.table.item(row, 7).text())

            result = self.calculator.calculate(
                velocity=v, depth=d, safety_factor=sf,
                stability_coef=cs, velocity_coef=cv, side_slope_factor=k1
            )

            # Update results
            self.table.item(row, 8).setText(f"{result.d30:.1f}")
            self.table.item(row, 9).setText(f"{result.d50:.1f}")
            self.table.item(row, 10).setText(f"{result.mass_d50:.1f}")

            # Status
            status_item = self.table.item(row, 11)
            if result.froude_number > 1.2:
                status_item.setText("LIMITE")
            else:
                status_item.setText("OK")

            # Store result
            while len(self.scenarios) <= row:
                self.scenarios.append(None)
            self.scenarios[row] = result

            # Apply colors
            self.update_table_colors()

        except (ValueError, AttributeError):
            pass  # Invalid input, skip calculation

    def update_chart(self):
        """Update the comparison chart"""
        valid_results = [r for r in self.scenarios if r is not None]
        if valid_results:
            self.chart.update_comparison(valid_results)
        else:
            self.chart.clear()

    def update_summary(self):
        """Update the comparison summary statistics"""
        valid_results = [r for r in self.scenarios if r is not None]

        if not valid_results:
            self.min_d30_label.setText("D30 min: --")
            self.max_d30_label.setText("D30 max: --")
            self.min_d50_label.setText("D50 min: --")
            self.max_d50_label.setText("D50 max: --")
            self.avg_mass_label.setText("Masse moy: --")
            self.scenario_count_label.setText("Scenarios: 0")
            return

        d30_values = [r.d30 for r in valid_results]
        d50_values = [r.d50 for r in valid_results]
        mass_values = [r.mass_d50 for r in valid_results]

        self.min_d30_label.setText(f"D30 min: {min(d30_values):.0f} mm")
        self.max_d30_label.setText(f"D30 max: {max(d30_values):.0f} mm")
        self.min_d50_label.setText(f"D50 min: {min(d50_values):.0f} mm")
        self.max_d50_label.setText(f"D50 max: {max(d50_values):.0f} mm")

        avg_mass = sum(mass_values) / len(mass_values)
        if avg_mass >= 1000:
            self.avg_mass_label.setText(f"Masse moy: {avg_mass/1000:.2f} t")
        else:
            self.avg_mass_label.setText(f"Masse moy: {avg_mass:.0f} kg")

        self.scenario_count_label.setText(f"Scenarios: {len(valid_results)}")

    def import_from_excel(self):
        """Import scenarios from Excel file"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Importer depuis Excel",
            "", "Fichiers Excel (*.xlsx *.xls)"
        )
        if not filename:
            return

        try:
            import openpyxl
            wb = openpyxl.load_workbook(filename)
            ws = wb.active

            # Clear existing
            self.table.setRowCount(0)
            self.scenarios = []

            # Read rows (skip header)
            for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), 1):
                if not row[0]:  # Skip empty rows
                    continue

                self.add_scenario()
                table_row = self.table.rowCount() - 1

                # Map Excel columns to table columns
                # Expecting: Description, V, D, SF, Cs, Cv, K1
                if len(row) >= 7:
                    self.table.item(table_row, 1).setText(str(row[0] or f"Scenario {row_idx}"))
                    self.table.item(table_row, 2).setText(str(row[1] or "2.0"))
                    self.table.item(table_row, 3).setText(str(row[2] or "1.5"))
                    self.table.item(table_row, 4).setText(str(row[3] or "1.1"))
                    self.table.item(table_row, 5).setText(str(row[4] or "0.375"))
                    self.table.item(table_row, 6).setText(str(row[5] or "1.0"))
                    self.table.item(table_row, 7).setText(str(row[6] or "1.0"))

                self.calculate_row(table_row)

            self.update_chart()
            self.update_summary()
            QMessageBox.information(self, "Import", f"{self.table.rowCount()} scenarios importes")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur d'import: {e}")

    def clear_scenarios(self):
        """Clear all scenarios"""
        self.table.setRowCount(0)
        self.scenarios = []
        self.chart.clear()
        self.update_summary()

    def refresh_labels(self):
        """Refresh labels after language change"""
        self.add_btn.setText("+ Scenario")
        self.import_btn.setText("Import Excel")
