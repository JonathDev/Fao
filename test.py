import pandas as pd
import numpy as np
import csv

popu = pd.read_csv("C:/Users/kaeli/OneDrive/Documents/GitHub/Group1/FAOSTAT_data_fr_12-18-2023.csv",
                dtype={'Valeur':np.float64},
                index_col='Code zone (M49)',
                decimal='.')

#popu1, popu2=popu.query("Zone in ('Chine')"), popu.query("Zone == 'Chine")
popu1=popu[popu.Zone.str.contains('Chine')]
popu2=popu[popu.Zone.str.startswith('Chine')]
print(popu1)

dispoCereal = pd.read_csv("C:/Users/kaeli/OneDrive/Documents/GitHub/Group1/FAOSTAT_2013_cereal.csv",
                dtype={'Valeur':np.float64},
                 decimal='.')
dispoCereal2=dispoCereal.loc[ dispoCereal.Pays.str.contains('France') & dispoCereal.Produit.str.contains('Blé'),'Élément':]
print(dispoCereal2)
