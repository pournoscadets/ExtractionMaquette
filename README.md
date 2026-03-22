# ExtractionMaquette

* Il faut clôner le projet [link](https://github.com/pournoscadets/ExtractionMaquette) 
  
* Il faut installer le logiciel minerU afin de pouvoir extraire la data des fichiers pdfs.<br/>
  
* Une fois la data extraite, il faut extraire les data brutes en respectant le format déjà établie(exemple: 
[path](Extraction_finale/SFA/RawData/L1/L1_MI.toml)) au moyen d'un prompt(si tu as un prompt parfait tu pourras le partager directement dans le repo). <br/><br/>
NB: Pour ne pas dépasser la limite des contextes des IA <br/>

* il faut néttoyer les données précédemment extraites pour avoir les données du même format que ([path](Extraction_finale/SFA/Clean_data/L1/L1_MI.toml))

* Il faut formater les données pour l'appel api au serveur back, il faudra utiliser le prompt([path](Extraction_finale/SFA/Clean_data/prompt.md)) comme contexte de l'agent. <br/>

* Il faut par la suite donner à l'IA le fichier que nous voulons formater(ex:[path](Extraction_finale/SFA/Clean_data/prompt.md)) <br/>
  
* Il faut par la suite formatter les sorties de sorte à ce que ça soit sous le même format que(ex:[path](Extraction_finale/SFA/Clean_data/output.json))<br/><br/>
NB: il n'est pas obligatoire de communiquer à tout moment le gros json, il faut juste veiller à ce que l'université et la(les) filière(s) soit renseignée(s). Seuls les parcours et tous les composants qui leurs sont rattachés peuvent être omis si jamais nous les avons déjà sauvegarder en base de données(en outre on peut bien fonctionner avec la donnée delta).

* Il faut après récupérer ce json et faire l'appel à l'api suivante avec un token qui possède le rôle ADMIN. Pour ce fait, si ce n'est pas le cas il faut télécharger Bruno([link](https://www.usebruno.com)) et clôner le repo suivant [link](https://github.com/pournoscadets/BrunoExamemo). Importer le repository clôné dans Bruno afin d'avoir toutes les APIs du serveur. 

