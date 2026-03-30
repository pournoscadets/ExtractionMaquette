#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer le fichier sn_draft_model.json à partir de sn.toml
Structure basée sur le modèle draft.json
"""

import json
import re
import os
from pathlib import Path

def deduce_discipline_from_ue(ue_title):
    """Déduit la discipline en fonction du titre de l'UE"""
    
    discipline_mapping = {
        # Sciences Vétérinaires
        "immunologie": "Sciences Vétérinaires", "cynégétique": "Sciences Vétérinaires", 
        "hygiène": "Sciences Vétérinaires", "nutrition": "Sciences Vétérinaires",
        "pathologie": "Sciences Vétérinaires", "pharmacologie": "Sciences Vétérinaires",
        "toxicologie": "Sciences Vétérinaires", "maladie": "Sciences Vétérinaires",
        
        # Zootechnie
        "reproduction": "Zootechnie", "anatomie": "Zootechnie", "physiologie": "Zootechnie",
        "conduite": "Zootechnie", "infrastructure": "Zootechnie", "équipement": "Zootechnie",
        "technique": "Zootechnie", "élevage": "Zootechnie", "volaille": "Zootechnie",
        
        # Sciences de l'Environnement
        "écologie": "Sciences de l'Environnement", "environnement": "Sciences de l'Environnement",
        "biodiversité": "Sciences de l'Environnement", "écosystème": "Sciences de l'Environnement",
        "télédétection": "Sciences de l'Environnement", "impact": "Sciences de l'Environnement",
        "écotoxicologie": "Sciences de l'Environnement", "climat": "Sciences de l'Environnement",
        
        # Biologie
        "biologie": "Biologie", "cellulaire": "Biologie", "moléculaire": "Biologie",
        "génétique": "Biologie", "microbiologie": "Biologie", "végétale": "Biologie",
        "animale": "Biologie", "botanique": "Biologie", "zoologie": "Biologie",
        "systématique": "Biologie", "ethnobotanique": "Biologie",
        
        # Chimie
        "chimie": "Chimie", "biochimie": "Chimie", "phytochimie": "Chimie",
        "molécule": "Chimie", "pesticide": "Chimie", "liaison": "Chimie",
        "organique": "Chimie", "médicament": "Chimie",
        
        # Mathématiques
        "mathématique": "Mathématiques", "probabilité": "Mathématiques",
        "statistique": "Mathématiques", "algèbre": "Mathématiques", "analyse": "Mathématiques",
        "traitement": "Mathématiques", "collecte": "Mathématiques",
        
        # Physiques
        "mécanique": "Physiques", "physique": "Physiques", "optique": "Physiques",
        "électricité": "Physiques", "thermodynamique": "Physiques", "quantique": "Physiques",
        "électrostatique": "Physiques",
        
        # Informatique
        "informatique": "Informatique", "bioinformatique": "Informatique",
        
        # Géologie/Sciences de la Terre
        "géologie": "Sciences de la Terre", "pédologie": "Sciences de la Terre",
        "hydrologie": "Sciences de la Terre", "sol": "Sciences de la Terre",
        "structurale": "Sciences de la Terre",
        
        # Agronomie/Agriculture
        "agronomie": "Agronomie", "agricole": "Agriculture", "culture": "Agriculture",
        "production": "Agriculture", "fertilisation": "Agronomie", "irrigation": "Agronomie",
        "itinéraire": "Agriculture", "fertilité": "Agronomie",
        
        # Sciences Forestières
        "forest": "Sciences Forestières", "foresterie": "Sciences Forestières",
        "aménagement": "Sciences Forestières",
        
        # Sciences Halieutiques
        "aquatique": "Sciences Halieutiques", "halieutique": "Sciences Halieutiques",
        
        # Sciences Pharmaceutiques
        "pharmacognosie": "Sciences Pharmaceutiques", "formulation": "Sciences Pharmaceutiques",
        "médicament": "Sciences Pharmaceutiques", "traditionnel": "Sciences Pharmaceutiques",
        
        # Droit
        "droit": "Droit", "juridique": "Droit", "législation": "Droit", "norme": "Droit",
        "convention": "Droit", "foncier": "Droit",
        
        # Langues
        "anglais": "Langues", "langue": "Langues", "communication": "Langues",
        "expression": "Langues", "technique": "Langues", "composition": "Langues",
        
        # Recherche
        "recherche": "Recherche", "stage": "Recherche", "mémoire": "Recherche",
        "séminaire": "Recherche", "rédaction": "Recherche", "projet": "Recherche",
        "immersion": "Recherche", "documentaire": "Recherche",
        
        # Economie/Gestion
        "économie": "Economie", "gestion": "Gestion", "finance": "Economie",
        "marketing": "Economie", "agri-business": "Economie", "entrepreneuriat": "Economie",
        "insertion": "Economie", "professionnel": "Economie", "évaluation": "Gestion",
        "conception": "Gestion", "suivi": "Gestion"
    }
    
    ue_title_lower = ue_title.lower()
    
    for keyword, discipline in discipline_mapping.items():
        if keyword in ue_title_lower:
            return discipline
    
    return "Recherche"

