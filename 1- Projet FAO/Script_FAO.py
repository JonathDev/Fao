# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 11:40:40 2023

@author: Laurence Berville 
"""

import pandas as pd
import numpy as np
import squarify    # pip install squarify (algorithm for treemap)
import matplotlib.pyplot as plt
import seaborn as sb

# ---------------------------------------------------------------------------
popu = pd.read_csv("FAOSTAT_2013_population.csv",
                dtype={'Valeur':np.float64, 'Année': np.float64},
                converters={"Code Pays": str,"Code Année": str, "Code Élément": str, "Code Produit": str},
                 decimal='.')

dispoA = pd.read_csv("FAOSTAT_2013_animal.csv",
                dtype={'Valeur':np.float64, 'Année': np.float64},
                converters={"Code Pays": str,"Code Année": str, "Code Élément": str, "Code Produit": str},
                 decimal='.')

dispoC= pd.read_csv("FAOSTAT_2013_cereal.csv",
                dtype={'Valeur':np.float64},
                converters={"Code Pays": str,"Code Année": str, "Code Élément": str, "Code Produit": str },
                 decimal='.')

dispoV= pd.read_csv("FAOSTAT_2013_vegetal.csv",
                dtype={'Valeur':np.float64},
                converters={"Code Pays": str,"Code Année": str, "Code Élément": str, "Code Produit": str },
                 decimal='.')

# Le fichier d’insécurité alimentaire inclut : le pays, un facteur intervalle d’années, 
# le nombre de personnes en sous-alimentation en millions d’habitants et une colonne moyenne des années
# (ex. : pour l’intervalle 2012-2014, on peut le résumer en 2013).
dispo_ssAli= pd.read_csv("FAOSTAT_2013_sous_alimentation.csv",
                dtype={'Valeur':np.float64},
                 decimal='.')
# Nous avons donc les données de sous-nutritions pour 107 sur les 237 pays du monde. 
# ATTENTION les valeurs <0.1, sont notees ici 0.1
#-----------------------------------------------------------------------------
ListePays_A=set(dispoA["Pays"].values.tolist())
print(len(ListePays_A))

ListePays_V=set(dispoV["Pays"].values.tolist())
print(len(ListePays_V))

ListePays_C=set(dispoC["Pays"].values.tolist())
print(len(ListePays_C))

ListePays_popu=set(popu["Zone"].values.tolist())
print(len(ListePays_popu))

ListePays_ss_popu=set(dispo_ssAli["Zone"].values.tolist())
print(len(ListePays_ss_popu)) # Attention il y a 204 pays dans la table "vegetal"

if set(ListePays_A) == set(ListePays_V) == set(ListePays_C):
    print("Les listes des pays sont les mêmes dans Cereal / Animal et Vegetal")
else:
    print("Lists are not equal")
    
if set(ListePays_ss_popu) ==  set(ListePays_popu):
      print("Les listes des pays sont les mêmes")
else:
      print("Non, voici les pays absents : ")

difference_1 = set(ListePays_ss_popu).difference(set(ListePays_popu)) # 5
difference_2 = set(ListePays_popu).difference(set(ListePays_ss_popu)) # 36

list_difference = difference_1.union(difference_2)
print(list_difference) # pays different entre les tables population et sous alimentation


#-----------------------------------------------------------------------------
# Statistiques descriptives des 5 tables :
summary_across_rows = pd.DataFrame(popu).describe() # across axis=0
print(summary_across_rows )

summary_across_rows = pd.DataFrame(dispoA).describe() # across axis=0
print(summary_across_rows )

summary_across_rows = pd.DataFrame(dispoC).describe() # across axis=0
print(summary_across_rows )

summary_across_rows = pd.DataFrame(dispoV).describe() # across axis=0
print(summary_across_rows )

summary_across_rows = pd.DataFrame(dispo_ssAli).describe() # across axis=0
print(summary_across_rows )

#-----------------------------------------------------------------------------
# Question 1 : 

Total = popu["Valeur"].sum()
print("Population mondial :", int(Total*1000))
# Nous notons la prensence de trop d'habitants
# Erreur avec la Chine

Chine = popu.query("Zone=='Chine'")["Valeur"]
print(type(Chine))
Chine = list(Chine)
y = Chine[0]
print("On enlève donc la chine  = ", y*1000, "habitants")
TotalssChine = Total - y
print("Population mondial :", int(TotalssChine*1000) )

# ----------------------------------------------------------------------------
# Question 2 : 
    # Redondance : 
# Il y a des colonnes qui donnent la même information. Voici un exemple avec le Blé et la France : 
    # création de sous tableau
FranceV=dispoV[dispoV['Pays']=='France']# Sous tableau avec que la France 
FranceBle=FranceV[FranceV['Produit']=='Blé']# Sous tableau avec que le blé de France

# J'enlève les colonnes non utiles
FranceBle= FranceBle.drop(columns=["Code Domaine", "Description du Symbole","Domaine", "Code Pays", "Pays","Année", "Code Produit", "Produit", "Code Année"])
print(FranceBle)

FrBle=FranceBle[FranceBle['Symbole']=='S']# Sous tableau avec que les données en tonnes
# J'ajoute une colonne avec la valeur en kg
FrBle['ValeurKg'] = FrBle['Valeur'] * 1000

# J'enlève Unité
FrBle= FrBle.drop(columns=["Unité"])

# plot it
squarify.plot(sizes=FrBle['ValeurKg'],
              label=FrBle['Élément'], 
              color = sb.color_palette("rocket", 
                                     len('ValeurKg')),
              #pad = 0.01,# blanc pour séparer les carrés
              ec = 'black', #E ligne noir autour des carrés
              text_kwargs = {'fontsize': 5, 'color': 'black'}, # taille de la legende et couleur
              alpha=.9)# transparance des couleurs
plt.axis('off')
#plt.savefig("High resoltion.png", dpi=300)
plt.show()

# La Disponibilite interieure est égale à (Importation - Exportation) + Production
# La Disponibilite interieure est utilisée en Nourriture + Perte + Semences + Traitement + Alimentation Animale + Autres Utilisations
# Variation de stock = [(Importation - Exportation) + Production] - [Nourriture + Perte + Semences + Traitement + Alimentation Animale ]

# Reorder it following the values:
ordered_df = FrBle.sort_values(by='ValeurKg') # trier les données en ordre decroissant
my_range=range(1,len(FrBle.index)+1)
# Horizontal version
plt.hlines(y=my_range, xmin=0, xmax=ordered_df['ValeurKg'], color='skyblue')
plt.plot(ordered_df['ValeurKg'], my_range, "D")
plt.yticks(my_range, ordered_df['Élément'])
plt.title('Disponibilité en blé, en France en 2013')# rajouter un titre
#plt.savefig("DisponibiliteBle_France_2013.png", dpi=500)
plt.show()

# Question 3 : Disponibilité alimentaire (calories, protéines)

# Population
 # enlever les cols inutiles
PopulationM= popu.drop(columns=["Code Domaine","Code zone (M49)","Domaine","Note", "Code Élément","Élément","Description du Symbole","Symbole", "Produit","Code Produit", "Année", "Code année"])
PopulationM ['habitant'] = PopulationM['Valeur'] * 1000
PopulationM= PopulationM.drop(columns=["Valeur","Unité"])# Sous tableau avec que les habitants
PopulationM=PopulationM.rename(columns={'Zone':'Pays'})
PopulationM.set_index("Pays", inplace=True)


    # Mettre les deux tables ensemble
dispo = pd.concat([dispoA, dispoV])
   # enlever les cols inutiles
dispo= dispo.drop(columns=["Code Domaine","Domaine", "Élément","Description du Symbole","Symbole", "Code Pays", "Année", "Code Année"])
    # Passage de Pays en index
dispo.set_index("Pays", inplace=True)
    # On enlève la Chine : 
dispo_ss_chine = dispo.drop('Chine')


#Calculez (pour chaque pays et chaque produit) la disponibilité alimentaire en kcal puis en kg de protéines. 
kcal =dispo_ss_chine[dispo_ss_chine['Code Élément'] == '664'] # sous tableau avec que les kcalorie
# J'ajoute une colonne avec la valeur en année
kcal['	Kcal/personne/an'] = kcal['Valeur'] * 365

gr_Proteine =dispo_ss_chine[dispo_ss_chine['Code Élément'] == '674']# sous tableau avec que les proteines
# J'ajoute une colonne avec la valeur en année
gr_Proteine ['g/personne/an'] = gr_Proteine ['Valeur'] * 365
gr_Proteine ['kg/personne/an'] = gr_Proteine ['g/personne/an'] *0.001 # passage en kg


# Fusion des tables Proteine et Population
ProteinePays = pd.merge(gr_Proteine, PopulationM, on=["Pays"])
kcalPays = pd.merge(kcal, PopulationM, on=["Pays"])


# Vous ferez cela à partir de ces informations : 
# Population de chaque pays
# Disponibilité alimentaire donnée pour chaque produit et pour chaque pays en kcal/personne/jour, - - 
# Disponibilité alimentaire en protéines donnée pour chaque produit et pour chaque pays en g/personne/jour.




