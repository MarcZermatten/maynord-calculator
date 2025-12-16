"""
Coefficient Calculations for Maynord Equation

Cv - Vertical Velocity Distribution Coefficient
K1 - Side Slope Correction Factor
Cs - Stability Coefficient

Based on USACE EM 1110-2-1601 and HEC-RAS guidelines
"""

import math
from typing import Tuple, Optional
from enum import Enum


class RockType(Enum):
    """Type de roche pour Cs"""
    ROUNDED = "rounded"     # Galets, roche roulée
    ANGULAR = "angular"     # Roche concassée, angulaire


# Valeurs standard de Cs selon USACE
CS_VALUES = {
    RockType.ROUNDED: 0.30,
    RockType.ANGULAR: 0.375,
}


def get_cs_value(rock_type: RockType) -> float:
    """
    Retourne le coefficient de stabilité Cs selon le type de roche

    Args:
        rock_type: Type de roche (ROUNDED ou ANGULAR)

    Returns:
        Cs (0.30 pour arrondi, 0.375 pour angulaire)

    Note:
        - Roche arrondie nécessite un D30 ~25% plus grand
        - Roche angulaire est plus stable grâce à l'imbrication
    """
    return CS_VALUES.get(rock_type, 0.375)


def calculate_cv(channel_type: str = "straight",
                 bend_radius: Optional[float] = None,
                 channel_width: Optional[float] = None) -> float:
    """
    Calcule le coefficient de distribution verticale de vitesse Cv

    Args:
        channel_type: "straight", "transition", ou "bend"
        bend_radius: R - Rayon de courbure (m) - requis si bend
        channel_width: W - Largeur du chenal (m) - requis si bend

    Returns:
        Cv ≥ 1.0

    Formule pour courbes:
        Cv = 1.283 - 0.2 × log10(R/W)  pour 2 < R/W < 25
        Cv = 1.0                        pour R/W > 25

    Valeurs standard:
        - Chenal droit: 1.0
        - Zone de transition: 1.25
        - Courbe: 1.0 à 1.22 selon R/W
    """
    channel_type = channel_type.lower()

    if channel_type == "straight":
        return 1.0

    elif channel_type == "transition":
        return 1.25

    elif channel_type == "bend":
        if bend_radius is None or channel_width is None:
            raise ValueError("bend_radius et channel_width requis pour une courbe")

        if channel_width <= 0:
            raise ValueError("channel_width doit être positif")

        r_w = bend_radius / channel_width

        if r_w <= 0:
            raise ValueError("R/W doit être positif")

        # Limites de validité
        if r_w < 2:
            # Courbe très serrée - utiliser Cv max
            cv = 1.283 - 0.2 * math.log10(2)
            return round(cv, 3)

        elif r_w > 25:
            # Courbe très large - assimilable à chenal droit
            return 1.0

        else:
            # Formule de Maynord
            cv = 1.283 - 0.2 * math.log10(r_w)
            return max(1.0, round(cv, 3))

    else:
        raise ValueError(f"channel_type inconnu: {channel_type}")


def calculate_k1(slope_angle: float,
                 repose_angle: float = 40.0,
                 method: str = "analytical") -> float:
    """
    Calcule le facteur de correction de pente latérale K1

    Args:
        slope_angle: θ - Angle du talus par rapport à l'horizontale (degrés)
        repose_angle: φ - Angle de repos de la roche (degrés), ~40° pour angulaire
        method: "analytical" ou "graphical" (USACE Plate 39)

    Returns:
        K1 ≤ 1.0 (K1=1.0 pour lit plat)

    Formule analytique (Carter, Carleson, Lane 1953):
        K1 = √(1 - sin²(θ)/sin²(φ))

    Note:
        - K1 < 1.0 signifie que le D30 doit être plus grand sur le talus
        - Plus le talus est raide, plus K1 est petit
        - θ doit être < φ sinon instabilité gravitaire
    """
    if slope_angle <= 0:
        return 1.0  # Lit plat

    if slope_angle >= repose_angle:
        raise ValueError(f"Angle du talus ({slope_angle}°) >= angle de repos ({repose_angle}°): instable")

    # Conversion en radians
    theta = math.radians(slope_angle)
    phi = math.radians(repose_angle)

    if method == "analytical":
        # Formule analytique
        sin_theta = math.sin(theta)
        sin_phi = math.sin(phi)

        k1_squared = 1 - (sin_theta ** 2) / (sin_phi ** 2)

        if k1_squared < 0:
            raise ValueError("Calcul impossible: θ trop proche de φ")

        k1 = math.sqrt(k1_squared)
        return round(k1, 3)

    elif method == "graphical":
        # Approximation de la méthode graphique USACE Plate 39
        # Légèrement moins conservative que l'analytique
        ratio = slope_angle / repose_angle
        k1 = math.sqrt(1 - ratio ** 1.8)  # Approximation empirique
        return max(0.1, round(k1, 3))

    else:
        raise ValueError(f"method inconnue: {method}")


