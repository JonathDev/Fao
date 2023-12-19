import pandas as pd
import numpy as np
import csv


#%%

popu = pd.read_csv("C:/Users/kaeli/Documents/python/FAOSTAT_data_fr_12-18-2023.csv",
                dtype={'Valeur':np.float64},
                index_col='Code zone (M49)',
                 decimal='.')

popu1=popu.head(5)
print(popu1)

#%%

dispoAnimal = pd.read_csv("C:/Users/kaeli/Documents/python/FAOSTAT_2013_animal.csv",
                dtype={'Valeur':np.float64},
                 decimal='.')

ListePays_A=set(dispoAnimal["Pays"].values.tolist())
print(len(ListePays_A))


dispoCereal = pd.read_csv("C:/Users/kaeli/Documents/python/FAOSTAT_2013_cereal.csv",
                dtype={'Valeur':np.float64},
                 decimal='.')

#%%

ListePays_C=set(dispoCereal["Pays"].values.tolist())
print(len(ListePays_C))

ListePays_C
#%%

dispoVegetal= pd.read_csv("C:/Users/kaeli/Documents/python/FAOSTAT_2013_vegetal.csv",
                dtype={'Valeur':np.float64},
                 decimal='.')
ListePaysV=set(dispoVegetal["Pays"].values.tolist())


#%%

ListePays_V=set(dispoVegetal["Pays"].values.tolist())
print(len(ListePays_V))


#%%


popu.sort_values(by = 'Valeur')#Trie pour voir si il n'y a pas de Valeur aberrante

#%%
popu.tail(10) #regarde les plus grande dans le cas de Valeur aberrante

#%%
popu2=popu[popu.Zone.str.contains('Chine')]#regarde les differnet cas de la Chine
print(popu2)
#%%
b=popu.iloc[41,10]#compare chaque valeur pour chaque chine
c=popu.iloc[42,10]
d=popu.iloc[43,10]
e=popu.iloc[44,10]
f=popu.iloc[40,10]
print(f'population chinoise totale ={int(f*1000)}')
print(f'population chinoise continentale + macao + taiwan + hong kong ={int((b+c+d+e)*1000)}')
 #regarde si les valeur se valent
#%%
popu_sans_chine=popu.copy()# créer une copie


popu_sans_chine=popu_sans_chine.drop(labels=159)#supprime la ligne de la chine en trop

#%%

import math

population_total=sum(popu_sans_chine['Valeur'])
population_total=int(population_total*1000)
print(population_total)
#dispo_cereal1=dispoCereal.head(11)
#print(dispo_cereal1)