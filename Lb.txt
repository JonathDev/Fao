import pandas as pd
import numpy as np

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

# La Disponibilite interieure est égale à (Importation - Exportation) + Production
# La Disponibilite interieure est utilisée en Nourriture + Perte + Semences + Traitement + Alimentation Animale
# Variation de stock = [(Importation - Exportation) + Production] - [Nourriture + Perte + Semences + Traitement + Alimentation Animale ]