def slope_ratio_to_angle(horizontal: float, vertical: float = 1.0) -> float:
    """
    Convertit un ratio de pente (H:V) en angle (degrés)

    Args:
        horizontal: Distance horizontale
        vertical: Distance verticale (défaut 1.0)

    Returns:
        Angle en degrés

    Exemples:
        2:1 → 26.57°
        1.5:1 → 33.69°
        1:1 → 45°
    """
    if horizontal <= 0:
        raise ValueError("horizontal doit être positif")

    angle = math.degrees(math.atan(vertical / horizontal))
    return round(angle, 2)


def angle_to_slope_ratio(angle_deg: float) -> Tuple[float, float]:
    """
    Convertit un angle (degrés) en ratio de pente (H:V)

    Args:
        angle_deg: Angle en degrés

    Returns:
        Tuple (horizontal, vertical=1)

    Exemples:
        26.57° → (2.0, 1)
        33.69° → (1.5, 1)
        45° → (1.0, 1)
    """
    if angle_deg <= 0 or angle_deg >= 90:
        raise ValueError("angle doit être entre 0 et 90 degrés")

    tan_theta = math.tan(math.radians(angle_deg))
    horizontal = 1.0 / tan_theta
    return (round(horizontal, 2), 1.0)


def get_recommended_coefficients(channel_type: str = "straight",
                                 section_type: str = "bed",
                                 rock_type: str = "angular",
                                 slope_ratio: Optional[Tuple[float, float]] = None,
                                 bend_r_w: Optional[float] = None) -> dict:
    """
    Retourne un ensemble de coefficients recommandés

    Args:
        channel_type: "straight", "transition", "bend"
        section_type: "bed" ou "side"
        rock_type: "angular" ou "rounded"
        slope_ratio: (H, V) ex: (2, 1) pour 2:1
        bend_r_w: ratio R/W pour les courbes

    Returns:
        dict avec SF, Cs, Cv, CT, K1
    """
    # Cs selon type de roche
    cs = 0.375 if rock_type == "angular" else 0.30

    # SF recommandé
    sf = 1.1  # Standard USACE

    # CT standard
    ct = 1.0

    # Cv selon configuration
    if channel_type == "straight":
        cv = 1.0
    elif channel_type == "transition":
        cv = 1.25
    elif channel_type == "bend" and bend_r_w:
        cv = calculate_cv("bend", bend_r_w, 1.0)  # Normaliser avec W=1
    else:
        cv = 1.0

    # K1 selon section
    if section_type == "bed":
        k1 = 1.0
    elif section_type == "side" and slope_ratio:
        angle = slope_ratio_to_angle(slope_ratio[0], slope_ratio[1])
        k1 = calculate_k1(angle)
    else:
        k1 = 1.0

    return {
        'SF': sf,
        'Cs': cs,
        'Cv': round(cv, 3),
        'CT': ct,
        'K1': round(k1, 3),
        'description': {
            'SF': 'Facteur de sécurité USACE standard',
            'Cs': f'Roche {"angulaire" if rock_type == "angular" else "arrondie"}',
            'Cv': f'Configuration: {channel_type}',
            'CT': 'Épaisseur standard (1×D100 ou 1.5×D50)',
            'K1': f'Section: {section_type}' + (f' pente {slope_ratio[0]}:{slope_ratio[1]}' if slope_ratio else ''),
        }
    }


# Tableau des pentes courantes
COMMON_SLOPES = {
    '3:1': {'angle': 18.43, 'k1_approx': 0.88},
    '2.5:1': {'angle': 21.80, 'k1_approx': 0.84},
    '2:1': {'angle': 26.57, 'k1_approx': 0.77},
    '1.5:1': {'angle': 33.69, 'k1_approx': 0.64},
    '1:1': {'angle': 45.00, 'k1_approx': 0.40},  # Limite pratique
}


def get_k1_for_common_slope(slope_str: str, repose_angle: float = 40.0) -> float:
    """
    Retourne K1 pour une pente courante

    Args:
        slope_str: "2:1", "1.5:1", etc.
        repose_angle: Angle de repos (degrés)

    Returns:
        K1
    """
    if slope_str in COMMON_SLOPES:
        angle = COMMON_SLOPES[slope_str]['angle']
        return calculate_k1(angle, repose_angle)
    else:
        raise ValueError(f"Pente {slope_str} non reconnue. Utiliser: {list(COMMON_SLOPES.keys())}")
