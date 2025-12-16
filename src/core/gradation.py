"""
Gradation and Mass Calculations for Riprap

Handles:
- D30 → D50 → D100 conversions
- Mass calculations from diameter
- Standard gradation classes (USACE)
- Thickness calculations
"""

import math
from dataclasses import dataclass
from typing import Optional, List, Dict
from enum import Enum

# Physical constants
WATER_DENSITY = 1000  # kg/m³


class GradationClass(Enum):
    """Classes de gradation standard USACE"""
    CLASS_I = "I"       # D50 ~ 125mm
    CLASS_II = "II"     # D50 ~ 175mm
    CLASS_III = "III"   # D50 ~ 250mm
    CLASS_IV = "IV"     # D50 ~ 350mm
    CLASS_V = "V"       # D50 ~ 500mm
    CLASS_VI = "VI"     # D50 ~ 650mm
    CUSTOM = "custom"   # Personnalisé


@dataclass
class Gradation:
    """
    Représente une gradation d'enrochement

    Attributes:
        d30: 30ème percentile (mm)
        d50: 50ème percentile - médian (mm)
        d85: 85ème percentile (mm)
        d100: 100ème percentile - max (mm)
        d15: 15ème percentile (mm) - optionnel
    """
    d30: float
    d50: float
    d85: Optional[float] = None
    d100: Optional[float] = None
    d15: Optional[float] = None
    gradation_class: GradationClass = GradationClass.CUSTOM

    def __post_init__(self):
        # Calculs automatiques si non fournis
        if self.d100 is None:
            self.d100 = self.d30 * 2.1  # Ratio standard

        if self.d85 is None:
            self.d85 = self.d30 * 1.7  # Approximation

        if self.d15 is None:
            self.d15 = self.d30 * 0.7  # Approximation

    def get_uniformity_coefficient(self) -> float:
        """
        Calcule le coefficient d'uniformité Cu = D60/D10

        Plus Cu est grand, plus la gradation est étalée
        Cu > 4 = bien gradué, Cu < 4 = uniforme
        """
        d60 = self.d30 * 1.15  # Approximation
        d10 = self.d15 * 0.9   # Approximation
        return round(d60 / d10, 2) if d10 > 0 else 0

    def to_dict(self) -> Dict:
        """Convertit en dictionnaire"""
        return {
            'd15': round(self.d15, 1) if self.d15 else None,
            'd30': round(self.d30, 1),
            'd50': round(self.d50, 1),
            'd85': round(self.d85, 1) if self.d85 else None,
            'd100': round(self.d100, 1) if self.d100 else None,
            'class': self.gradation_class.value,
        }


# Gradations standard USACE (valeurs en mm)
USACE_GRADATIONS = {
    GradationClass.CLASS_I: {
        'd15': 70, 'd30': 95, 'd50': 125, 'd85': 180, 'd100': 200,
        'weight_range_kg': (1, 15),
    },
    GradationClass.CLASS_II: {
        'd15': 100, 'd30': 135, 'd50': 175, 'd85': 250, 'd100': 300,
        'weight_range_kg': (5, 45),
    },
    GradationClass.CLASS_III: {
        'd15': 140, 'd30': 190, 'd50': 250, 'd85': 350, 'd100': 425,
        'weight_range_kg': (15, 125),
    },
    GradationClass.CLASS_IV: {
        'd15': 200, 'd30': 270, 'd50': 350, 'd85': 500, 'd100': 600,
        'weight_range_kg': (45, 350),
    },
    GradationClass.CLASS_V: {
        'd15': 280, 'd30': 385, 'd50': 500, 'd85': 700, 'd100': 850,
        'weight_range_kg': (125, 1000),
    },
    GradationClass.CLASS_VI: {
        'd15': 360, 'd30': 500, 'd50': 650, 'd85': 900, 'd100': 1100,
        'weight_range_kg': (350, 2000),
    },
}


def convert_d30_to_gradation(d30_mm: float,
                             d50_ratio: float = 1.30,
                             d100_ratio: float = 2.10) -> Gradation:
    """
    Convertit un D30 en gradation complète

    Args:
        d30_mm: D30 calculé (mm)
        d50_ratio: Ratio D50/D30 (défaut 1.30)
        d100_ratio: Ratio D100/D30 (défaut 2.10)

    Returns:
        Gradation complète
    """
    d50 = d30_mm * d50_ratio
    d100 = d30_mm * d100_ratio
    d85 = d30_mm * 1.70  # Approximation
    d15 = d30_mm * 0.70  # Approximation

    # Trouver la classe la plus proche
    grad_class = find_closest_gradation_class(d50)

    return Gradation(
        d30=d30_mm,
        d50=d50,
        d85=d85,
        d100=d100,
        d15=d15,
        gradation_class=grad_class,
    )


def find_closest_gradation_class(d50_mm: float) -> GradationClass:
    """
    Trouve la classe de gradation USACE la plus proche d'un D50 donné

    Args:
        d50_mm: D50 en mm

    Returns:
        GradationClass
    """
    min_diff = float('inf')
    closest = GradationClass.CUSTOM

    for grad_class, values in USACE_GRADATIONS.items():
        diff = abs(values['d50'] - d50_mm)
        if diff < min_diff:
            min_diff = diff
            closest = grad_class

    # Si trop loin de toute classe standard (>30% d'écart)
    if closest != GradationClass.CUSTOM:
        ref_d50 = USACE_GRADATIONS[closest]['d50']
        if abs(d50_mm - ref_d50) / ref_d50 > 0.30:
            return GradationClass.CUSTOM

    return closest


