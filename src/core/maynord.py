"""
Maynord Equation Implementation
Based on USACE EM 1110-2-1601 and Maynord (1988) Technical Report HL-88-4

Equation:
    d30 = SF × Cs × Cv × CT × D × [V / √(g × D × (Ss - 1))]^2.5 / K1

References:
- Maynord, S.T. (1988). "Stable Riprap Size for Open Channel Flows"
- USACE Engineering Manual EM 1110-2-1601
- HEC-RAS Hydraulic Reference Manual
"""

import math
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

# Physical constants
GRAVITY = 9.81  # m/s²
WATER_DENSITY = 1000  # kg/m³


class RockShape(Enum):
    """Type de roche pour le coefficient de stabilité Cs"""
    ROUNDED = "rounded"      # Roche arrondie (galets)
    ANGULAR = "angular"      # Roche angulaire (concassée)
    CUSTOM = "custom"        # Valeur personnalisée


class ChannelConfig(Enum):
    """Configuration du chenal pour le coefficient Cv"""
    STRAIGHT = "straight"       # Chenal droit
    TRANSITION = "transition"   # Zone de transition
    BEND = "bend"              # Courbe


class SectionType(Enum):
    """Type de section pour le calcul"""
    BED = "bed"           # Lit de rivière
    SIDE_SLOPE = "side"   # Talus latéral


@dataclass
class MaynordInput:
    """Paramètres d'entrée pour le calcul Maynord"""
    # Paramètres hydrauliques
    velocity: float          # V - Vitesse d'écoulement (m/s)
    depth: float            # D - Profondeur d'eau (m)

    # Coefficients
    safety_factor: float = 1.1          # SF - Facteur de sécurité
    stability_coef: float = 0.375       # Cs - Coefficient de stabilité (angulaire par défaut)
    velocity_coef: float = 1.0          # Cv - Coefficient distribution vitesse
    thickness_coef: float = 1.0         # CT - Coefficient d'épaisseur
    side_slope_factor: float = 1.0      # K1 - Facteur correction pente
    specific_gravity: float = 2.65      # Ss - Densité relative de la roche

    # Métadonnées
    rock_shape: RockShape = RockShape.ANGULAR
    channel_config: ChannelConfig = ChannelConfig.STRAIGHT
    section_type: SectionType = SectionType.BED

    # Optionnel - pour calculs Cv/K1 automatiques
    bend_radius: Optional[float] = None     # R - Rayon de courbure (m)
    channel_width: Optional[float] = None   # W - Largeur du chenal (m)
    slope_angle: Optional[float] = None     # θ - Angle du talus (degrés)
    repose_angle: float = 40.0              # φ - Angle de repos (degrés)


@dataclass
class MaynordResult:
    """Résultats du calcul Maynord"""
    # Diamètres caractéristiques
    d30: float              # mm - 30ème percentile
    d50: float              # mm - 50ème percentile (médian)
    d100: float             # mm - 100ème percentile (max)

    # Masses correspondantes
    mass_d30: float         # kg - Masse pierre D30
    mass_d50: float         # kg - Masse pierre D50
    mass_d100: float        # kg - Masse pierre D100

    # Épaisseur de couche recommandée
    thickness: float        # cm

    # Paramètres intermédiaires
    froude_number: float    # Nombre de Froude
    dimensionless_param: float  # Paramètre sans dimension V/√(gD(Ss-1))

    # Coefficients utilisés
    coefficients: dict = field(default_factory=dict)

    # Status
    is_valid: bool = True
    warnings: list = field(default_factory=list)

    def get_summary_dict(self) -> dict:
        """Retourne un dictionnaire résumé pour export"""
        return {
            'd30_mm': round(self.d30, 1),
            'd50_mm': round(self.d50, 1),
            'd100_mm': round(self.d100, 1),
            'mass_d30_kg': round(self.mass_d30, 2),
            'mass_d50_kg': round(self.mass_d50, 2),
            'mass_d100_kg': round(self.mass_d100, 2),
            'thickness_cm': round(self.thickness, 1),
            'froude': round(self.froude_number, 3),
            'is_valid': self.is_valid,
        }


