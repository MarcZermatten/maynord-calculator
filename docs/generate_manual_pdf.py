"""
Generate Professional PDF Manual for Maynord Calculator
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import os


# Colors
PRIMARY_BLUE = HexColor('#1e40af')
LIGHT_BLUE = HexColor('#dbeafe')
DARK_GRAY = HexColor('#334155')
LIGHT_GRAY = HexColor('#f1f5f9')
GREEN = HexColor('#16a34a')
ORANGE = HexColor('#f59e0b')
RED = HexColor('#dc2626')


def create_styles():
    """Create custom paragraph styles"""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='MainTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=PRIMARY_BLUE,
        alignment=TA_CENTER,
        spaceAfter=20,
        spaceBefore=40
    ))

    styles.add(ParagraphStyle(
        name='Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=DARK_GRAY,
        alignment=TA_CENTER,
        spaceAfter=30
    ))

    styles.add(ParagraphStyle(
        name='ChapterTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=PRIMARY_BLUE,
        spaceBefore=30,
        spaceAfter=15,
        borderPadding=10,
        borderWidth=0,
        borderColor=PRIMARY_BLUE
    ))

    styles.add(ParagraphStyle(
        name='SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=PRIMARY_BLUE,
        spaceBefore=20,
        spaceAfter=10
    ))

    styles.add(ParagraphStyle(
        name='SubsectionTitle',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=DARK_GRAY,
        spaceBefore=15,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name='Body',
        parent=styles['Normal'],
        fontSize=10,
        textColor=black,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=14
    ))

    styles.add(ParagraphStyle(
        name='Formula',
        parent=styles['Normal'],
        fontSize=11,
        textColor=PRIMARY_BLUE,
        alignment=TA_CENTER,
        spaceBefore=10,
        spaceAfter=10,
        fontName='Courier-Bold'
    ))

    styles.add(ParagraphStyle(
        name='Note',
        parent=styles['Normal'],
        fontSize=9,
        textColor=DARK_GRAY,
        leftIndent=20,
        rightIndent=20,
        spaceBefore=5,
        spaceAfter=5,
        backColor=LIGHT_GRAY
    ))

    styles.add(ParagraphStyle(
        name='TableHeader',
        parent=styles['Normal'],
        fontSize=10,
        textColor=white,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))

    styles.add(ParagraphStyle(
        name='Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=DARK_GRAY,
        alignment=TA_CENTER
    ))

    return styles


def add_header_footer(canvas, doc):
    """Add header and footer to each page"""
    canvas.saveState()

    # Header line
    canvas.setStrokeColor(PRIMARY_BLUE)
    canvas.setLineWidth(2)
    canvas.line(2*cm, A4[1] - 1.5*cm, A4[0] - 2*cm, A4[1] - 1.5*cm)

    # Header text
    canvas.setFont('Helvetica-Bold', 9)
    canvas.setFillColor(PRIMARY_BLUE)
    canvas.drawString(2*cm, A4[1] - 1.2*cm, "Maynord Calculator - Manuel Utilisateur")

    # Page number
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(DARK_GRAY)
    canvas.drawRightString(A4[0] - 2*cm, 1.5*cm, f"Page {doc.page}")

    # Footer line
    canvas.setLineWidth(1)
    canvas.line(2*cm, 2*cm, A4[0] - 2*cm, 2*cm)

    # Footer text
    canvas.setFont('Helvetica', 8)
    canvas.drawCentredString(A4[0]/2, 1*cm, "2025 GeoMind - Developpe par Marc Zermatten")

    canvas.restoreState()


def create_table(data, col_widths=None, header=True):
    """Create a styled table"""
    table = Table(data, colWidths=col_widths)

    style_commands = [
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, DARK_GRAY),
    ]

    if header:
        style_commands.extend([
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_BLUE),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, -1), white),
        ])

        # Alternate row colors
        for i in range(1, len(data)):
            if i % 2 == 0:
                style_commands.append(('BACKGROUND', (0, i), (-1, i), LIGHT_GRAY))

    table.setStyle(TableStyle(style_commands))
    return table


def generate_manual():
    """Generate the complete PDF manual"""
    output_path = os.path.join(os.path.dirname(__file__), 'MANUEL_MAYNORD_CALCULATOR.pdf')

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm
    )

    styles = create_styles()
    story = []

    # ==================== COVER PAGE ====================
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("MAYNORD CALCULATOR", styles['MainTitle']))
    story.append(Paragraph("Manuel Utilisateur Complet", styles['Subtitle']))
    story.append(Spacer(1, 2*cm))

    story.append(Paragraph(
        "Application de dimensionnement d'enrochements<br/>"
        "selon la methode USACE/Maynord",
        styles['Subtitle']
    ))

    story.append(Spacer(1, 3*cm))

    # Version info table
    version_data = [
        ['Version', '1.0'],
        ['Date', datetime.now().strftime('%d/%m/%Y')],
        ['Auteur', 'Marc Zermatten'],
        ['Organisation', 'GeoMind'],
    ]
    story.append(create_table(version_data, col_widths=[4*cm, 6*cm], header=False))

    story.append(PageBreak())

    # ==================== TABLE OF CONTENTS ====================
    story.append(Paragraph("Table des matieres", styles['ChapterTitle']))
    story.append(Spacer(1, 0.5*cm))

    toc_items = [
        ("1. Introduction", "3"),
        ("2. Installation", "4"),
        ("3. Interface utilisateur", "5"),
        ("4. Guide d'utilisation", "6"),
        ("5. Reference technique", "8"),
        ("6. Exemples pratiques", "11"),
        ("7. Export des resultats", "12"),
        ("8. Depannage", "13"),
        ("9. References", "14"),
    ]

    toc_data = [[item[0], item[1]] for item in toc_items]
    toc_table = Table(toc_data, colWidths=[12*cm, 2*cm])
    toc_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
    ]))
    story.append(toc_table)

    story.append(PageBreak())

    # ==================== CHAPTER 1: INTRODUCTION ====================
    story.append(Paragraph("1. Introduction", styles['ChapterTitle']))

    story.append(Paragraph("1.1 Presentation", styles['SectionTitle']))
    story.append(Paragraph(
        "Maynord Calculator est une application professionnelle de dimensionnement "
        "d'enrochements selon la methode USACE/Maynord. Elle est destinee aux ingenieurs "
        "civils et hydrauliciens travaillant sur des projets de renaturation de cours d'eau, "
        "protection de berges et amenagements hydrauliques.",
        styles['Body']
    ))

    story.append(Paragraph("1.2 Fonctionnalites principales", styles['SectionTitle']))

    features = [
        "Calcul automatique des diametres D30, D50, D100",
        "Estimation des masses unitaires des blocs",
        "Coefficients complets : SF, Cs, Cv, CT, K1",
        "Configuration flexible : chenal droit, courbe, transition",
        "Support des talus : pentes de 3:1 a 1.5:1",
        "Visualisation : courbe granulometrique interactive",
        "Export : Excel (.xlsx) et PDF",
        "Interface bilingue : Francais / English",
        "Mode sombre disponible",
    ]

    for feat in features:
        story.append(Paragraph(f"- {feat}", styles['Body']))

    story.append(Paragraph("1.3 Domaine de validite", styles['SectionTitle']))
    story.append(Paragraph(
        "L'equation de Maynord est valide dans les conditions suivantes :",
        styles['Body']
    ))

    validity_data = [
        ['Parametre', 'Limite'],
        ['Pente du chenal', '< 2%'],
        ['Nombre de Froude', '< 1.2'],
        ['Ratio R/W (courbes)', '2 a 25'],
        ['Profondeur d\'eau', '0.1 a 30 m'],
        ['Vitesse', '0.1 a 15 m/s'],
    ]
    story.append(Spacer(1, 0.3*cm))
    story.append(create_table(validity_data, col_widths=[6*cm, 6*cm]))

    story.append(PageBreak())

    # ==================== CHAPTER 2: INSTALLATION ====================
    story.append(Paragraph("2. Installation", styles['ChapterTitle']))

    story.append(Paragraph("2.1 Prerequis", styles['SectionTitle']))
    prereq_data = [
        ['Composant', 'Requis'],
        ['Systeme', 'Windows 10/11 (64-bit)'],
        ['Python', 'Version 3.11 ou superieure'],
        ['Espace disque', '~200 Mo'],
    ]
    story.append(create_table(prereq_data, col_widths=[5*cm, 7*cm]))

    story.append(Paragraph("2.2 Procedure d'installation", styles['SectionTitle']))
    story.append(Paragraph(
        "<b>Etape 1 :</b> Telecharger Python depuis python.org/downloads",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>IMPORTANT :</b> Cocher 'Add Python to PATH' lors de l'installation !",
        styles['Note']
    ))
    story.append(Paragraph(
        "<b>Etape 2 :</b> Double-cliquer sur START.bat",
        styles['Body']
    ))
    story.append(Paragraph(
        "L'installation des dependances se fait automatiquement au premier lancement. "
        "Les lancements suivants sont instantanes.",
        styles['Body']
    ))

    story.append(PageBreak())

    # ==================== CHAPTER 3: INTERFACE ====================
    story.append(Paragraph("3. Interface utilisateur", styles['ChapterTitle']))

    story.append(Paragraph("3.1 Panneau de gauche : Parametres d'entree", styles['SectionTitle']))

    story.append(Paragraph("Parametres hydrauliques", styles['SubsectionTitle']))
    params_data = [
        ['Parametre', 'Description', 'Unite'],
        ['Vitesse V', 'Vitesse moyenne de l\'ecoulement', 'm/s'],
        ['Profondeur D', 'Profondeur d\'eau moyenne', 'm'],
    ]
    story.append(create_table(params_data, col_widths=[4*cm, 7*cm, 3*cm]))

    story.append(Paragraph("Configuration", styles['SubsectionTitle']))
    config_data = [
        ['Option', 'Description'],
        ['Lit de riviere', 'Enrochement sur le fond (K1=1.0)'],
        ['Talus lateral', 'Enrochement sur berge inclinee'],
        ['Chenal droit', 'Distribution uniforme (Cv=1.0)'],
        ['Transition', 'Zone de changement (Cv=1.25)'],
        ['Courbe', 'Section en courbe (Cv calcule)'],
    ]
    story.append(create_table(config_data, col_widths=[4*cm, 10*cm]))

    story.append(Paragraph("3.2 Panneau de droite : Resultats", styles['SectionTitle']))
    story.append(Paragraph(
        "Le panneau de resultats affiche les diametres calcules (D30, D50, D100), "
        "les masses correspondantes, l'epaisseur de couche recommandee et le nombre de Froude. "
        "Un graphique interactif montre la courbe granulometrique.",
        styles['Body']
    ))

    story.append(PageBreak())

    # ==================== CHAPTER 4: GUIDE ====================
    story.append(Paragraph("4. Guide d'utilisation", styles['ChapterTitle']))

    story.append(Paragraph("4.1 Calcul simple (lit de riviere)", styles['SectionTitle']))
    steps = [
        "Entrer la vitesse de l'ecoulement",
        "Entrer la profondeur d'eau",
        "Verifier que 'Lit de riviere' est selectionne",
        "Verifier que 'Droit' est selectionne",
        "Ajuster le facteur de securite si necessaire",
        "Cliquer sur Calculer",
    ]
    for i, step in enumerate(steps, 1):
        story.append(Paragraph(f"{i}. {step}", styles['Body']))

    story.append(Paragraph("4.2 Calcul pour talus lateral", styles['SectionTitle']))
    story.append(Paragraph(
        "Pour les berges inclinees, selectionnez 'Talus lateral' et choisissez la pente. "
        "Le coefficient K1 se calcule automatiquement. Un talus plus raide necessite "
        "des blocs plus gros (K1 plus petit).",
        styles['Body']
    ))

    story.append(Paragraph("4.3 Calcul en courbe", styles['SectionTitle']))
    story.append(Paragraph(
        "Pour les sections en courbe, selectionnez 'Courbe' et entrez le ratio R/W "
        "(rayon de courbure / largeur du chenal). Le coefficient Cv est calcule "
        "automatiquement selon la formule de Maynord.",
        styles['Body']
    ))

    rw_data = [
        ['R/W', 'Cv', 'Type de courbe'],
        ['< 5', '> 1.14', 'Courbe serree'],
        ['5-15', '1.08-1.14', 'Courbe moderee'],
        ['> 25', '~1.0', 'Quasi-droit'],
    ]
    story.append(Spacer(1, 0.3*cm))
    story.append(create_table(rw_data, col_widths=[3*cm, 3*cm, 6*cm]))

    story.append(Paragraph("4.4 Interpretation des resultats", styles['SectionTitle']))

    status_data = [
        ['Status', 'Signification'],
        ['STABLE (vert)', 'Conditions dans le domaine de validite'],
        ['LIMITE (orange)', 'Attention requise (Froude > 1.2 ou D100 > 1500mm)'],
        ['ERREUR (rouge)', 'Parametres hors limites'],
    ]
    story.append(create_table(status_data, col_widths=[4*cm, 10*cm]))

    story.append(PageBreak())

    # ==================== CHAPTER 5: REFERENCE TECHNIQUE ====================
    story.append(Paragraph("5. Reference technique", styles['ChapterTitle']))

    story.append(Paragraph("5.1 Equation de Maynord", styles['SectionTitle']))
    story.append(Paragraph(
        "D30 = SF x Cs x Cv x CT x D x [V / sqrt(g x D x (Ss - 1))]^2.5 / K1",
        styles['Formula']
    ))

    story.append(Paragraph("Parametres de l'equation :", styles['SubsectionTitle']))
    eq_params = [
        ['Symbole', 'Description', 'Unite'],
        ['D30', 'Diametre a 30% de passant', 'm'],
        ['SF', 'Facteur de securite', '-'],
        ['Cs', 'Coefficient de stabilite', '-'],
        ['Cv', 'Coefficient de distribution de vitesse', '-'],
        ['CT', 'Coefficient d\'epaisseur', '-'],
        ['D', 'Profondeur d\'eau', 'm'],
        ['V', 'Vitesse d\'ecoulement', 'm/s'],
        ['g', 'Acceleration gravitationnelle', '9.81 m/s2'],
        ['Ss', 'Densite relative de la roche', '-'],
        ['K1', 'Facteur de correction de pente', '-'],
    ]
    story.append(create_table(eq_params, col_widths=[2.5*cm, 7*cm, 3*cm]))

    story.append(Paragraph("5.2 Facteur de securite (SF)", styles['SectionTitle']))
    sf_data = [
        ['Valeur', 'Application'],
        ['1.1', 'Standard USACE, conditions normales'],
        ['1.15', 'Incertitude moderee sur les donnees'],
        ['1.2', 'Conditions critiques, ouvrages importants'],
        ['1.25+', 'Tres conservateur, donnees incertaines'],
    ]
    story.append(create_table(sf_data, col_widths=[3*cm, 10*cm]))

    story.append(Paragraph("5.3 Coefficient de stabilite (Cs)", styles['SectionTitle']))
    cs_data = [
        ['Type de roche', 'Cs', 'Description'],
        ['Angulaire', '0.375', 'Roche concassee, bon imbriquement'],
        ['Arrondie', '0.30', 'Galets, moins de friction'],
    ]
    story.append(create_table(cs_data, col_widths=[4*cm, 2*cm, 7*cm]))

    story.append(Paragraph("5.4 Coefficient de distribution de vitesse (Cv)", styles['SectionTitle']))
    story.append(Paragraph(
        "Chenal droit : Cv = 1.0<br/>"
        "Zone de transition : Cv = 1.25<br/>"
        "Courbe : Cv = 1.283 - 0.2 x log10(R/W)  pour 2 < R/W < 25",
        styles['Body']
    ))

    story.append(Paragraph("5.5 Facteur de pente laterale (K1)", styles['SectionTitle']))
    story.append(Paragraph(
        "K1 = sqrt(1 - sin2(theta) / sin2(phi))<br/>"
        "ou theta = angle du talus, phi = angle de repos (~40 deg)",
        styles['Body']
    ))

    k1_data = [
        ['Pente (H:V)', 'Angle', 'K1'],
        ['3:1', '18.4 deg', '0.94'],
        ['2.5:1', '21.8 deg', '0.91'],
        ['2:1', '26.6 deg', '0.88'],
        ['1.5:1', '33.7 deg', '0.80'],
    ]
    story.append(create_table(k1_data, col_widths=[4*cm, 4*cm, 4*cm]))

    story.append(PageBreak())

    story.append(Paragraph("5.6 Conversions granulometriques", styles['SectionTitle']))
    conv_data = [
        ['Percentile', 'Formule', 'Description'],
        ['D15', 'D30 x 0.70', 'Limite fine'],
        ['D50', 'D30 x 1.30', 'Diametre median'],
        ['D85', 'D30 x 1.70', 'Bloc typique'],
        ['D100', 'D30 x 2.10', 'Bloc maximum'],
    ]
    story.append(create_table(conv_data, col_widths=[3*cm, 4*cm, 6*cm]))

    story.append(Paragraph("5.7 Calcul des masses", styles['SectionTitle']))
    story.append(Paragraph(
        "M = (pi/6) x rho_s x D^3",
        styles['Formula']
    ))
    story.append(Paragraph(
        "ou M = masse (kg), rho_s = Ss x 1000 (kg/m3), D = diametre (m)",
        styles['Body']
    ))

    story.append(PageBreak())

    # ==================== CHAPTER 6: EXAMPLES ====================
    story.append(Paragraph("6. Exemples pratiques", styles['ChapterTitle']))

    story.append(Paragraph("6.1 Riviere de plaine", styles['SectionTitle']))
    story.append(Paragraph(
        "<b>Contexte :</b> Protection de berge sur une riviere de plaine",
        styles['Body']
    ))

    ex1_params = [
        ['Parametre', 'Valeur'],
        ['Vitesse de crue', '2.5 m/s'],
        ['Profondeur', '2.0 m'],
        ['Configuration', 'Chenal droit, talus 2:1'],
        ['Roche', 'Angulaire (granite)'],
    ]
    story.append(create_table(ex1_params, col_widths=[5*cm, 5*cm]))

    story.append(Paragraph("<b>Resultats attendus :</b>", styles['Body']))
    ex1_results = [
        ['D30', '~180 mm'],
        ['D50', '~235 mm'],
        ['D100', '~380 mm'],
        ['Masse D50', '~18 kg'],
    ]
    story.append(create_table(ex1_results, col_widths=[5*cm, 5*cm]))

    story.append(Paragraph("6.2 Torrent de montagne", styles['SectionTitle']))
    story.append(Paragraph(
        "<b>Contexte :</b> Seuil de stabilisation en torrent",
        styles['Body']
    ))

    ex2_params = [
        ['Parametre', 'Valeur'],
        ['Vitesse', '4.0 m/s'],
        ['Profondeur', '0.8 m'],
        ['Configuration', 'Courbe (R/W=8), lit'],
        ['SF', '1.2 (conditions severes)'],
    ]
    story.append(create_table(ex2_params, col_widths=[5*cm, 5*cm]))

    story.append(Paragraph("<b>Resultats attendus :</b>", styles['Body']))
    ex2_results = [
        ['D30', '~280 mm'],
        ['D50', '~365 mm'],
        ['D100', '~590 mm'],
        ['Masse D50', '~65 kg'],
    ]
    story.append(create_table(ex2_results, col_widths=[5*cm, 5*cm]))

    story.append(PageBreak())

    # ==================== CHAPTER 7: EXPORT ====================
    story.append(Paragraph("7. Export des resultats", styles['ChapterTitle']))

    story.append(Paragraph("7.1 Export Excel", styles['SectionTitle']))
    story.append(Paragraph(
        "Le fichier Excel genere contient toutes les valeurs d'entree, "
        "les resultats calcules et les coefficients utilises. "
        "Les formules sont visibles pour verification.",
        styles['Body']
    ))

    story.append(Paragraph("7.2 Export PDF", styles['SectionTitle']))
    story.append(Paragraph(
        "Le rapport PDF inclut un en-tete avec le nom du projet, "
        "les tableaux de parametres et resultats, "
        "ainsi que la courbe granulometrique.",
        styles['Body']
    ))

    story.append(Paragraph("7.3 Sauvegarde projet", styles['SectionTitle']))
    story.append(Paragraph(
        "Le format .maynord permet de sauvegarder l'historique complet "
        "des calculs et de les recharger ulterieurement.",
        styles['Body']
    ))

    story.append(PageBreak())

    # ==================== CHAPTER 8: TROUBLESHOOTING ====================
    story.append(Paragraph("8. Depannage", styles['ChapterTitle']))

    trouble_data = [
        ['Probleme', 'Solution'],
        ['Application ne demarre pas', 'Verifier que Python est installe et dans le PATH'],
        ['Valeurs invisibles', 'Relancer l\'application ou changer de theme'],
        ['Module not found', 'Supprimer le dossier venv et relancer START.bat'],
        ['Export PDF echoue', 'Installer reportlab : pip install reportlab'],
        ['Resultats aberrants', 'Verifier que Froude < 1.2 et pente < 2%'],
    ]
    story.append(create_table(trouble_data, col_widths=[5*cm, 9*cm]))

    story.append(PageBreak())

    # ==================== CHAPTER 9: REFERENCES ====================
    story.append(Paragraph("9. References bibliographiques", styles['ChapterTitle']))

    story.append(Paragraph("Documents techniques", styles['SectionTitle']))
    refs = [
        "Maynord, S.T. (1988) - 'Stable Riprap Size for Open Channel Flows' - Technical Report HL-88-4, U.S. Army Corps of Engineers",
        "USACE (1994) - Engineering Manual EM 1110-2-1601 'Hydraulic Design of Flood Control Channels'",
        "HEC-RAS (2020) - 'Hydraulic Reference Manual', Hydrologic Engineering Center",
        "CIRIA/CUR/CETMEF (2007) - 'The Rock Manual', 2nd Edition",
    ]
    for ref in refs:
        story.append(Paragraph(f"- {ref}", styles['Body']))

    story.append(Spacer(1, 2*cm))
    story.append(Paragraph(
        "Maynord Calculator v1.0<br/>"
        "Developpe par Marc Zermatten<br/>"
        "2025 GeoMind",
        styles['Subtitle']
    ))

    # Build PDF
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"PDF genere : {output_path}")
    return output_path


if __name__ == "__main__":
    generate_manual()