def get_usace_gradation(grad_class: GradationClass) -> Gradation:
    """
    Retourne une gradation standard USACE

    Args:
        grad_class: Classe de gradation

    Returns:
        Gradation
    """
    if grad_class == GradationClass.CUSTOM:
        raise ValueError("Pas de gradation standard pour CUSTOM")

    vals = USACE_GRADATIONS[grad_class]
    return Gradation(
        d15=vals['d15'],
        d30=vals['d30'],
        d50=vals['d50'],
        d85=vals['d85'],
        d100=vals['d100'],
        gradation_class=grad_class,
    )


def calculate_mass(diameter_mm: float,
                   specific_gravity: float = 2.65,
                   shape_factor: float = 0.523) -> float:
    """
    Calcule la masse d'une pierre à partir de son diamètre

    Args:
        diameter_mm: Diamètre équivalent (mm)
        specific_gravity: Densité relative (2.5-3.0)
        shape_factor: Facteur de forme (0.523 pour sphère parfaite)

    Returns:
        Masse en kg

    Formule (sphère équivalente):
        M = (π/6) × ρs × D³ = shape_factor × ρs × D³

    Note:
        shape_factor = π/6 ≈ 0.523 pour une sphère
        En pratique, utiliser 0.5-0.55 pour des pierres réelles
    """
    diameter_m = diameter_mm / 1000
    density = specific_gravity * WATER_DENSITY  # kg/m³

    mass = shape_factor * density * (diameter_m ** 3)
    return round(mass, 3)


def calculate_diameter_from_mass(mass_kg: float,
                                  specific_gravity: float = 2.65,
                                  shape_factor: float = 0.523) -> float:
    """
    Calcule le diamètre équivalent à partir de la masse

    Args:
        mass_kg: Masse de la pierre (kg)
        specific_gravity: Densité relative
        shape_factor: Facteur de forme

    Returns:
        Diamètre en mm
    """
    density = specific_gravity * WATER_DENSITY
    diameter_m = (mass_kg / (shape_factor * density)) ** (1/3)
    return round(diameter_m * 1000, 1)


def calculate_layer_thickness(d50_mm: float, d100_mm: float) -> float:
    """
    Calcule l'épaisseur de couche recommandée

    Règle USACE EM 1110-2-1601:
        Épaisseur = max(D100, 1.5 × D50)

    Args:
        d50_mm: D50 en mm
        d100_mm: D100 en mm

    Returns:
        Épaisseur recommandée en cm
    """
    thickness_mm = max(d100_mm, 1.5 * d50_mm)
    return round(thickness_mm / 10, 1)  # Conversion mm → cm


def calculate_volume_per_m2(thickness_cm: float, porosity: float = 0.35) -> float:
    """
    Calcule le volume de roche par m² de surface

    Args:
        thickness_cm: Épaisseur de couche (cm)
        porosity: Porosité (0.30-0.40 typique)

    Returns:
        Volume solide de roche (m³/m²)
    """
    thickness_m = thickness_cm / 100
    solid_volume = thickness_m * (1 - porosity)
    return round(solid_volume, 4)


def calculate_mass_per_m2(thickness_cm: float,
                          specific_gravity: float = 2.65,
                          porosity: float = 0.35) -> float:
    """
    Calcule la masse d'enrochement par m² de surface

    Args:
        thickness_cm: Épaisseur de couche (cm)
        specific_gravity: Densité relative de la roche
        porosity: Porosité

    Returns:
        Masse en kg/m²
    """
    volume = calculate_volume_per_m2(thickness_cm, porosity)
    density = specific_gravity * WATER_DENSITY
    mass = volume * density
    return round(mass, 1)


def calculate_tonnes_per_m(length_m: float,
                           width_m: float,
                           thickness_cm: float,
                           specific_gravity: float = 2.65,
                           porosity: float = 0.35) -> float:
    """
    Calcule le tonnage total pour une section

    Args:
        length_m: Longueur du tronçon (m)
        width_m: Largeur de la protection (m)
        thickness_cm: Épaisseur (cm)
        specific_gravity: Densité relative
        porosity: Porosité

    Returns:
        Masse totale en tonnes
    """
    surface = length_m * width_m
    mass_per_m2 = calculate_mass_per_m2(thickness_cm, specific_gravity, porosity)
    total_kg = surface * mass_per_m2
    return round(total_kg / 1000, 2)


@dataclass
class GradationSummary:
    """Résumé complet d'une gradation avec masses et épaisseur"""
    gradation: Gradation
    mass_d30: float  # kg
    mass_d50: float  # kg
    mass_d100: float  # kg
    thickness: float  # cm
    mass_per_m2: float  # kg/m²
    usace_class: str


def get_complete_gradation_summary(d30_mm: float,
                                    specific_gravity: float = 2.65) -> GradationSummary:
    """
    Génère un résumé complet à partir du D30 calculé

    Args:
        d30_mm: D30 en mm
        specific_gravity: Densité relative

    Returns:
        GradationSummary avec toutes les informations
    """
    grad = convert_d30_to_gradation(d30_mm)

    mass_d30 = calculate_mass(grad.d30, specific_gravity)
    mass_d50 = calculate_mass(grad.d50, specific_gravity)
    mass_d100 = calculate_mass(grad.d100, specific_gravity)

    thickness = calculate_layer_thickness(grad.d50, grad.d100)
    mass_m2 = calculate_mass_per_m2(thickness, specific_gravity)

    return GradationSummary(
        gradation=grad,
        mass_d30=mass_d30,
        mass_d50=mass_d50,
        mass_d100=mass_d100,
        thickness=thickness,
        mass_per_m2=mass_m2,
        usace_class=grad.gradation_class.value,
    )
