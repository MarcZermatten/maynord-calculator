"""
Internationalization (i18n) for Maynord Calculator
Supports: French (FR) and English (EN)
"""

from typing import Dict
from enum import Enum


class Language(Enum):
    FR = "fr"
    EN = "en"


# Current language (mutable at runtime)
_current_language = Language.FR


def set_language(lang: Language):
    """Set the current language"""
    global _current_language
    _current_language = lang


def get_language() -> Language:
    """Get the current language"""
    return _current_language


def tr(key: str) -> str:
    """
    Translate a key to the current language

    Args:
        key: Translation key (e.g., "main.title")

    Returns:
        Translated string
    """
    lang = _current_language.value
    keys = key.split('.')

    result = TRANSLATIONS.get(lang, TRANSLATIONS['fr'])
    for k in keys:
        if isinstance(result, dict):
            result = result.get(k, key)
        else:
            return key
    return result if isinstance(result, str) else key


TRANSLATIONS: Dict[str, Dict] = {
    'fr': {
        'app': {
            'title': 'Maynord Calculator',
            'subtitle': 'Dimensionnement d\'enrochements',
        },
        'tabs': {
            'calculator': 'Calculateur',
            'comparison': 'Comparaison',
            'project': 'Projet',
            'settings': 'Paramètres',
        },
        'input': {
            'title': 'Paramètres hydrauliques',
            'velocity': 'Vitesse V',
            'velocity_unit': 'm/s',
            'depth': 'Profondeur D',
            'depth_unit': 'm',
            'section_type': 'Type de section',
            'bed': 'Lit de rivière',
            'side_slope': 'Talus latéral',
            'slope_angle': 'Angle du talus',
            'slope_ratio': 'Pente (H:V)',
            'channel_config': 'Configuration du chenal',
            'straight': 'Chenal droit',
            'transition': 'Zone de transition',
            'bend': 'Courbe',
            'bend_radius': 'Rayon de courbure R',
            'channel_width': 'Largeur du chenal W',
        },
        'coefficients': {
            'title': 'Coefficients',
            'safety_factor': 'Facteur de sécurité SF',
            'stability': 'Coefficient de stabilité Cs',
            'rock_type': 'Type de roche',
            'angular': 'Angulaire (concassé)',
            'rounded': 'Arrondi (galets)',
            'custom': 'Personnalisé',
            'velocity_coef': 'Coefficient de vitesse Cv',
            'thickness_coef': 'Coefficient d\'épaisseur CT',
            'side_slope_factor': 'Facteur de pente K1',
            'specific_gravity': 'Densité relative Ss',
        },
        'results': {
            'title': 'Résultats',
            'd30': 'D30 calculé',
            'd50': 'D50 estimé',
            'd100': 'D100 estimé',
            'mass_d30': 'Masse D30',
            'mass_d50': 'Masse D50',
            'mass_d100': 'Masse D100',
            'thickness': 'Épaisseur de couche',
            'gradation_class': 'Classe de gradation',
            'froude': 'Nombre de Froude',
            'status': 'Statut',
            'stable': 'STABLE',
            'marginal': 'LIMITE',
            'unstable': 'INSTABLE',
            'mass_per_m2': 'Masse par m²',
        },
        'units': {
            'mm': 'mm',
            'cm': 'cm',
            'm': 'm',
            'kg': 'kg',
            'kg_m2': 'kg/m²',
            't': 't',
            'ms': 'm/s',
            'degrees': '°',
        },
        'buttons': {
            'calculate': 'Calculer',
            'reset': 'Réinitialiser',
            'export_excel': 'Export Excel',
            'export_pdf': 'Export PDF',
            'save': 'Sauvegarder',
            'load': 'Charger',
            'new_project': 'Nouveau projet',
            'add_scenario': 'Ajouter scénario',
            'delete': 'Supprimer',
        },
        'messages': {
            'warning': 'Attention',
            'error': 'Erreur',
            'success': 'Succès',
            'froude_warning': 'Froude > 1.2: hors domaine de validité',
            'slope_warning': 'Pente > 2%: extrapolation',
            'saved': 'Projet sauvegardé',
            'exported': 'Export réussi',
        },
        'project': {
            'title': 'Gestion de projet',
            'name': 'Nom du projet',
            'engineer': 'Ingénieur',
            'date': 'Date',
            'location': 'Localisation',
            'notes': 'Notes',
            'history': 'Historique des calculs',
        },
        'comparison': {
            'title': 'Comparaison de scénarios',
            'scenario': 'Scénario',
            'description': 'Description',
            'import_excel': 'Importer depuis Excel',
        },
        'settings': {
            'title': 'Paramètres',
            'language': 'Langue',
            'theme': 'Thème',
            'light': 'Clair',
            'dark': 'Sombre',
            'precision': 'Précision d\'affichage',
            'default_values': 'Valeurs par défaut',
            'about': 'À propos',
        },
        'about': {
            'title': 'À propos',
            'version': 'Version',
            'description': 'Application de dimensionnement d\'enrochements selon la méthode Maynord (USACE)',
            'references': 'Références',
            'ref1': 'Maynord, S.T. (1988) - Technical Report HL-88-4',
            'ref2': 'USACE EM 1110-2-1601',
            'ref3': 'HEC-RAS Hydraulic Reference Manual',
        },
    },
    'en': {
        'app': {
            'title': 'Maynord Calculator',
            'subtitle': 'Riprap Sizing',
        },
        'tabs': {
            'calculator': 'Calculator',
            'comparison': 'Comparison',
            'project': 'Project',
            'settings': 'Settings',
        },
        'input': {
            'title': 'Hydraulic Parameters',
            'velocity': 'Velocity V',
            'velocity_unit': 'm/s',
            'depth': 'Depth D',
            'depth_unit': 'm',
            'section_type': 'Section Type',
            'bed': 'Channel Bed',
            'side_slope': 'Side Slope',
            'slope_angle': 'Slope Angle',
            'slope_ratio': 'Slope (H:V)',
            'channel_config': 'Channel Configuration',
            'straight': 'Straight Channel',
            'transition': 'Transition Zone',
            'bend': 'Bend',
            'bend_radius': 'Bend Radius R',
            'channel_width': 'Channel Width W',
        },
        'coefficients': {
            'title': 'Coefficients',
            'safety_factor': 'Safety Factor SF',
            'stability': 'Stability Coefficient Cs',
            'rock_type': 'Rock Type',
            'angular': 'Angular (crushed)',
            'rounded': 'Rounded (cobbles)',
            'custom': 'Custom',
            'velocity_coef': 'Velocity Coefficient Cv',
            'thickness_coef': 'Thickness Coefficient CT',
            'side_slope_factor': 'Side Slope Factor K1',
            'specific_gravity': 'Specific Gravity Ss',
        },
        'results': {
            'title': 'Results',
            'd30': 'D30 Calculated',
            'd50': 'D50 Estimated',
            'd100': 'D100 Estimated',
            'mass_d30': 'Mass D30',
            'mass_d50': 'Mass D50',
            'mass_d100': 'Mass D100',
            'thickness': 'Layer Thickness',
            'gradation_class': 'Gradation Class',
            'froude': 'Froude Number',
            'status': 'Status',
            'stable': 'STABLE',
            'marginal': 'MARGINAL',
            'unstable': 'UNSTABLE',
            'mass_per_m2': 'Mass per m²',
        },
        'units': {
            'mm': 'mm',
            'cm': 'cm',
            'm': 'm',
            'kg': 'kg',
            'kg_m2': 'kg/m²',
            't': 't',
            'ms': 'm/s',
            'degrees': '°',
        },
        'buttons': {
            'calculate': 'Calculate',
            'reset': 'Reset',
            'export_excel': 'Export Excel',
            'export_pdf': 'Export PDF',
            'save': 'Save',
            'load': 'Load',
            'new_project': 'New Project',
            'add_scenario': 'Add Scenario',
            'delete': 'Delete',
        },
        'messages': {
            'warning': 'Warning',
            'error': 'Error',
            'success': 'Success',
            'froude_warning': 'Froude > 1.2: outside validity range',
            'slope_warning': 'Slope > 2%: extrapolation',
            'saved': 'Project saved',
            'exported': 'Export successful',
        },
        'project': {
            'title': 'Project Management',
            'name': 'Project Name',
            'engineer': 'Engineer',
            'date': 'Date',
            'location': 'Location',
            'notes': 'Notes',
            'history': 'Calculation History',
        },
        'comparison': {
            'title': 'Scenario Comparison',
            'scenario': 'Scenario',
            'description': 'Description',
            'import_excel': 'Import from Excel',
        },
        'settings': {
            'title': 'Settings',
            'language': 'Language',
            'theme': 'Theme',
            'light': 'Light',
            'dark': 'Dark',
            'precision': 'Display Precision',
            'default_values': 'Default Values',
            'about': 'About',
        },
        'about': {
            'title': 'About',
            'version': 'Version',
            'description': 'Riprap sizing application using the Maynord method (USACE)',
            'references': 'References',
            'ref1': 'Maynord, S.T. (1988) - Technical Report HL-88-4',
            'ref2': 'USACE EM 1110-2-1601',
            'ref3': 'HEC-RAS Hydraulic Reference Manual',
        },
    },
}
