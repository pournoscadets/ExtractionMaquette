# Tâche principale

Ton objectif est de construire un json en te basant sur le format du **toml de base** et par la suite les données que je te fournirai. Ta sortie finale sera du json, même si tu ne traiteras que du toml( j'utilise le toml juste pour la structuration)

## Valeurs possibles (si jamais tu as du mal à identifier une valeur laisse là à vide et fais le moi savoir, mais à aucun moment tu ne devras considérer d'autres valeurs que celles ci-dessous)

### ufrs.parcours.levels: L1, L2, L3 , M1, M2, DOC

### ues.ecues.type; ECUE1, ECUE2, ECUE3

### **ufrs.parcours.levels.disciplines.labels:** Mathématiques, Physiques, Chimie, Informatique, Economie, Recherche, Droit, Pedologie, Biologie, Géologie, Sciences de l'Ingénieur, Sciences de la Terre, Sciences de la Vie, Sciences de l'Environnement, Sciences Sociales, Sciences Politiques, Gestion, Commerce, Marketing, Finance, Comptabilité, Médecine, Pharmacie, Odontologie, Sciences Pharmaceutiques, Sciences Médicales, Lettres, Langues, Philosophie, Histoire, Géographie, Sociologie, Psychologie, Sciences de l'Éducation, Arts, Musique, Architecture, Urbanisme, Génie Civil, Génie Électrique, Génie Mécanique, Génie Chimique, Génie Informatique, Télécommunications, Agriculture, Agronomie, Zootechnie, Sciences Vétérinaires, Sciences Halieutiques, Sciences Forestières

### **ufrs.parcours.levels.disciplines.abbreviation:** MATHS, PHYS, CHIM, INFO, ECO, RECH, DRT, PEDOL, BIO, GEOL, ING, ST, SV, ENV, SC_SOC, SC_POL, GEST, COM, MK, FIN, CPTA, MED, PHAR, ODONT, SC_PHAR, SC_MED, LETT, LANG, PHILO, HIST, GEOG, SOCIO, PSY, SC_EDUC, ARTS, MUS, ARCH, URB, GC, GE, GM, GCH, GI, TELECOM, AGRI, AGRO, ZOOT, SC_VET, SC_HAL, SC_FOR

En ce qui conerne les disciplines je voudrais que tu en **déduisent** en **fonction de l'ue traités**.

## Instructions

### Nettoyage

Quand tu rencontres les chaînes de caractères de ce type: **"MATHEMATIQUES - INFORMATIQUE"**, il faudrait le transformer de sorte à avoir **"MATHEMATIQUES-INFORMATIQUE"**.

### Quand tu rencontres ce genre de données

```toml
[[semestre_1.ue_connaissances_fondamentales]]
code_ue = "IAP2201"
intitule_ue = "Initiation à l'Algorithmique et Programmation"

  [[semestre_1.ue_connaissances_fondamentales.ecue]]
  code_ecue = "IAP22011"
  intitule_ecue = "Algorithmique"  

  [[semestre_1.ue_connaissances_fondamentales.ecue]]
  code_ecue = "IAP22012"
  intitule_ecue = "Programmation"  
  ```

il faudrait que tu considères l'Ecue(label: "Algorithmique", type :"ECUE1") et Ecue(label: "Programmation", type :"ECUE2"), autant qu'il y'a de données d'ecue autant qu'il y'a de tpe d'ecue mais rangé dans leur ordre d'apparution.

### Pour la structure suivante elle vaudra la valeur que je te fournirai ci-dessous

```toml
label = ""
abbreviation = ""
```

Valeur à considérer:

```toml
label = "Université Nangui Abrogoua"
abbreviation = "UNA" 
```

```toml
[[ufrs]]
label = ""
abbreviation = ""
```

Valeur à considérer:

```toml
[[ufrs]]
label = "Sciences Fondamentales et Appliquées"
abbreviation = "SFA"
```

## Exemple

### Structure du toml de base

```toml
label = ""
abbreviation = ""

[[ufrs]]
label = ""
abbreviation = ""

[[ufrs.parcours]]
label = ""
abbreviation = ""

[[ufrs.parcours.levels]]
label = ""

[[ufrs.parcours.levels.disciplines]]
label = ""
abbreviation = ""

[[ufrs.parcours.levels.disciplines.ues]]
label = ""
abbreviation = ""

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = ""
type = ""
```

### Données fournies

```toml
# Domaine: SCIENCES ET TECHNOLOGIE
# Parcours: MATHEMATIQUES - INFORMATIQUE
# Grade: LICENCE
# Niveau: L1
# Semestre: 1

[semestre_1.metadata]
domaine = "SCIENCES ET TECHNOLOGIE"
parcours = "MATHEMATIQUES - INFORMATIQUE"
grade = "LICENCE"
niveau = "L1"
semestre = 1

[[semestre_1.ue_connaissances_fondamentales]]
code_ue = "MAN2201"
intitule_ue = "Initiation à l'Analyse Mathématique et Bases"

  [[semestre_1.ue_connaissances_fondamentales.ecue]]
  code_ecue = "MAL22011"
  intitule_ecue = "Initiation à l'Analyse Mathématique"  

  [[semestre_1.ue_connaissances_fondamentales.ecue]]
  code_ecue = "MAL22012"
  intitule_ecue = "Analyse de base"  

[[semestre_1.ue_connaissances_fondamentales]]
code_ue = "IAP2201"
intitule_ue = "Initiation à l'Algorithmique et Programmation"

  [[semestre_1.ue_connaissances_fondamentales.ecue]]
  code_ecue = "IAP22011"
  intitule_ecue = "Algorithmique"  

  [[semestre_1.ue_connaissances_fondamentales.ecue]]
  code_ecue = "IAP22012"
  intitule_ecue = "Programmation"  

[[semestre_1.ue_connaissances_fondamentales]]
code_ue = "MAL2201"
intitule_ue = "Groupes et Algèbre Linéaire"

  [[semestre_1.ue_connaissances_fondamentales.ecue]]
  code_ecue = "MAL22011"
  intitule_ecue = "Groupes"  

  [[semestre_1.ue_connaissances_fondamentales.ecue]]
  code_ecue = "MAL22012"
  intitule_ecue = "Algèbre Linéaire"  

[[semestre_1.ue_connaissances_fondamentales]]
code_ue = "PME2201"
intitule_ue = "Mécanique du Point Matériel"

  [[semestre_1.ue_connaissances_fondamentales.ecue]]
  code_ecue = "PME22011"
  intitule_ecue = "Cinématique"

  [[semestre_1.ue_connaissances_fondamentales.ecue]]
  code_ecue = "PME22012"
  intitule_ecue = "Dynamique"  

[[semestre_1.ue_methodologie]]
code_ue = "LMR2201"
intitule_ue = "Logique et Méthode de Raisonnement en Mathématique"

  [[semestre_1.ue_methodologie.ecue]]
  code_ecue = "LMR2201"
  intitule_ecue = "Logique et Méthode de Raisonnement en Mathématique"

[[semestre_1.ue_culture_generale]]
code_ue = "ANG2201"
intitule_ue = "Anglais"

  [[semestre_1.ue_culture_generale.ecue]]
  code_ecue = "ANG2201"
  intitule_ecue = "Anglais"  

[[semestre_1.ue_culture_generale]]
code_ue = "RED2201"
intitule_ue = "Recherche Documentaire"

  [[semestre_1.ue_culture_generale.ecue]]
  code_ecue = "RED2201"
  intitule_ecue = "Recherche Documentaire"

# Domaine: SCIENCES ET TECHNOLOGIE
# Parcours: MATHEMATIQUES - INFORMATIQUE
# Grade: LICENCE
# Niveau: L1
# Semestre: 2

[semestre_2.metadata]
domaine = "SCIENCES ET TECHNOLOGIE"
parcours = "MATHEMATIQUES - INFORMATIQUE"
grade = "LICENCE"
niveau = "L1"
semestre = 2

[[semestre_2.ue_connaissances_fondamentales]]
code_ue = "ALG2202"
intitule_ue = "Algèbre 2"

  [[semestre_2.ue_connaissances_fondamentales.ecue]]
  code_ecue = "ALG22021"
  intitule_ecue = "Espace vectorielle et calcul vectoriel"  

  [[semestre_2.ue_connaissances_fondamentales.ecue]]
  code_ecue = "ALG22022"
  intitule_ecue = "Algèbre linéaire"

[[semestre_2.ue_connaissances_fondamentales]]
code_ue = "ANA2202"
intitule_ue = "Analyse 2"

  [[semestre_2.ue_connaissances_fondamentales.ecue]]
  code_ecue = "ANA22021"
  intitule_ecue = "Intégration et équation différentielle"

  [[semestre_2.ue_connaissances_fondamentales.ecue]]
  code_ecue = "ANA22022"
  intitule_ecue = "Fonction vectorielle d'une variable réelle"  

[[semestre_2.ue_connaissances_fondamentales]]
code_ue = "PEL2202"
intitule_ue = "Electrostatique - Electricité"

  [[semestre_2.ue_connaissances_fondamentales.ecue]]
  code_ecue = "PEL22021"
  intitule_ecue = "Electrostatique"  

  [[semestre_2.ue_connaissances_fondamentales.ecue]]
  code_ecue = "PEL22022"
  intitule_ecue = "Electricité"  

[[semestre_2.ue_specialite]]
code_ue = "GEO2202"
intitule_ue = "Géométrie 1"

  [[semestre_2.ue_specialite.ecue]]
  code_ecue = "GEO22021"
  intitule_ecue = "Éléments de base de la Géométrie"  

  [[semestre_2.ue_specialite.ecue]]
  code_ecue = "GEO22022"
  intitule_ecue = "Théories - Espaces affine et euclidien"  

[[semestre_2.ue_specialite]]
code_ue = "STD2202"
intitule_ue = "Statistiques descriptives"

  [[semestre_2.ue_specialite.ecue]]
  code_ecue = "STD22021"
  intitule_ecue = "Statistique descriptive univariée"

  [[semestre_2.ue_specialite.ecue]]
  code_ecue = "STD22022"
  intitule_ecue = "Statistique descriptive bivariée"  

[[semestre_2.ue_methodologie]]
code_ue = "ARO2202"
intitule_ue = "Architecture des Ordinateurs"

  [[semestre_2.ue_methodologie.ecue]]
  code_ecue = "ARO2202"
  intitule_ecue = "Architecture des Ordinateurs"

[[semestre_2.ue_culture_generale]]
code_ue = "MIC2202"
intitule_ue = "Microeconomie"

  [[semestre_2.ue_culture_generale.ecue]]
  code_ecue = "MIC2202"
  intitule_ecue = "Microeconomie"  
  ```

### Equivalent toml du json du  résultat final

```toml
label = "Université Nangui Abrogoua"
abbreviation = "UNA"

[[ufrs]]
label = "Sciences Fondamentales et Appliquées"
abbreviation = "SFA"

[[ufrs.parcours]]
label = "MATHEMATIQUES-INFORMATIQUE"
abbreviation = "MI"

[[ufrs.parcours.levels]]
label = "L1"

[[ufrs.parcours.levels.disciplines]]
label = "Mathématiques"
abbreviation = "MATHS"

[[ufrs.parcours.levels.disciplines.ues]]
label = "Initiation à l'Analyse Mathématique et Bases"
abbreviation = "MAN2201"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Initiation à l'Analyse Mathématique"
type = "ECUE1"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Analyse de base"
type = "ECUE2"

[[ufrs.parcours.levels.disciplines.ues]]
label = "Groupes et Algèbre Linéaire"
abbreviation = "MAL2201"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Groupes"
type = "ECUE1"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Algèbre Linéaire"
type = "ECUE2"

[[ufrs.parcours.levels.disciplines.ues]]
label = "Algèbre 2"
abbreviation = "ALG2202"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Espace vectorielle et calcul vectoriel"
type = "ECUE1"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Algèbre linéaire"
type = "ECUE2"

[[ufrs.parcours.levels.disciplines.ues]]
label = "Analyse 2"
abbreviation = "ANA2202"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Intégration et équation différentielle"
type = "ECUE1"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Fonction vectorielle d'une variable réelle"
type = "ECUE2"

[[ufrs.parcours.levels.disciplines.ues]]
label = "Géométrie 1"
abbreviation = "GEO2202"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Éléments de base de la Géométrie"
type = "ECUE1"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Théories - Espaces affine et euclidien"
type = "ECUE2"

[[ufrs.parcours.levels.disciplines.ues]]
label = "Statistiques descriptives"
abbreviation = "STD2202"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Statistique descriptive univariée"
type = "ECUE1"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Statistique descriptive bivariée"
type = "ECUE2"

[[ufrs.parcours.levels.disciplines.ues]]
label = "Logique et Méthode de Raisonnement en Mathématique"
abbreviation = "LMR2201"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Logique et Méthode de Raisonnement en Mathématique"
type = "ECUE1"

[[ufrs.parcours.levels.disciplines]]
label = "Informatique"
abbreviation = "INFO"

[[ufrs.parcours.levels.disciplines.ues]]
label = "Initiation à l'Algorithmique et Programmation"
abbreviation = "IAP2201"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Algorithmique"
type = "ECUE1"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Programmation"
type = "ECUE2"

[[ufrs.parcours.levels.disciplines.ues]]
label = "Architecture des Ordinateurs"
abbreviation = "ARO2202"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Architecture des Ordinateurs"
type = "ECUE1"

[[ufrs.parcours.levels.disciplines]]
label = "Physiques"
abbreviation = "PHYS"

[[ufrs.parcours.levels.disciplines.ues]]
label = "Mécanique du Point Matériel"
abbreviation = "PME2201"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Cinématique"
type = "ECUE1"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Dynamique"
type = "ECUE2"

[[ufrs.parcours.levels.disciplines.ues]]
label = "Electrostatique - Electricité"
abbreviation = "PEL2202"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Electrostatique"
type = "ECUE1"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Electricité"
type = "ECUE2"

[[ufrs.parcours.levels.disciplines]]
label = "Langues"
abbreviation = "LANG"

[[ufrs.parcours.levels.disciplines.ues]]
label = "Anglais"
abbreviation = "ANG2201"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Anglais"
type = "ECUE1"

[[ufrs.parcours.levels.disciplines]]
label = "Recherche"
abbreviation = "RECH"

[[ufrs.parcours.levels.disciplines.ues]]
label = "Recherche Documentaire"
abbreviation = "RED2201"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Recherche Documentaire"
type = "ECUE1"

[[ufrs.parcours.levels.disciplines]]
label = "Economie"
abbreviation = "ECO"

[[ufrs.parcours.levels.disciplines.ues]]
label = "Microeconomie"
abbreviation = "MIC2202"

[[ufrs.parcours.levels.disciplines.ues.ecues]]
label = "Microeconomie"
type = "ECUE1"
```