class MaynordCalculator:
    """
    Calculateur Maynord pour le dimensionnement d'enrochements

    Utilisation:
        calc = MaynordCalculator()
        result = calc.calculate(velocity=2.5, depth=1.5)
    """

    # Limites de validité de la méthode Maynord
    MAX_SLOPE = 0.02        # Pente max 2%
    MAX_FROUDE = 1.2        # Froude max

    # Ratios de conversion D30 → D50 → D100 (gradation standard)
    D50_RATIO = 1.30        # D50/D30
    D100_RATIO = 2.10       # D100/D30

    def __init__(self):
        pass

    def calculate(self,
                  velocity: float,
                  depth: float,
                  safety_factor: float = 1.1,
                  stability_coef: float = 0.375,
                  velocity_coef: float = 1.0,
                  thickness_coef: float = 1.0,
                  side_slope_factor: float = 1.0,
                  specific_gravity: float = 2.65) -> MaynordResult:
        """
        Calcule la taille d'enrochement stable selon la méthode Maynord

        Args:
            velocity: Vitesse d'écoulement (m/s)
            depth: Profondeur d'eau (m)
            safety_factor: SF - Facteur de sécurité (1.1-1.5)
            stability_coef: Cs - Coefficient de stabilité (0.30-0.375)
            velocity_coef: Cv - Coefficient distribution vitesse (≥1.0)
            thickness_coef: CT - Coefficient d'épaisseur (≤1.0)
            side_slope_factor: K1 - Facteur correction pente (≤1.0)
            specific_gravity: Ss - Densité relative roche (2.5-3.0)

        Returns:
            MaynordResult avec d30, d50, d100, masses et épaisseur
        """
        warnings = []

        # Validation des entrées
        if velocity <= 0:
            raise ValueError("La vitesse doit être positive")
        if depth <= 0:
            raise ValueError("La profondeur doit être positive")
        if specific_gravity <= 1.0:
            raise ValueError("La densité relative doit être > 1.0")

        # Calcul du nombre de Froude
        froude = velocity / math.sqrt(GRAVITY * depth)
        if froude > self.MAX_FROUDE:
            warnings.append(f"Froude ({froude:.2f}) > {self.MAX_FROUDE}: extrapolation hors domaine de validité")

        # Paramètre sans dimension
        dim_param = velocity / math.sqrt(GRAVITY * depth * (specific_gravity - 1))

        # Équation de Maynord: d30 = SF × Cs × Cv × CT × D × (V/√(gD(Ss-1)))^2.5 / K1
        d30_m = (safety_factor * stability_coef * velocity_coef * thickness_coef *
                 depth * (dim_param ** 2.5)) / side_slope_factor

        # Conversion en mm
        d30_mm = d30_m * 1000

        # Calcul des autres percentiles
        d50_mm = d30_mm * self.D50_RATIO
        d100_mm = d30_mm * self.D100_RATIO

        # Calcul des masses (sphère équivalente)
        rock_density = specific_gravity * WATER_DENSITY  # kg/m³
        mass_d30 = self._calculate_sphere_mass(d30_mm / 1000, rock_density)
        mass_d50 = self._calculate_sphere_mass(d50_mm / 1000, rock_density)
        mass_d100 = self._calculate_sphere_mass(d100_mm / 1000, rock_density)

        # Épaisseur de couche recommandée: max(D100, 1.5×D50)
        thickness_cm = max(d100_mm / 10, 1.5 * d50_mm / 10)

        # Vérifications supplémentaires
        if d30_mm < 50:
            warnings.append("D30 < 50mm: considérer un filtre géotextile")
        if d100_mm > 1500:
            warnings.append("D100 > 1.5m: blocs très lourds, vérifier les moyens de mise en place")

        return MaynordResult(
            d30=d30_mm,
            d50=d50_mm,
            d100=d100_mm,
            mass_d30=mass_d30,
            mass_d50=mass_d50,
            mass_d100=mass_d100,
            thickness=thickness_cm,
            froude_number=froude,
            dimensionless_param=dim_param,
            coefficients={
                'SF': safety_factor,
                'Cs': stability_coef,
                'Cv': velocity_coef,
                'CT': thickness_coef,
                'K1': side_slope_factor,
                'Ss': specific_gravity,
            },
            is_valid=True,
            warnings=warnings,
        )

    def calculate_from_input(self, inp: MaynordInput) -> MaynordResult:
        """Calcule à partir d'un objet MaynordInput"""
        return self.calculate(
            velocity=inp.velocity,
            depth=inp.depth,
            safety_factor=inp.safety_factor,
            stability_coef=inp.stability_coef,
            velocity_coef=inp.velocity_coef,
            thickness_coef=inp.thickness_coef,
            side_slope_factor=inp.side_slope_factor,
            specific_gravity=inp.specific_gravity,
        )

    def calculate_inverse(self,
                          d30_available: float,
                          depth: float,
                          specific_gravity: float = 2.65,
                          safety_factor: float = 1.1,
                          stability_coef: float = 0.375,
                          velocity_coef: float = 1.0,
                          thickness_coef: float = 1.0,
                          side_slope_factor: float = 1.0) -> float:
        """
        Calcul inverse: trouve la vitesse max pour un D30 donné

        Args:
            d30_available: D30 disponible (mm)
            depth: Profondeur d'eau (m)
            ... autres coefficients

        Returns:
            Vitesse maximale admissible (m/s)
        """
        d30_m = d30_available / 1000  # Conversion mm → m

        # Réarrangement de l'équation: V = [...] × √(gD(Ss-1))
        # d30 = SF × Cs × Cv × CT × D × (V/√(gD(Ss-1)))^2.5 / K1
        # dim_param^2.5 = d30 × K1 / (SF × Cs × Cv × CT × D)
        # dim_param = (d30 × K1 / (SF × Cs × Cv × CT × D))^0.4

        numerator = d30_m * side_slope_factor
        denominator = safety_factor * stability_coef * velocity_coef * thickness_coef * depth

        if denominator <= 0:
            raise ValueError("Coefficients invalides")

        dim_param = (numerator / denominator) ** 0.4

        # V = dim_param × √(gD(Ss-1))
        v_max = dim_param * math.sqrt(GRAVITY * depth * (specific_gravity - 1))

        return v_max

    @staticmethod
    def _calculate_sphere_mass(diameter_m: float, density: float) -> float:
        """
        Calcule la masse d'une sphère équivalente

        Args:
            diameter_m: Diamètre en mètres
            density: Densité en kg/m³

        Returns:
            Masse en kg
        """
        volume = (math.pi / 6) * (diameter_m ** 3)
        return volume * density


