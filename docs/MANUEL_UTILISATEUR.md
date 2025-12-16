# Maynord Calculator - Manuel Utilisateur Complet

**Version 1.0** | Developpe par Marc Zermatten | 2025

---

## Table des matieres

1. [Introduction](#1-introduction)
2. [Installation](#2-installation)
3. [Interface utilisateur](#3-interface-utilisateur)
4. [Guide d'utilisation](#4-guide-dutilisation)
5. [Reference technique](#5-reference-technique)
6. [Exemples pratiques](#6-exemples-pratiques)
7. [Export des resultats](#7-export-des-resultats)
8. [Gestion de projets](#8-gestion-de-projets)
9. [Depannage](#9-depannage)
10. [References bibliographiques](#10-references-bibliographiques)

---

## 1. Introduction

### 1.1 Presentation

Maynord Calculator est une application professionnelle de dimensionnement d'enrochements selon la methode USACE/Maynord. Elle est destinee aux ingenieurs civils et hydrauliciens travaillant sur des projets de:

- Renaturation de cours d'eau
- Protection de berges
- Amenagements hydrauliques
- Ouvrages de stabilisation

### 1.2 Fonctionnalites principales

- **Calcul automatique** des diametres D30, D50, D100
- **Estimation des masses** unitaires des blocs
- **Coefficients complets** : SF, Cs, Cv, CT, K1
- **Configuration flexible** : chenal droit, courbe, transition
- **Support des talus** : pentes de 3:1 a 1.5:1
- **Visualisation** : courbe granulometrique interactive
- **Comparaison** : multi-scenarios en tableau
- **Export** : Excel (.xlsx) et PDF
- **Bilingue** : Francais / English
- **Mode sombre** : interface jour/nuit

### 1.3 Domaine de validite

L'equation de Maynord est valide dans les conditions suivantes:

| Parametre | Limite |
|-----------|--------|
| Pente du chenal | < 2% |
| Nombre de Froude | < 1.2 |
| Ratio R/W (courbes) | 2 a 25 |
| Profondeur d'eau | 0.1 a 30 m |
| Vitesse | 0.1 a 15 m/s |

---

## 2. Installation

### 2.1 Prerequis

- **Systeme** : Windows 10/11 (64-bit)
- **Python** : Version 3.11 ou superieure
- **Espace disque** : ~200 Mo

### 2.2 Installation de Python

1. Telecharger Python depuis : https://www.python.org/downloads/
2. Lancer l'installateur
3. **IMPORTANT** : Cocher "Add Python to PATH"
4. Cliquer sur "Install Now"

### 2.3 Lancement de l'application

**Methode simple (recommandee)** :
- Double-cliquer sur `START.bat`
- L'installation des dependances se fait automatiquement au premier lancement
- Les lancements suivants sont instantanes

**Executable standalone** :
- Double-cliquer sur `BUILD.bat` pour creer `dist/MaynordCalculator.exe`
- L'executable (~80 Mo) fonctionne sans Python

---

## 3. Interface utilisateur

### 3.1 Vue d'ensemble

```
+------------------------------------------------------------------+
|  Maynord Calculator          [Sans titre]    [Theme] [FR|EN] [Parametres] |
+------------------------------------------------------------------+
|  [Calculateur]  [Comparaison]  [Projet]                          |
+------------------+-----------------------------------------------+
|                  |                                               |
|  PARAMETRES      |  RESULTATS                                    |
|  HYDRAULIQUES    |  +------------------------------------------+ |
|                  |  | Status: En attente de calcul...          | |
|  Vitesse V       |  +------------------------------------------+ |
|  [====|===] m/s  |  | Diametres caracteristiques               | |
|                  |  | D30 calcule:     -- mm                   | |
|  Profondeur D    |  | D50 estime:      -- mm                   | |
|  [===|====] m    |  | D100 estime:     -- mm                   | |
|                  |  +------------------------------------------+ |
|  CONFIGURATION   |  | Masses unitaires                         | |
|  o Lit de riviere|  | Masse D30:       -- kg                   | |
|  o Talus lateral |  | Masse D50:       -- kg                   | |
|                  |  | Masse D100:      -- kg                   | |
|  COEFFICIENTS    |  +------------------------------------------+ |
|  SF: [1.10]      |                                               |
|  Cs = 0.375      |  +------------------------------------------+ |
|  Cv = 1.000      |  |       Courbe granulometrique             | |
|  K1 = 1.000      |  |           (graphique)                    | |
|  Ss: [2.65]      |  +------------------------------------------+ |
|  CT: [1.00]      |                                               |
|                  |                                               |
|  [Calculer]      |                                               |
|  [Reinitialiser] |                                               |
|                  |                                               |
|  EXPORT          |                                               |
|  [Excel][PDF]    |                                               |
|  [Sauvegarder]   |                                               |
+------------------+-----------------------------------------------+
```

### 3.2 Panneau de gauche : Parametres d'entree

#### Parametres hydrauliques
- **Vitesse V** : Vitesse moyenne de l'ecoulement (m/s)
- **Profondeur D** : Profondeur d'eau moyenne (m)

#### Configuration
- **Type de section** : Lit plat ou talus lateral
- **Pente du talus** : 3:1, 2.5:1, 2:1, ou 1.5:1
- **Configuration chenal** : Droit, transition, ou courbe
- **Ratio R/W** : Pour les courbes (rayon/largeur)

#### Coefficients
- **SF** : Facteur de securite
- **Cs** : Coefficient de stabilite (selon type de roche)
- **Cv** : Coefficient de distribution de vitesse (automatique)
- **K1** : Facteur de pente laterale (automatique)
- **Ss** : Densite relative de la roche
- **CT** : Coefficient d'epaisseur

### 3.3 Panneau de droite : Resultats

- **Status** : Stable / Limite / Erreur
- **Diametres** : D30, D50, D100 en mm
- **Masses** : kg ou tonnes selon la taille
- **Autres** : Epaisseur de couche, classe de gradation, Froude
- **Graphique** : Courbe granulometrique avec annotations

---

## 4. Guide d'utilisation

### 4.1 Calcul simple (lit de riviere)

1. Entrer la **vitesse** de l'ecoulement
2. Entrer la **profondeur** d'eau
3. Verifier que "Lit de riviere" est selectionne
4. Verifier que "Droit" est selectionne
5. Ajuster le **facteur de securite** si necessaire
6. Cliquer sur **Calculer**

### 4.2 Calcul pour talus lateral

1. Selectionner "Talus lateral"
2. Choisir la **pente** du talus (ex: 2:1)
3. Le coefficient K1 se calcule automatiquement
4. Les autres parametres restent identiques
5. Cliquer sur **Calculer**

**Note** : Un talus plus raide necessite des blocs plus gros (K1 plus petit).

### 4.3 Calcul en courbe

1. Selectionner "Courbe" dans Configuration chenal
2. Entrer le **ratio R/W** (rayon de courbure / largeur)
3. Le coefficient Cv se calcule automatiquement
4. Cliquer sur **Calculer**

**Valeurs typiques R/W** :
- < 5 : Courbe serree (Cv eleve)
- 5-15 : Courbe moderee
- > 25 : Quasi-droit (Cv → 1.0)

### 4.4 Interpretation des resultats

#### Status "STABLE" (vert)
Les conditions sont dans le domaine de validite. Les resultats sont fiables.

#### Status "LIMITE" (orange)
Attention requise :
- Froude > 1.2 : conditions supercritiques
- D100 > 1500 mm : blocs tres lourds

#### Status "ERREUR" (rouge)
Parametres hors limites. Verifier les entrees.

### 4.5 Lecture du graphique

La courbe granulometrique montre:
- **Axe X** : Diametre des blocs (mm, echelle log)
- **Axe Y** : Pourcentage passant cumule (%)
- **Points** : D15, D30, D50, D85, D100
- **Lignes verticales** : D30 (vert), D50 (orange), D100 (rouge)

---

## 5. Reference technique

### 5.1 Equation de Maynord

L'equation principale pour le calcul du D30 :

```
D30 = SF x Cs x Cv x CT x D x [V / sqrt(g x D x (Ss - 1))]^2.5 / K1
```

Ou :
- **D30** : Diametre a 30% de passant (m)
- **SF** : Facteur de securite (-)
- **Cs** : Coefficient de stabilite (-)
- **Cv** : Coefficient de distribution de vitesse (-)
- **CT** : Coefficient d'epaisseur (-)
- **D** : Profondeur d'eau (m)
- **V** : Vitesse d'ecoulement (m/s)
- **g** : Acceleration gravitationnelle (9.81 m/s²)
- **Ss** : Densite relative de la roche (-)
- **K1** : Facteur de correction de pente laterale (-)

### 5.2 Facteur de securite (SF)

| Valeur | Application |
|--------|-------------|
| 1.1 | Standard USACE, conditions normales |
| 1.15 | Incertitude moderee sur les donnees |
| 1.2 | Conditions critiques, ouvrages importants |
| 1.25+ | Tres conservateur, donnees incertaines |

### 5.3 Coefficient de stabilite (Cs)

| Type de roche | Cs | Description |
|---------------|-----|-------------|
| Angulaire | 0.375 | Roche concassee, bon imbriquement |
| Arrondie | 0.30 | Galets, moins de friction |

### 5.4 Coefficient de distribution de vitesse (Cv)

**Chenal droit** : Cv = 1.0

**Zone de transition** : Cv = 1.25

**Courbe** (formule de Maynord) :
```
Cv = 1.283 - 0.2 x log10(R/W)   pour 2 < R/W < 25
```

| R/W | Cv |
|-----|-----|
| 2 | 1.22 |
| 5 | 1.14 |
| 10 | 1.08 |
| 20 | 1.02 |
| 25+ | 1.00 |

### 5.5 Facteur de pente laterale (K1)

Pour les talus, K1 reduit la stabilite :

```
K1 = sqrt(1 - sin²(theta) / sin²(phi))
```

Ou :
- **theta** : Angle du talus (degres)
- **phi** : Angle de repos de la roche (~40° pour angulaire)

| Pente (H:V) | Angle | K1 |
|-------------|-------|-----|
| 3:1 | 18.4° | 0.94 |
| 2.5:1 | 21.8° | 0.91 |
| 2:1 | 26.6° | 0.88 |
| 1.5:1 | 33.7° | 0.80 |

### 5.6 Conversions granulometriques

A partir du D30 calcule :

| Percentile | Formule | Description |
|------------|---------|-------------|
| D15 | D30 x 0.70 | Limite fine |
| D50 | D30 x 1.30 | Diametre median |
| D85 | D30 x 1.70 | Bloc typique |
| D100 | D30 x 2.10 | Bloc maximum |

### 5.7 Calcul des masses

Masse d'un bloc spherique equivalent :

```
M = (pi/6) x rho_s x D³
```

Ou :
- **M** : Masse (kg)
- **rho_s** : Masse volumique = Ss x 1000 (kg/m³)
- **D** : Diametre (m)

### 5.8 Epaisseur de couche

Epaisseur minimale recommandee :

```
e = max(D100, 1.5 x D50)
```

### 5.9 Nombre de Froude

Indicateur du regime d'ecoulement :

```
Fr = V / sqrt(g x D)
```

| Froude | Regime |
|--------|--------|
| < 1.0 | Fluvial (sous-critique) |
| = 1.0 | Critique |
| > 1.0 | Torrentiel (supercritique) |

**Attention** : L'equation de Maynord est validee pour Fr < 1.2

---

## 6. Exemples pratiques

### Exemple 1 : Riviere de plaine

**Contexte** : Protection de berge sur une riviere de plaine
- Vitesse de crue : 2.5 m/s
- Profondeur : 2.0 m
- Chenal droit
- Talus 2:1
- Roche angulaire (granite)

**Parametres** :
- V = 2.5 m/s
- D = 2.0 m
- SF = 1.1
- Cs = 0.375
- Cv = 1.0
- K1 = 0.88 (talus 2:1)
- Ss = 2.65
- CT = 1.0

**Resultats attendus** :
- D30 ≈ 180 mm
- D50 ≈ 235 mm
- D100 ≈ 380 mm
- Masse D50 ≈ 18 kg

### Exemple 2 : Torrent de montagne

**Contexte** : Seuil de stabilisation en torrent
- Vitesse : 4.0 m/s
- Profondeur : 0.8 m
- Chenal en courbe (R/W = 8)
- Lit de riviere
- Roche angulaire locale

**Parametres** :
- V = 4.0 m/s
- D = 0.8 m
- SF = 1.2 (conditions severes)
- Cs = 0.375
- Cv = 1.10 (courbe R/W=8)
- K1 = 1.0 (lit)
- Ss = 2.65
- CT = 1.0

**Resultats attendus** :
- D30 ≈ 280 mm
- D50 ≈ 365 mm
- D100 ≈ 590 mm
- Masse D50 ≈ 65 kg

---

## 7. Export des resultats

### 7.1 Export Excel

Le fichier Excel contient :
- Feuille "Parametres" : toutes les valeurs d'entree
- Feuille "Resultats" : D30, D50, D100, masses
- Feuille "Coefficients" : SF, Cs, Cv, K1, CT
- Formules visibles pour verification

### 7.2 Export PDF

Le rapport PDF inclut :
- En-tete avec nom du projet et date
- Tableau des parametres
- Tableau des resultats
- Courbe granulometrique
- Notes et avertissements

### 7.3 Sauvegarde projet

Format `.maynord` (JSON) contenant :
- Historique complet des calculs
- Parametres de chaque scenario
- Metadonnees du projet

---

## 8. Gestion de projets

### 8.1 Creer un projet

Menu Fichier > Nouveau projet (Ctrl+N)

### 8.2 Sauvegarder

- Menu Fichier > Sauvegarder (Ctrl+S)
- Bouton "Sauvegarder" dans l'onglet Calculateur
- Format : `.maynord`

### 8.3 Ouvrir un projet

Menu Fichier > Ouvrir (Ctrl+O)

### 8.4 Onglet Comparaison

Permet de :
- Comparer jusqu'a 10 scenarios
- Visualiser les gradations sur un meme graphique
- Exporter le tableau comparatif

---

## 9. Depannage

### 9.1 L'application ne demarre pas

**Cause possible** : Python non installe ou pas dans le PATH

**Solution** :
1. Verifier que Python est installe : `python --version`
2. Reinstaller Python en cochant "Add to PATH"
3. Redemarrer l'ordinateur

### 9.2 Les valeurs ne s'affichent pas

**Cause possible** : Probleme de rendu graphique

**Solution** :
1. Fermer et relancer l'application
2. Essayer de changer de theme (clair/sombre)

### 9.3 Erreur "Module not found"

**Cause** : Dependances non installees

**Solution** :
1. Supprimer le dossier `venv`
2. Relancer `START.bat`

### 9.4 Export PDF echoue

**Cause possible** : Bibliotheque reportlab manquante

**Solution** :
```
venv\Scripts\pip install reportlab
```

### 9.5 Resultats aberrants

**Verifications** :
- Froude < 1.2 ?
- Pente chenal < 2% ?
- Parametres dans les plages valides ?

---

## 10. References bibliographiques

### Documents techniques

1. **Maynord, S.T. (1988)**
   "Stable Riprap Size for Open Channel Flows"
   Technical Report HL-88-4
   U.S. Army Corps of Engineers
   Waterways Experiment Station

2. **USACE (1994)**
   Engineering Manual EM 1110-2-1601
   "Hydraulic Design of Flood Control Channels"
   U.S. Army Corps of Engineers

3. **HEC-RAS (2020)**
   "Hydraulic Reference Manual"
   U.S. Army Corps of Engineers
   Hydrologic Engineering Center

### Normes et guides

4. **CIRIA/CUR/CETMEF (2007)**
   "The Rock Manual"
   2nd Edition

5. **ASCE (2014)**
   "Sedimentation Engineering"
   Manual of Practice No. 110

### Sites web utiles

- USACE Digital Library : https://usace.contentdm.oclc.org
- HEC-RAS : https://www.hec.usace.army.mil/software/hec-ras/

---

## Annexes

### A. Raccourcis clavier

| Raccourci | Action |
|-----------|--------|
| Ctrl+N | Nouveau projet |
| Ctrl+O | Ouvrir projet |
| Ctrl+S | Sauvegarder |
| Ctrl+Q | Quitter |

### B. Valeurs par defaut

| Parametre | Valeur |
|-----------|--------|
| Vitesse | 2.0 m/s |
| Profondeur | 1.5 m |
| SF | 1.1 |
| Cs | 0.375 |
| Ss | 2.65 |
| CT | 1.0 |

### C. Limites du logiciel

| Parametre | Min | Max |
|-----------|-----|-----|
| Vitesse | 0.1 m/s | 15 m/s |
| Profondeur | 0.1 m | 30 m |
| SF | 1.0 | 2.0 |
| Ss | 2.0 | 3.5 |
| R/W | 2 | 50 |

---

**Maynord Calculator v1.0**
Developpe par Marc Zermatten
2025 GeoMind

*Ce logiciel est fourni "tel quel", sans garantie d'aucune sorte.*
