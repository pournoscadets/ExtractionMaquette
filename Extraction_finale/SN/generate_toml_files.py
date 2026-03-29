#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer automatiquement les fichiers TOML à partir du fichier Excel "Maquette complet UFR SN.xlsx"
Les fichiers sont organisés dans les répertoires L1, L2, L3, M1, M2 selon le niveau et le diplôme.
"""

import pandas as pd
import os
import re
from pathlib import Path

def create_directories():
    """Crée les répertoires nécessaires s'ils n'existent pas"""
    directories = ['L1', 'L2', 'L3', 'M1', 'M2']
    base_path = Path('.')
    
    for dir_name in directories:
        dir_path = base_path / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"Répertoire {dir_path} créé ou vérifié")

def extract_program_info(df, start_line):
    """Extrait les informations du programme (domaine, parcours, grade, etc.)"""
    info = {
        'domaine': '',
        'parcours': '',
        'grade': '',
        'specialite': ''
    }
    
    for i in range(start_line, min(start_line + 10, len(df))):
        row = df.iloc[i]
        if pd.notna(row.iloc[0]):
            text = str(row.iloc[0]).strip()
            if 'DOMAINE' in text:
                info['domaine'] = text.split(':')[1].strip() if ':' in text else ''
            elif 'MENTION' in text:
                info['parcours'] = text.split(':')[1].strip() if ':' in text else ''
            elif 'SPECIALITE' in text:
                info['specialite'] = text.split(':')[1].strip() if ':' in text else ''
            elif 'GRADE' in text:
                info['grade'] = text.split(':')[1].strip() if ':' in text else ''
    
    return info

def extract_ue_data(df, start_line, end_line):
    """Extrait les données des UE et ECUE pour une plage de lignes"""
    ue_data = []
    current_ue = None
    current_ue_type = None
    
    for i in range(start_line, min(end_line, len(df))):
        row = df.iloc[i]
        
        if pd.notna(row.iloc[0]):
            text = str(row.iloc[0]).strip()
            
            # Détection des types d'UE
            if 'UE FONDAMENTALE' in text:
                current_ue_type = 'ue_fondamentale'
                continue
            elif 'UE DE SPECIALITE' in text or 'UE DE SPÉCIALITÉ' in text:
                current_ue_type = 'ue_specialite'
                continue
            elif 'UE DE METHODOLOGIE' in text or 'UE DE MÉTHODOLOGIE' in text:
                current_ue_type = 'ue_methodologie'
                continue
            elif 'UE DE CULTURE GENERALE' in text or 'UE DE CULTURE GÉNÉRALE' in text:
                current_ue_type = 'ue_culture_generale'
                continue
            elif 'UE STAGE' in text:
                current_ue_type = 'ue_stage'
                continue
            elif 'Total' in text or 'TOTAL' in text:
                break
            
            # Extraction des UE
            if len(text) >= 4 and text[0].isalpha() and text[1:].isdigit():
                # C'est un code UE
                ue_code = text
                ue_title = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ''
                
                current_ue = {
                    'code': ue_code,
                    'title': ue_title,
                    'type': current_ue_type,
                    'ecue': []
                }
                ue_data.append(current_ue)
                
                # Vérifier s'il y a un ECUE sur la même ligne
                if pd.notna(row.iloc[2]):
                    ecue_code = str(row.iloc[2]).strip()
                    ecue_title = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ''
                    if ecue_code and ecue_title:
                        current_ue['ecue'].append({
                            'code': ecue_code,
                            'title': ecue_title
                        })
            elif current_ue and pd.notna(row.iloc[2)):
                # C'est un ECUE
                ecue_code = str(row.iloc[2]).strip()
                ecue_title = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ''
                if ecue_code and ecue_title:
                    current_ue['ecue'].append({
                        'code': ecue_code,
                        'title': ecue_title
                    })
    
    return ue_data

def generate_toml_content(program_info, niveau, semestre_data):
    """Génère le contenu TOML pour un programme"""
    content = []
    
    # En-tête
    content.append(f"# Domaine: {program_info['domaine']}")
    content.append(f"# Parcours: {program_info['parcours']}")
    content.append(f"# Grade: {program_info['grade']}")
    content.append(f"# Niveau: {niveau}")
    content.append(f"# Semestre: {semestre_data['number']}")
    content.append("")
    
    # Métadonnées
    content.append(f"[semestre_{semestre_data['number']}.metadata]")
    content.append(f"domaine = \"{program_info['domaine']}\"")
    content.append(f"parcours = \"{program_info['parcours']}\"")
    content.append(f"grade = \"{program_info['grade']}\"")
    content.append(f"niveau = \"{niveau}\"")
    content.append(f"semestre = {semestre_data['number']}")
    content.append("")
    
    # UE
    for ue in semestre_data['ue_list']:
        content.append(f"[[semestre_{semestre_data['number']}.{ue['type']}]]")
        content.append(f"code_ue = \"{ue['code']}\"")
        content.append(f"intitule_ue = \"{ue['title']}\"")
        content.append("")
        
        for ecue in ue['ecue']:
            content.append(f"  [[semestre_{semestre_data['number']}.{ue['type']}.ecue]]")
            content.append(f"  code_ecue = \"{ecue['code']}\"")
            content.append(f"  intitule_ecue = \"{ecue['title']}\"")
            content.append("")
    
    return "\n".join(content)

def determine_level_and_speciality(filename):
    """Détermine le niveau et la spécialité à partir du nom de fichier"""
    match = re.match(r'^([LM])([123])_(.+)\.toml$', filename)
    if match:
        return match.group(1), match.group(2), match.group(3)
    return None, None, None

def find_program_ranges(df):
    """Trouve les plages de lignes pour chaque programme dans le fichier Excel"""
    ranges = []
    
    # Plages connues basées sur les données précédentes
    known_ranges = {
        'L1_PVA': (1, 50),
        'L2_PVA': (51, 120),
        'L3_PVE': (121, 176),
        'L3_PA': (178, 236),
        'L3_BP': (237, 292),
        'M1_PV': (298, 353),
        'M2_PV': (361, 396),
        'M1_BioGDE': (423, 477),
        'M2_BioGDE': (480, 509),
        'M1_PVE': (534, 579),
        'M2_PVE': (587, 622),
        'M1_PA': (648, 701),
        'M2_PA': (706, 741),
        'M1_AVI': (767, 788),
        'M2_AVI': (792, 827),
        'M1_GAB': (852, 908),
        'M2_GV': (911, 933),
        'M2_GA': (937, 960),
        'M1_BP': (992, 1040),
        'M2_BP': (1049, 1074),
        'M2_BS': (1075, 1099)
    }
    
    return known_ranges

def main():
    """Fonction principale"""
    print("Génération des fichiers TOML à partir du fichier Excel...")
    
    # Créer les répertoires
    create_directories()
    
    # Charger le fichier Excel
    excel_file = "Maquette complet UFR SN.xlsx"
    try:
        df = pd.read_excel(excel_file, header=None)
        print(f"Fichier Excel {excel_file} chargé avec succès")
    except Exception as e:
        print(f"Erreur lors du chargement du fichier Excel: {e}")
        return
    
    # Obtenir les plages de programmes
    program_ranges = find_program_ranges(df)
    
    # Générer les fichiers pour chaque programme
    for program_name, (start_line, end_line) in program_ranges.items():
        print(f"\nTraitement du programme: {program_name} (lignes {start_line}-{end_line})")
        
        # Déterminer le niveau et la spécialité
        niveau, semestre_num, speciality = determine_level_and_speciality(program_name + ".toml")
        
        if not niveau:
            print(f"  Format de nom de programme non reconnu: {program_name}")
            continue
        
        # Extraire les informations du programme
        program_info = extract_program_info(df, start_line)
        
        # Créer le répertoire si nécessaire
        dir_path = Path(niveau)
        dir_path.mkdir(exist_ok=True)
        
        # Traiter les semestres
        semestre_files = []
        
        # Pour les programmes avec deux semestres
        if 'M1' in program_name or 'M2' in program_name or 'L2' in program_name or 'L3' in program_name:
            # Semestre 1 (ou 3 pour L3)
            semestre1_num = 3 if niveau == 'L3' else 1
            semestre1_end = start_line + 50  # Approximation
            
            # Trouver la fin du semestre 1
            for i in range(start_line, min(end_line, len(df))):
                row = df.iloc[i]
                if pd.notna(row.iloc[0]):
                    text = str(row.iloc[0]).strip()
                    if 'semestre 2' in text.lower() or 'Semestre 2' in text:
                        semestre1_end = i
                        break
            
            # Extraire les données du semestre 1
            ue_data1 = extract_ue_data(df, start_line, semestre1_end)
            
            if ue_data1:
                semestre1_data = {
                    'number': semestre1_num,
                    'ue_list': ue_data1
                }
                
                # Générer le contenu TOML
                toml_content1 = generate_toml_content(program_info, niveau, semestre1_data)
                
                # Écrire le fichier
                filename1 = f"{niveau}{semestre1_num}_{speciality}.toml"
                filepath1 = dir_path / filename1
                
                with open(filepath1, 'w', encoding='utf-8') as f:
                    f.write(toml_content1)
                
                print(f"  Fichier créé: {filepath1}")
                semestre_files.append(filename1)
            
            # Semestre 2 (ou 4 pour L3)
            semestre2_num = 4 if niveau == 'L3' else 2
            semestre2_start = semestre1_end + 1
            
            # Extraire les données du semestre 2
            ue_data2 = extract_ue_data(df, semestre2_start, end_line)
            
            if ue_data2:
                semestre2_data = {
                    'number': semestre2_num,
                    'ue_list': ue_data2
                }
                
                # Générer le contenu TOML
                toml_content2 = generate_toml_content(program_info, niveau, semestre2_data)
                
                # Écrire le fichier
                filename2 = f"{niveau}{semestre2_num}_{speciality}.toml"
                filepath2 = dir_path / filename2
                
                with open(filepath2, 'w', encoding='utf-8') as f:
                    f.write(toml_content2)
                
                print(f"  Fichier créé: {filepath2}")
                semestre_files.append(filename2)
        
        else:
            # Pour L1 (semestres 1 et 2)
            # Semestre 1
            semestre1_end = start_line + 50
            for i in range(start_line, min(end_line, len(df))):
                row = df.iloc[i]
                if pd.notna(row.iloc[0]):
                    text = str(row.iloc[0]).strip()
                    if 'semestre 2' in text.lower() or 'Semestre 2' in text:
                        semestre1_end = i
                        break
            
            ue_data1 = extract_ue_data(df, start_line, semestre1_end)
            
            if ue_data1:
                semestre1_data = {
                    'number': 1,
                    'ue_list': ue_data1
                }
                
                toml_content1 = generate_toml_content(program_info, niveau, semestre1_data)
                
                filename1 = f"{niveau}1_{speciality}.toml"
                filepath1 = dir_path / filename1
                
                with open(filepath1, 'w', encoding='utf-8') as f:
                    f.write(toml_content1)
                
                print(f"  Fichier créé: {filepath1}")
                semestre_files.append(filename1)
            
            # Semestre 2
            semestre2_start = semestre1_end + 1
            ue_data2 = extract_ue_data(df, semestre2_start, end_line)
            
            if ue_data2:
                semestre2_data = {
                    'number': 2,
                    'ue_list': ue_data2
                }
                
                toml_content2 = generate_toml_content(program_info, niveau, semestre2_data)
                
                filename2 = f"{niveau}2_{speciality}.toml"
                filepath2 = dir_path / filename2
                
                with open(filepath2, 'w', encoding='utf-8') as f:
                    f.write(toml_content2)
                
                print(f"  Fichier créé: {filepath2}")
                semestre_files.append(filename2)
    
    print("\nGénération terminée!")

if __name__ == "__main__":
    main()