def get_discipline_abbreviation(discipline):
    """Retourne l'abréviation de la discipline"""
    discipline_abbreviations = {
        "Sciences Vétérinaires": "SC_VET", "Zootechnie": "ZOOT",
        "Sciences de l'Environnement": "ENV", "Biologie": "BIO", "Chimie": "CHIM",
        "Mathématiques": "MATHS", "Physiques": "PHYS", "Informatique": "INFO",
        "Sciences de la Terre": "ST", "Agronomie": "AGRO", "Agriculture": "AGRI",
        "Sciences Forestières": "SC_FOR", "Sciences Halieutiques": "SC_HAL",
        "Sciences Pharmaceutiques": "SC_PHAR", "Droit": "DRT", "Langues": "LANG",
        "Recherche": "RECH", "Economie": "ECO", "Gestion": "GEST"
    }
    
    return discipline_abbreviations.get(discipline, "RECH")

def clean_string(text):
    """Nettoie les chaînes de caractères"""
    if not text:
        return ""
    text = re.sub(r'\s*-\s*', '-', text)
    return text.strip()

def generate_sn_draft_model(toml_file_path, output_file_path):
    """Génère le fichier sn_draft_model.json à partir du fichier TOML"""
    
    # Lire le fichier TOML
    with open(toml_file_path, 'r', encoding='utf-8') as f:
        toml_content = f.read()
    
    # Structure JSON selon le modèle draft.json
    output_json = {
        "label": "Université Nangui Abrogoua",
        "abbreviation": "UNA",
        "ufrs": [
            {
                "label": "Sciences Naturelles",
                "abbreviation": "SN",
                "parcours": []
            }
        ]
    }
    
    ufr = output_json["ufrs"][0]
    
    # Parser le contenu TOML
    current_parcours = None
    current_level = None
    current_discipline = None
    current_ue = None
    ecue_counter = 1
    
    lines = toml_content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line or line.startswith('===') or line.startswith('# Fichier'):
            continue
        
        # Extraire les métadonnées des sections
        if line.startswith('# Niveau:'):
            level = line.split(':')[1].strip()
            current_level = level
            ecue_counter = 1
        
        elif line.startswith('# Parcours:'):
            if current_level:
                parcours_name = clean_string(line.split(':')[1].strip())
                
                parcours_abbreviations = {
                    "PRODUCTIONS VEGETALES /PRODUCTIONS ANIMALES": "PVA",
                    "BOTANIQUE ET PHYTOTHERAPIE": "BP", "PRODUCTIONS ANIMALES": "PA",
                    "PROTECTION DES VEGETAUX ET DE L'ENVIRONNEMENT": "PVE", "AVICULTURE": "AVI",
                    "BIODIVERSITE ET GESTION DURABLE DES ECOSYSTEMES": "BioGDE",
                    "BIOLOGIE ET SANTE": "BS", "GENETIQUE ET AMELIORATION DES Bioressources": "GAB",
                    "PRODUCTIONS VEGETALES": "PV", "GENETIQUE ANIMALE": "GA", "GENETIQUE VEGETALE": "GV"
                }
                
                parcours_found = None
                for parcours in ufr["parcours"]:
                    if parcours["label"] == parcours_name:
                        parcours_found = parcours
                        break
                
                if not parcours_found:
                    new_parcours = {
                        "label": parcours_name,
                        "abbreviation": parcours_abbreviations.get(parcours_name, "UNK"),
                        "levels": []
                    }
                    ufr["parcours"].append(new_parcours)
                    current_parcours = new_parcours
                else:
                    current_parcours = parcours_found
        
        elif line.startswith('# Semestre:'):
            if current_parcours:
                semestre_num = line.split(':')[1].strip()
                level_label = current_level
                
                level_found = None
                for level in current_parcours["levels"]:
                    if level["label"] == level_label:
                        level_found = level
                        break
                
                if not level_found:
                    new_level = {
                        "label": level_label,
                        "disciplines": []
                    }
                    current_parcours["levels"].append(new_level)
                    current_level = new_level
                else:
                    current_level = level_found
        
        # Extraire les UE
        elif line.startswith('[[semestre_'):
            ue_match = re.match(r'\[\[semestre_\d+\.(.+?)\]\]', line)
            if ue_match:
                ue_type = ue_match.group(1)
                ecue_counter = 1
        
        elif line.startswith('code_ue ='):
            ue_code = line.split('=')[1].strip().strip('"')
        
        elif line.startswith('intitule_ue ='):
            ue_title = clean_string(line.split('=')[1].strip().strip('"'))
            
            discipline = deduce_discipline_from_ue(ue_title)
            discipline_abbrev = get_discipline_abbreviation(discipline)
            
            current_ue = {
                "label": ue_title,
                "abbreviation": ue_code,
                "ecues": []
            }
            
            discipline_found = None
            for disc in current_level["disciplines"]:
                if disc["label"] == discipline:
                    discipline_found = disc
                    break
            
            if not discipline_found:
                new_discipline = {
                    "label": discipline,
                    "abbreviation": discipline_abbrev,
                    "ues": []
                }
                current_level["disciplines"].append(new_discipline)
                current_discipline = new_discipline
            else:
                current_discipline = discipline_found
            
            current_discipline["ues"].append(current_ue)
            ecue_counter = 1
        
        elif line.startswith('code_ecue ='):
            ecue_code = line.split('=')[1].strip().strip('"')
        
        elif line.startswith('intitule_ecue ='):
            if current_ue:
                ecue_title = clean_string(line.split('=')[1].strip().strip('"'))
                
                ecue_type = f"ECUE{ecue_counter}"
                new_ecue = {
                    "label": ecue_title,
                    "type": ecue_type
                }
                current_ue["ecues"].append(new_ecue)
                ecue_counter += 1
                if ecue_counter > 3:
                    ecue_counter = 1
    
    return output_json