# Fonctions utilitaires de haut niveau
def quick_calculate(velocity: float, depth: float,
                    rock_type: str = "angular") -> MaynordResult:
    """
    Calcul rapide avec paramètres par défaut

    Args:
        velocity: Vitesse (m/s)
        depth: Profondeur (m)
        rock_type: "angular" ou "rounded"

    Returns:
        MaynordResult
    """
    calc = MaynordCalculator()
    cs = 0.375 if rock_type == "angular" else 0.30
    return calc.calculate(velocity=velocity, depth=depth, stability_coef=cs)


def check_stability(velocity: float, depth: float, d30_available: float,
                    specific_gravity: float = 2.65) -> dict:
    """
    Vérifie si un enrochement existant est stable

    Returns:
        dict avec 'is_stable', 'safety_margin', 'max_velocity'
    """
    calc = MaynordCalculator()

    # Calcul du D30 requis
    result = calc.calculate(velocity=velocity, depth=depth,
                           specific_gravity=specific_gravity)
    d30_required = result.d30

    # Calcul de la vitesse max pour le D30 disponible
    v_max = calc.calculate_inverse(d30_available=d30_available, depth=depth,
                                   specific_gravity=specific_gravity)

    safety_margin = (d30_available - d30_required) / d30_required * 100

    return {
        'is_stable': d30_available >= d30_required,
        'd30_required_mm': round(d30_required, 1),
        'd30_available_mm': d30_available,
        'safety_margin_percent': round(safety_margin, 1),
        'max_velocity_ms': round(v_max, 2),
        'current_velocity_ms': velocity,
    }
