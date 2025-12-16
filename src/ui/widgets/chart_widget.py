"""
Chart Widget - Gradation curve visualization (Enhanced)
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from core.maynord import MaynordResult


class GradationChart(QWidget):
    """Widget displaying gradation curve"""

    def __init__(self):
        super().__init__()
        self.current_theme = "light"
        self.last_result = None  # Store last result for theme changes
        self.last_results = []   # Store comparison results
        self.setup_ui()

    def setup_ui(self):
        """Setup the chart widget"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create matplotlib figure with constrained layout
        self.figure = Figure(figsize=(6, 4), dpi=100, constrained_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.canvas)
        self.init_chart()

    def set_theme(self, theme: str):
        """Set the chart theme and redraw with existing data"""
        self.current_theme = theme
        # Redraw with existing data
        if self.last_results:
            self.update_comparison(self.last_results)
        elif self.last_result:
            self.update_chart(self.last_result)
        else:
            self.init_chart()

    def _get_theme_colors(self):
        """Get colors based on current theme"""
        if self.current_theme == "dark":
            return {
                'bg': '#1e293b',
                'plot_bg': '#0f172a',
                'text': '#cbd5e1',
                'grid': '#334155',
                'line': '#0ea5e9',
                'd30': '#22c55e',
                'd50': '#f59e0b',
                'd100': '#ef4444',
            }
        else:
            return {
                'bg': '#ffffff',
                'plot_bg': '#f8fafc',
                'text': '#334155',
                'grid': '#e2e8f0',
                'line': '#2563eb',
                'd30': '#16a34a',
                'd50': '#d97706',
                'd100': '#dc2626',
            }

    def init_chart(self):
        """Initialize empty chart"""
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        colors = self._get_theme_colors()

        self.figure.patch.set_facecolor(colors['bg'])
        self.ax.set_facecolor(colors['plot_bg'])

        self.ax.set_xlabel('Diametre (mm)', fontsize=10, color=colors['text'], fontweight='bold')
        self.ax.set_ylabel('Passant cumule (%)', fontsize=10, color=colors['text'], fontweight='bold')
        self.ax.set_title('Courbe granulometrique', fontsize=11, fontweight='bold',
                         color=colors['text'], pad=10)

        self.ax.set_xscale('log')
        self.ax.set_xlim(10, 2000)
        self.ax.set_ylim(0, 100)

        # Grid
        self.ax.grid(True, which='major', linestyle='-', alpha=0.3, color=colors['grid'])
        self.ax.grid(True, which='minor', linestyle=':', alpha=0.2, color=colors['grid'])

        # Tick colors
        self.ax.tick_params(colors=colors['text'], which='both', labelsize=9)
        for spine in self.ax.spines.values():
            spine.set_color(colors['grid'])

        self.canvas.draw()

    def update_chart(self, result: MaynordResult):
        """Update chart with calculation results"""
        self.last_result = result
        self.last_results = []  # Clear comparison data

        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        colors = self._get_theme_colors()

        self.figure.patch.set_facecolor(colors['bg'])
        self.ax.set_facecolor(colors['plot_bg'])

        # Setup axes with responsive font sizes
        self.ax.set_xlabel('Diametre (mm)', fontsize=10, color=colors['text'], fontweight='bold')
        self.ax.set_ylabel('Passant cumule (%)', fontsize=10, color=colors['text'], fontweight='bold')
        self.ax.set_title('Courbe granulometrique', fontsize=11, fontweight='bold',
                         color=colors['text'], pad=8)

        self.ax.set_xscale('log')

        # Calculate gradation points
        d15 = result.d30 * 0.70
        d30 = result.d30
        d50 = result.d50
        d85 = result.d30 * 1.70
        d100 = result.d100

        # Adjust X limits to show full curve with margin
        x_min = max(5, d15 * 0.5)
        x_max = d100 * 1.3
        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(0, 105)

        # Grid
        self.ax.grid(True, which='major', linestyle='-', alpha=0.3, color=colors['grid'])
        self.ax.grid(True, which='minor', linestyle=':', alpha=0.2, color=colors['grid'])

        # Tick colors
        self.ax.tick_params(colors=colors['text'], which='both', labelsize=9)
        for spine in self.ax.spines.values():
            spine.set_color(colors['grid'])

        # Data points
        diameters = [d15, d30, d50, d85, d100]
        percentages = [15, 30, 50, 85, 100]

        # Plot gradation curve with markers
        self.ax.plot(diameters, percentages, 'o-', color=colors['line'],
                     linewidth=2.5, markersize=8, markerfacecolor='white',
                     markeredgewidth=2, label='Gradation', zorder=5)

        # Fill area under curve
        self.ax.fill_between(diameters, [0]*5, percentages, alpha=0.15, color=colors['line'])

        # Vertical lines for key diameters
        self.ax.axvline(x=d30, color=colors['d30'], linestyle='--', alpha=0.8, linewidth=1.5)
        self.ax.axvline(x=d50, color=colors['d50'], linestyle='--', alpha=0.8, linewidth=1.5)
        self.ax.axvline(x=d100, color=colors['d100'], linestyle='--', alpha=0.8, linewidth=1.5)

        # Annotations with boxes - positioned to avoid overlaps
        bbox_bg = colors['bg']
        bbox_props = dict(boxstyle="round,pad=0.2", facecolor=bbox_bg, edgecolor=colors['d30'], alpha=0.95)

        self.ax.annotate(f'D30={d30:.0f}', xy=(d30, 30), xytext=(d30*0.5, 20),
                        fontsize=9, color=colors['d30'], fontweight='bold',
                        bbox=bbox_props,
                        arrowprops=dict(arrowstyle='->', color=colors['d30'], alpha=0.7))

        bbox_props['edgecolor'] = colors['d50']
        self.ax.annotate(f'D50={d50:.0f}', xy=(d50, 50), xytext=(d50*1.5, 60),
                        fontsize=9, color=colors['d50'], fontweight='bold',
                        bbox=bbox_props,
                        arrowprops=dict(arrowstyle='->', color=colors['d50'], alpha=0.7))

        bbox_props['edgecolor'] = colors['d100']
        self.ax.annotate(f'D100={d100:.0f}', xy=(d100, 100), xytext=(d100*0.5, 90),
                        fontsize=9, color=colors['d100'], fontweight='bold',
                        bbox=bbox_props,
                        arrowprops=dict(arrowstyle='->', color=colors['d100'], alpha=0.7))

        # Legend
        self.ax.legend(loc='lower right', fontsize=9, framealpha=0.9,
                      facecolor=bbox_bg, edgecolor=colors['grid'], labelcolor=colors['text'])

        self.canvas.draw()

    def update_comparison(self, results: list):
        """Update chart with multiple results for comparison"""
        self.last_results = results
        self.last_result = None  # Clear single result

        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        colors = self._get_theme_colors()

        self.figure.patch.set_facecolor(colors['bg'])
        self.ax.set_facecolor(colors['plot_bg'])

        self.ax.set_xlabel('Diametre (mm)', fontsize=10, color=colors['text'], fontweight='bold')
        self.ax.set_ylabel('Passant cumule (%)', fontsize=10, color=colors['text'], fontweight='bold')
        self.ax.set_title(f'Comparaison ({len(results)} scenarios)', fontsize=11, fontweight='bold',
                         color=colors['text'], pad=8)

        self.ax.set_xscale('log')

        # Calculate x limits from all results
        all_d100 = [r.d100 for r in results]
        all_d15 = [r.d30 * 0.70 for r in results]
        x_min = max(5, min(all_d15) * 0.5)
        x_max = max(all_d100) * 1.3
        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(0, 105)

        self.ax.grid(True, which='both', linestyle='--', alpha=0.3, color=colors['grid'])
        self.ax.tick_params(colors=colors['text'], labelsize=9)
        for spine in self.ax.spines.values():
            spine.set_color(colors['grid'])

        # Color palette for scenarios
        palette = ['#2563eb', '#16a34a', '#f59e0b', '#dc2626', '#8b5cf6',
                   '#ec4899', '#06b6d4', '#84cc16', '#f97316', '#6366f1']

        for i, result in enumerate(results[:10]):
            d15 = result.d30 * 0.70
            d30 = result.d30
            d50 = result.d50
            d85 = result.d30 * 1.70
            d100 = result.d100

            diameters = [d15, d30, d50, d85, d100]
            percentages = [15, 30, 50, 85, 100]

            color = palette[i % len(palette)]
            self.ax.plot(diameters, percentages, 'o-', color=color,
                        linewidth=2, markersize=5,
                        label=f'S{i+1}: D30={d30:.0f} D50={d50:.0f}')

            # Add D50 marker annotation
            self.ax.plot(d50, 50, 's', color=color, markersize=8,
                        markerfacecolor='white', markeredgewidth=2)

        # Legend with scenario info
        self.ax.legend(loc='lower right', fontsize=8, framealpha=0.95,
                      facecolor=colors['bg'], edgecolor=colors['grid'],
                      labelcolor=colors['text'], ncol=1)

        # Add reference lines for percentiles
        for pct in [30, 50]:
            self.ax.axhline(y=pct, color=colors['grid'], linestyle='-', alpha=0.5, linewidth=0.5)

        self.canvas.draw()

    def clear(self):
        """Clear the chart and stored data"""
        self.last_result = None
        self.last_results = []
        self.init_chart()

    def save_image(self, filepath: str):
        """Save chart as image file"""
        self.figure.savefig(filepath, dpi=150, bbox_inches='tight',
                           facecolor=self.figure.get_facecolor())