def main():
    """Fonction principale"""
    print("Génération du fichier sn_draft_model.json...")
    
    toml_file = "sn.toml"
    output_file = "sn_draft_model.json"
    
    if not os.path.exists(toml_file):
        print(f"Erreur: Le fichier {toml_file} n'existe pas!")
        return
    
    try:
        json_data = generate_sn_draft_model(toml_file, output_file)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Fichier généré: {output_file}")
        print(f"📊 Taille: {os.path.getsize(output_file):,} octets")
        
        # Résumé
        total_parcours = len(json_data["ufrs"][0]["parcours"])
        total_levels = sum(len(parcours["levels"]) for parcours in json_data["ufrs"][0]["parcours"])
        total_disciplines = sum(len(level["disciplines"]) for parcours in json_data["ufrs"][0]["parcours"] for level in parcours["levels"])
        total_ues = sum(len(discipline["ues"]) for parcours in json_data["ufrs"][0]["parcours"] for level in parcours["levels"] for discipline in level["disciplines"])
        total_ecues = sum(len(ue["ecues"]) for parcours in json_data["ufrs"][0]["parcours"] for level in parcours["levels"] for discipline in level["disciplines"] for ue in discipline["ues"])
        
        print(f"\n📈 Résumé:")
        print(f"   - UFR: 1 (Sciences Naturelles)")
        print(f"   - Parcours: {total_parcours}")
        print(f"   - Niveaux: {total_levels}")
        print(f"   - Disciplines: {total_disciplines}")
        print(f"   - UE: {total_ues}")
        print(f"   - ECUE: {total_ecues}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
