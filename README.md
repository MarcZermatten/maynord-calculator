# Maynord Calculator

Application de dimensionnement d'enrochements selon la méthode USACE/Maynord pour les projets de renaturation de cours d'eau et d'ingénierie hydraulique.

## Fonctionnalités

- **Calculateur Maynord** : Calcul du D30, D50, D100 et masses correspondantes
- **Coefficients complets** : SF, Cs, Cv, CT, K1 tous modifiables
- **Configuration chenal** : Droit, transition, courbe avec calcul automatique de Cv
- **Talus latéraux** : Support des pentes 3:1 à 1:1 avec calcul de K1
- **Comparaison** : Multi-scénarios en tableau avec graphique comparatif
- **Gestion de projets** : Sauvegarde/chargement au format .maynord
- **Export** : Excel (.xlsx) et PDF
- **Bilingue** : Interface FR/EN

## Installation rapide (Windows)

### Methode 1 : Un seul clic (Recommande)

1. Installer Python 3.11+ depuis : https://www.python.org/downloads/
   - **IMPORTANT** : Cocher "Add Python to PATH" lors de l'installation !

2. Double-cliquer sur **`START.bat`**
   - L'installation se fait automatiquement au premier lancement
   - Les fois suivantes, l'application demarre directement

### Methode 2 : Executable standalone

Double-cliquer sur `BUILD.bat` pour generer `dist/MaynordCalculator.exe`

L'executable (~80 Mo) est autonome et peut etre distribue sans avoir Python installe.

## Installation manuelle

```bash
cd maynord-calculator
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

## Build manuel

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="MaynordCalculator" src/main.py
```

## Équation de Maynord

```
d30 = SF × Cs × Cv × CT × D × [V / √(g × D × (Ss - 1))]^2.5 / K1
```

### Paramètres

| Paramètre | Description | Valeurs typiques |
|-----------|-------------|------------------|
| **SF** | Facteur de sécurité | 1.1 (USACE standard) |
| **Cs** | Coefficient de stabilité | 0.30 (arrondi), 0.375 (angulaire) |
| **Cv** | Coefficient distribution vitesse | 1.0 (droit), 1.25 (transition) |
| **CT** | Coefficient d'épaisseur | 1.0 (standard) |
| **K1** | Correction pente latérale | 1.0 (lit), <1.0 (talus) |
| **D** | Profondeur d'eau | m |
| **V** | Vitesse d'écoulement | m/s |
| **Ss** | Densité relative roche | 2.65 (granite typique) |

### Domaine de validité

- Pente du chenal < 2%
- Nombre de Froude < 1.2

## Références

- Maynord, S.T. (1988). "Stable Riprap Size for Open Channel Flows". Technical Report HL-88-4, U.S. Army Corps of Engineers.
- USACE Engineering Manual EM 1110-2-1601: Hydraulic Design of Flood Control Channels
- HEC-RAS Hydraulic Reference Manual

## Licence

MIT

## Auteur

Développé par GeoBrain pour les bureaux d'ingénieurs civils.
