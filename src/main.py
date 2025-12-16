#!/usr/bin/env python3
"""
Maynord Calculator - Main Entry Point

Riprap sizing application based on USACE/Maynord methodology
for river restoration and hydraulic engineering.

Author: GeoMind
License: MIT
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from app import MaynordApp


def main():
    """Application entry point"""
    # High DPI support
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)

    # Application metadata
    app.setApplicationName("Maynord Calculator")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("GeoMind")

    # Default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Create and show main window
    window = MaynordApp()
    window.show()

    # Run event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
