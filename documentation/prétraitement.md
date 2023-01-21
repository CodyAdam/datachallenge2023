# En résumé

Nous vons fait les oppérations suivantes :
- Filtrages des colonnes inutiles `communes_bre.csv`
- Filtrages des temps de trajets trop longs (> 30 min) `temps_trajet.csv`
- Discretisation des données en coefficient de pondération (`niveau_interventions.csv`)

# Développement

L'objectif du fichier R est de réaliser un formatage des données afin d'enrichir notre algorithme génétique. Pour cela, nous avons décidé de créer deux nouvelles variables dans le fichier intervention. Ces deux variables cherchent à pondérer la variable intervention cliente et réseau de telles sortes que le poids alloué aux variables est plus fort si le nombre d'interventions y est fréquent.


- Très bas → 1,0
- Bas → 1,1
- Moyen → 1,2
- Haut → 1,3
- Très haut → 1,4


Nous avons choisi de faire cette pondération pour ne pas discriminer de manière trop importante les petites communes qui sont majoritaires en Bretagne (Environ 60 % des communes bretonnes font moins de 2000 habitants).


De plus, nous avons créé deux nouvelles variables (« df_clt » et « df_emp ») à test pour illustrer l'importance de la satisfaction client et du NPS qui peut améliorer notre modèle pour prendre à terme les critères RSE dans notre modèle d'algorithme génétique.


Enfin, nous nous sommes intéressés à la corrélation entre le nombre d'habitants des communes bretonnes et le nombre d'interventions. Effectuer sur le réseau et chez les particuliers et les entreprises. Pour cela, nous avons utilisé la base de données de l'INSEE avec le dernier recensement de 2019. Ces résultats nous ont montrés que l'activité d'Enedis se faisait de façon homogène sur tout le territoire breton hors villes de plus de 30 000 habitants.
