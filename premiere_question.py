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
popu2=popu.iloc[39:45,:]#regarde les differnet cas de la Chine
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


#%%


dispoAnimal = pd.read_csv("C:/Users/kaeli/OneDrive/Documents/GitHub/Group1/FAOSTAT_2013_animal.csv",
                dtype={'Valeur':np.float64},
                 decimal='.')

dispoVegetal= pd.read_csv("C:/Users/kaeli/OneDrive/Documents/GitHub/Group1/FAOSTAT_2013_vegetal.csv",
                dtype={'Valeur':np.float64},
                 decimal='.')

sousalim= pd.read_csv("C:/Users/kaeli/OneDrive/Documents/GitHub/Group1/FAOSTAT_2013_sous_alimentation.csv")


import matplotlib.pyplot as plt
plt.style.use('ggplot')

ListePays_A=set(dispoAnimal["Pays"].values.tolist())
ListePays_popu=set(popu_sans_chine["Zone"].values.tolist())

dispoA=dispoAnimal.loc[:,'Pays':'Valeur'] #enleve les colonne inutile pour animal
dispoA=dispoA[dispoA.Élément.str.contains('Disponibilité alimentaire')]#choisis les lignes utiles pour animal
dispoV=dispoVegetal.loc[:,'Pays':'Valeur']#enleve les colonne inutile pour Vegetal
dispoV=dispoV[dispoV.Élément.str.contains('Disponibilité alimentaire')]#choisis les lignes utiles pour vegetal
dispoCVA = pd.concat([dispoV, dispoA], axis=0)#colle mes 2 tableaux ensemble en ayant les elements voulus
dispoCVAkcal= dispoCVA[dispoCVA.Unité.str.contains('Kcal')]#ne garde que celle pour kcal

dispoA_1=dispoAnimal.loc[:,'Pays':'Valeur'] #enleve les colonne inutile pour animal
dispoA_1=dispoA_1[dispoA_1.Élément.str.contains('Disponibilité de prot')]#choisis les lignes utiles pour animal
dispoV_1=dispoVegetal.loc[:,'Pays':'Valeur']#enleve les colonne inutile pour Vegetal
dispoV_1=dispoV_1[dispoV_1.Élément.str.contains('Disponibilité de prot')]#choisis les lignes utiles pour vegetal
dispoCVA_1= pd.concat([dispoV_1, dispoA_1], axis=0)#colle mes 2 tableaux ensemble en ayant les elements voulus

#%% Pays/produit/kcal
dispoCVAkcal= dispoCVA[dispoCVA.Unité.str.contains('Kcal')]#ne garde que celle pour kcal
dispoCVAkcal2=dispoCVAkcal.drop(labels=['Code Année','Année','Code Produit','Code Élément','Élément','Unité'],axis=1)
  #enleve les colonne inutile
dispoCVAkcal2=pd.pivot_table(data=dispoCVAkcal2,index=['Pays','Produit'],aggfunc='sum')#me permet de faire une table multi index,a savoir pays et produit tout en faisant une somme

dispoCVAkcal2= dispoCVAkcal2.reset_index(level=['Pays','Produit'])#me permet de pouvoir de nouveau manipuler les index
dispoCVAkcal2.set_index("Pays",inplace=True)#met le pays comme index

dispoCVAkcal2=dispoCVAkcal2.drop(labels='Chine')#enleve la chine 

popu_sans_chine=popu_sans_chine.rename(columns={'Zone':'Pays'}) #change le nom pour me créer une clés "primaire"
popu_sans_chine3=popu_sans_chine.set_index("Pays")# set l'index
popu_sans_chine3=popu_sans_chine3.loc[:,"Valeur"]# choisis ma colonne voulus


resultkcal=  pd.merge(dispoCVAkcal2,popu_sans_chine3,on='Pays') #merge mon tableau qui contient les valeur par produit et par pays avec le tableau population
resultkcal['totalkcal_par_jour_et_par_habitant']=resultkcal['Valeur_x']*resultkcal['Valeur_y']*1000*365 # calcule mes ligne entre elles puit les multiplie par leur unitéresultkcal2['totalkcal_par_jour_et_par_habitant']=resultkcal2['Valeur_x']*resultkcal2['Valeur_y']*1000*365 # calcule mes ligne entre elles puit les multiplie par leur unité

resultkcal=resultkcal.drop(labels=['Valeur_x','Valeur_y'],axis=1)#vire mes colonne devenus inutile
resultkcal3=pd.pivot_table(data=resultkcal,index=['Pays'],aggfunc='sum')

#%% Pays/produit/kg(proteine)
dispoCVAkg_1= dispoCVA_1[dispoCVA_1.Unité.str.contains('g')] #selectionne mes lignes qui contienne kg
dispoCVAkg_1=dispoCVAkg_1.drop(labels=['Code Année','Année','Code Produit','Code Élément','Élément','Unité'],axis=1)
    #supprime mes colonne inutile
dispoCVAkg_2=pd.pivot_table(data=dispoCVAkg_1,index=['Pays','Produit'],aggfunc='sum')
    #comme precedent créer une table avec 2 index : pays et produit, tout en faisant la somme de ce qu'ils contienne
dispoCVAkg_2= dispoCVAkg_2.reset_index(level=['Pays','Produit'])#me permet de manipuler les index
dispoCVAkg_2.set_index("Pays",inplace=True)#choisis la colonne pays comme index

dispoCVAkg_2=dispoCVAkg_2.drop(labels='Chine')#supprime la ligne contenant la chine

resultkg_1=  pd.merge(dispoCVAkg_2,popu_sans_chine3,on='Pays') #merge mon tableau avec kg par rapport au produit et pays et la table contenant la population
resultkg_1['totalkg_par_jour_et_par_habitant']=(resultkg_1['Valeur_x']*resultkg_1['Valeur_y']*365)/1000#calcule mon kg par habitant par an

resultkg_1=resultkg_1.drop(labels=['Valeur_x','Valeur_y'],axis=1)# vire mes colonne devenus inutile

#%% table Pays/produit
result_final=  pd.merge(resultkg_1,resultkcal,on=['Pays','Produit'])#merge ma table kg et kcal

result_final['totalkcal/kg']=result_final['totalkcal_par_jour_et_par_habitant'].div(result_final['totalkg_par_jour_et_par_habitant'])
    #divise ma colonne kcal par la colonne kg
result_final=result_final.replace(0,np.nan)#enleve mes valeurs 0 pour ne pas faire une division par zeros
result_final=result_final.replace(np.inf,np.nan)#enleve mes valeurs aberante

#%% Pays/kcal
dispoCVAkcal4=dispoCVAkcal.drop(labels=['Code Année','Année','Code Produit','Code Élément','Élément','Unité','Produit'],axis=1)
#supprime de nuveau les colonne inutiles

dispoCVAkcal3=pd.pivot_table(data=dispoCVAkcal4,index=['Pays'],aggfunc='sum')#fait ma somme par rapoort a mes pays

dispoCVAkcal3= dispoCVAkcal3.reset_index(level='Pays')#me permet de rendre l'index manipulable
dispoCVAkcal3.set_index("Pays",inplace=True)#remet l'index maintenant manipulable comme index



resultkcal2=  pd.merge(dispoCVAkcal3,popu_sans_chine3,on='Pays') #colle les 2 tables avec pays comme clés "primaire"
resultkcal2['totalkcal_par_jour_et_par_habitant']=resultkcal2['Valeur_x']*resultkcal2['Valeur_y']*1000*365 # calcule mes ligne entre elles puit les multiplie par leur unité

#%% Pays/kg(proteine)
dispoCVAkg= dispoCVA_1[dispoCVA_1.Unité.str.contains('g')]# refait les memes etape précédente mais pour kg

dispoCVAkg1=dispoCVAkg.drop(labels=['Code Année','Année','Code Produit','Code Élément','Élément','Unité','Produit'],axis=1)

dispoCVAkg1=pd.pivot_table(data=dispoCVAkg1,index=['Pays'],aggfunc='sum')

dispoCVAkg1= dispoCVAkg1.reset_index(level='Pays')
dispoCVAkg1.set_index("Pays",inplace=True)


popu_sans_chine=popu_sans_chine.rename(columns={'Zone':'Pays'}) 
popu_sans_chine3=popu_sans_chine.set_index("Pays")
popu_sans_chine3=popu_sans_chine3.loc[:,"Valeur"]

resultkg=  pd.merge(dispoCVAkg1,popu_sans_chine3,on='Pays') 
resultkg['totalkg_par_jour_et_par_habitant']=resultkg['Valeur_x']*resultkg['Valeur_y']*365

resultkg2=resultkg.loc[:,'totalkg_par_jour_et_par_habitant']#garde ma colonne voulus
resultkcal2=resultkcal2.loc[:,'totalkcal_par_jour_et_par_habitant']#garde ma colonne voulus
resultpays=pd.merge(resultkcal2,resultkg2,on='Pays')#colle les 2 tables ayant mes valeur de kg et kcal

resultpays['totalkcal/kg']=resultpays['totalkcal_par_jour_et_par_habitant'].div(resultpays['totalkg_par_jour_et_par_habitant'])
#fait l'energie par pays
resultpays=resultpays.replace(0,np.nan)#enleve mes valeurs aberante
resultpays=resultpays.replace(np.inf,np.nan)#enleve mes valeurs aberante
#%%Pays/kg(dispo alimentaire)
dispoCVA= dispoCVA[dispoCVA.Unité.str.contains('kg')]
dispoCVAalim=dispoCVA.drop(labels=['Code Année','Année','Code Produit','Code Élément','Élément','Unité','Produit'],axis=1)

dispoCVAalim=pd.pivot_table(data=dispoCVAalim,index=['Pays'],aggfunc='sum')
dispoCVAalim= dispoCVAalim.reset_index(level='Pays')
dispoCVAalim.set_index("Pays",inplace=True)

resultkgalim=  pd.merge(dispoCVAalim,popu_sans_chine3,on='Pays')

resultkgalim['totalkg_par_jour_et_par_habitant']=resultkgalim['Valeur_x']*resultkgalim['Valeur_y']*365*1000

resultkgalim=resultkgalim.replace(0,np.nan)#enleve mes valeurs aberante
resultkgalim=resultkgalim.replace(np.inf,np.nan)#enleve mes valeurs aberante

resultkgalim=resultkgalim.drop(labels=['Valeur_x','Valeur_y'], axis=1)

#%% Produit/kg(dispo alimentaire)
dispoCVA= dispoCVA[dispoCVA.Unité.str.contains('kg')]
dispoCVAalimProduit=dispoCVA.drop(labels=['Code Année','Année','Code Produit','Code Élément','Élément','Unité'],axis=1)

dispoCVAalimProduit=pd.pivot_table(data=dispoCVAalimProduit,index=['Produit','Pays'],aggfunc='sum')
dispoCVAalimProduit= dispoCVAalimProduit.reset_index(level=['Produit','Pays'])
dispoCVAalimProduit.set_index("Pays",inplace=True)

resultkgalimProduit=  pd.merge(dispoCVAalimProduit,popu_sans_chine3,on='Pays')

resultkgalimProduit['totalkg_par_jour_et_par_habitant']=resultkgalimProduit['Valeur_x']*resultkgalimProduit['Valeur_y']*365*1000

resultkgalimProduit=resultkgalimProduit.replace(0,np.nan)#enleve mes valeurs aberante
resultkgalimProduit=resultkgalimProduit.replace(np.inf,np.nan)#enleve mes valeurs aberante

resultkgalimProduit=resultkgalimProduit.drop(labels=['Valeur_x','Valeur_y'], axis=1)

result_dispo_alim=pd.merge(resultkgalimProduit,resultkcal,on=['Pays','Produit'])

result_dispo_alim['totalkcal/kg']=result_dispo_alim['totalkcal_par_jour_et_par_habitant'].div(result_dispo_alim['totalkg_par_jour_et_par_habitant'])

result_dispo_alim=result_dispo_alim.replace(0,np.nan)
result_dispo_alim=result_dispo_alim.replace(np.inf,np.nan)

#%% Produit/kcal §§§§ a revoir §§§§
dispoProduitkcal=dispoCVAkcal.drop(labels=['Code Année','Année','Code Produit','Code Élément','Élément','Unité'],axis=1)#fait les meme chose plus haut mais pour avoir des table par rapport au produit et non au pays
#dispoProduitkcal=pd.pivot_table(data=dispoProduitkcal,index=['Produit'],aggfunc='sum')
#dispoProduitkcal['kcal/an']=dispoProduitkcal['Valeur']*365

#%% Produit/kg(proteine)

dispoProduitkgprot=dispoCVAkg.drop(labels=['Code Année','Année','Code Produit','Code Élément','Élément','Unité','Pays'],axis=1)
dispoProduitkgprot=pd.pivot_table(data=dispoProduitkgprot,index=['Produit'],aggfunc='sum')
dispoProduitkgprot['kg/an']=dispoProduitkgprot['Valeur']*365

#%% Produit/kg(total)  §§§§§ a revoir §§§§§
dispoCVA= dispoCVA[dispoCVA.Unité.str.contains('kg')]
dispoProduitkg_tot_pays=dispoCVA.drop(labels=['Code Année','Année','Code Produit','Code Élément','Élément','Unité'],axis=1)
#dispoProduitkg_tot=pd.pivot_table(data=dispoProduitkg_tot,index=['Produit'],aggfunc='sum')
#dispoProduitkg_tot['kg/an']=dispoProduitkg_tot['Valeur']*365

dispo_result_kg_kcal_pays=pd.merge(dispoProduitkg_tot_pays,dispoProduitkcal,how='outer',on=['Pays','Produit'])

dispo_result_kg_kcal_pays['kcal/kg']=(dispo_result_kg_kcal_pays['Valeur_y'])/(dispo_result_kg_kcal_pays['Valeur_x']/365)
#%% Produit tot/prot §§§§§ a revoir §§§§§
'''result_Produit_kcal_kg_prot=  pd.merge(dispoProduitkcal,dispoProduitkgprot,on=['Produit'])
result_Produit_kcal_kg_prot=result_Produit_kcal_kg_prot.drop(labels=['Valeur_x','Valeur_y'],axis=1)

result_Produit_kcal_kg_prot['totalkcal/kg']=result_Produit_kcal_kg_prot['kcal/an'].div(result_Produit_kcal_kg_prot['kg/an'])

result_Produit_kcal_kg_prot=result_Produit_kcal_kg_prot.replace(0,np.nan)
result_Produit_kcal_kg_prot=result_Produit_kcal_kg_prot.replace(np.inf,np.nan)

result_kcal_kg_Max=result_Produit_kcal_kg_prot.sort_values(by=['totalkcal/kg','Produit'], ascending=False)
print(result_kcal_kg_Max.head(10))#trie mes valeur d'energie de produit du plus grand au plus petit

result_kcal_kg_Min=result_Produit_kcal_kg_prot.sort_values(by=['totalkcal/kg','Produit'], ascending=True)
print(result_kcal_kg_Min.head(10))#trie mes valeur d'energie de produit du plus petit au plus grand
'''
#%% Produit tot
'''result_Produit_kcal_kg=  pd.merge(dispoProduitkcal,dispoProduitkg_tot,on=['Produit'])
result_Produit_kcal_kg=result_Produit_kcal_kg.drop(labels=['Valeur_x','Valeur_y'],axis=1)

result_Produit_kcal_kg['totalkcal/kg']=result_Produit_kcal_kg['kcal/an'].div(result_Produit_kcal_kg['kg/an'])

result_Produit_kcal_kg=result_Produit_kcal_kg.replace(0,np.nan)
result_Produit_kcal_kg=result_Produit_kcal_kg.replace(np.inf,np.nan)

result_kcal_kg_Max_tot=result_Produit_kcal_kg.sort_values(by=['totalkcal/kg','Produit'], ascending=False)
result_kcal_kg_Min_tot1=result_kcal_kg_Max_tot.head(10)#trie mes valeur d'energie de produit du plus grand au plus petit

result_kcal_kg_Min_tot=result_Produit_kcal_kg.sort_values(by=['totalkcal/kg','Produit'], ascending=True)
result_kcal_kg_Min_tot2=result_kcal_kg_Min_tot.head(10)#trie mes valeur d'energie de produit du plus petit au plus grand'''

#%% QUESTION 6
'''kcal_par_produit_par_pays1=dispoCVAkcal.drop(labels=['Code Année','Année','Code Produit','Code Élément','Élément','Unité'],axis=1)
kcal_par_produit_par_pays=pd.merge(kcal_par_produit_par_pays1,popu_sans_chine3,on=['Pays'])
kcal_par_produit_par_pays['kcal/pays']=kcal_par_produit_par_pays['Valeur_x']*kcal_par_produit_par_pays['Valeur_y']
kcal_par_produit_par_pays=pd.pivot_table(data=kcal_par_produit_par_pays,index=['Pays'],aggfunc='sum')
kcal_par_produit_par_pays= kcal_par_produit_par_pays.reset_index(level='Pays')
kcal_par_produit_par_pays.set_index("Pays",inplace=True)
kcal_par_produit_par_pays=kcal_par_produit_par_pays.drop(labels=['Produit'],axis=1)
azer=kcal_par_produit_par_pays['kcal/pays'].sum()
print(f'La disponibilité interieur mondiale (peut etre vrai) et végetale est de {azer}kcal')'''

dispoInterieurV=dispoVegetal[dispoVegetal.Élément.str.contains('Disponibilité intérieure')]
dispoInterieurV=dispoInterieurV.loc[:,['Valeur','Produit','Pays']]
dispoInterieurV=pd.pivot_table(data=dispoInterieurV,index=['Produit','Pays'],aggfunc='sum')
dispoInterieurV['kg']=dispoInterieurV['Valeur']*1000000
dispoInterieurV= dispoInterieurV.reset_index(level=['Produit','Pays'])
dispoInterieurV.set_index("Produit",inplace=True)
dispoInterieurV=dispoInterieurV.drop(labels='Valeur',axis=1)


vegetal=set(dispoInterieurV.index.values.tolist())
vegetal=list(vegetal)

dispo_result_kg_kcal_pays.set_index("Produit",inplace=True)

dispo_result_kg_kcal_pays=dispo_result_kg_kcal_pays.loc[[i for i in vegetal if i in dispo_result_kg_kcal_pays.index],:]

#dispo_result_kg_kcal_pays=dispo_result_kg_kcal_pays.drop(labels=['Valeur_x','Valeur_y'],axis=1)
dispo_result_kg_kcal_pays.reset_index(inplace=True)

dispoInterieurV1=pd.merge(dispo_result_kg_kcal_pays,dispoInterieurV,on=['Produit','Pays'])
dispoInterieurV1=dispoInterieurV1.replace(0,np.nan)
dispoInterieurV1=dispoInterieurV1.replace(np.inf,np.nan)
dispoInterieurV1.dropna(inplace=True)

dispoInterieurV1['kcal']=dispoInterieurV1['kcal/kg']*dispoInterieurV1['kg']
Total_dispo_int_veget=dispoInterieurV1['kcal'].sum()

print(f'La disponibilité interieur mondiale et végetale est de {Total_dispo_int_veget}kcal')

#%%
Popu_H_F= pd.read_csv("C:/Users/kaeli/OneDrive/Documents/GitHub/Group1/FAOSTAT_populationHF.csv",
                dtype={'Valeur':np.float64},
                 decimal='.')


Popu_H_F=Popu_H_F.loc[:,['Valeur','Élément']]
Popu_H_F=Popu_H_F.groupby(['Élément']).sum()

Popu_H_F= Popu_H_F.reset_index(level=['Élément'])
Popu_H_F.set_index("Élément",inplace=True)
Popu_H_F2=Popu_H_F.copy()
Popu_H_F['percent'] = (Popu_H_F['Valeur'] / Popu_H_F['Valeur'].sum()) * 100

moyenne_kcal=((Popu_H_F.loc['Hommes',['percent']]*2500)+(Popu_H_F.loc['Femmes',['percent']]*2000)).sum()/100
print(f'La moyenne est {moyenne_kcal}')
Popu_H_F2.loc['Hommes',['Valeur']]=Popu_H_F2.loc['Hommes',['Valeur']]*2500*1000
Popu_H_F2.loc['Femmes',['Valeur']]=Popu_H_F2.loc['Femmes',['Valeur']]*2000*1000

moyenne_kcal_an=moyenne_kcal*365

print(f"Le nombre d'humain que l'on pourrait nourrir est de :{Total_dispo_int_veget/moyenne_kcal_an} ce qui correspond à {((Total_dispo_int_veget/moyenne_kcal_an)*100/(population_total))}%")

#%% dispo interieur en protéine
dispo_interieur_V2=dispoVegetal[dispoVegetal.Élément.str.contains('Disponibilité de protéines') ]
dispo_interieur_V3=dispoVegetal[dispoVegetal.Élément.str.contains('Disponibilité alimentaire en quantité')]
dispo_interieur_V5=dispoVegetal[dispoVegetal.Élément.str.contains('Disponibilité intérieur')]
dispo_interieur_V2=dispo_interieur_V2.loc[:,['Valeur','Produit','Pays','Élément']]
dispo_interieur_V3=dispo_interieur_V3.loc[:,['Valeur','Produit','Pays','Élément']]
dispo_interieur_V5=dispo_interieur_V5.loc[:,['Valeur','Produit','Pays','Élément']]

dispo_interieur_V3['Valeur']=dispo_interieur_V3['Valeur']

dispo_interieur_V4 = pd.merge(dispo_interieur_V2,dispo_interieur_V3,on=['Produit','Pays'],how='outer')
dispo_interieur_V4 = pd.merge(dispo_interieur_V4,dispo_interieur_V5,on=['Produit','Pays'],how='outer')

dispo_interieur_V4=dispo_interieur_V4.replace(0,np.nan)

dispo_interieur_V4['ratio de proteine']=(dispo_interieur_V4['Valeur_y']/365 * 1000) / (dispo_interieur_V4['Valeur_x'])
dispo_interieur_V4['kg de proteine par produit']=(dispo_interieur_V4['Valeur']*1000000) / (dispo_interieur_V4['ratio de proteine'])

a=dispo_interieur_V4['kg de proteine par produit'].sum()
print(a)


MoyenneBasseProteine = round(int(((50*365)+(62*365))/2),0)/1000
MoyenneHauteProteine =round(int(((138*365)+(170*365))/2),0)/1000
moyenneProteine= round(int((MoyenneHauteProteine+MoyenneBasseProteine)/2),0)
pop_prot_basse=(MoyenneBasseProteine*population_total)
pop_prot_haute=(MoyenneHauteProteine*population_total)
pop_prot=moyenneProteine*population_total



print(f"La disponibilité interieur basse en proteine permettrai de nourrir : {(a*100)/pop_prot_basse} %")
print(f"La disponibilité interieur haute en proteine permettrai de nourrir : {(a*100)/pop_prot_haute} %")

#%% Question 8
pot_alimentaire_V1=dispoVegetal[dispoVegetal.Élément.str.contains('Pertes') ]#millier de tonnes
pot_alimentaire_V2=dispoVegetal[dispoVegetal.Élément.str.contains('Disponibilité alimentaire en quantité')]#kg/personne/an
pot_alimentaire_V3=dispoVegetal[dispoVegetal.Élément.str.contains('Aliments pour animaux')]#millier de tonne
pot_alimentaire_V1=pot_alimentaire_V1.loc[:,['Valeur','Produit','Pays']]
pot_alimentaire_V2=pot_alimentaire_V2.loc[:,['Valeur','Produit','Pays']]
pot_alimentaire_V3=pot_alimentaire_V3.loc[:,['Valeur','Produit','Pays']]

azert=pot_alimentaire_V1['Valeur'].sum()
azert2=pot_alimentaire_V2['Valeur'].sum()
azert3=pot_alimentaire_V3['Valeur'].sum()

print(f"mon total en millier de tonne  de perte est de :{azert}")
print(f"mon total en millier de tonne  d'Aliments pour animaux est de :{azert2}")
print(f"mon total en millier de tonne  de Disponibilité alimentaire en quantité est de :{azert3}")

pot_alimentaire_V1=pot_alimentaire_V1.rename(columns={'Valeur' : 'Millier de tonne'})
pot_alimentaire_V3=pot_alimentaire_V3.rename(columns={'Valeur' : 'Millier de tonne'})

pot_alimentaire_V2=pd.merge(pot_alimentaire_V2,popu_sans_chine3,on=['Pays'],how='outer')
pot_alimentaire_V2['millier de tonne']=((pot_alimentaire_V2['Valeur_x']*pot_alimentaire_V2['Valeur_y'])/1000)
pot_alimentaire_V2=pot_alimentaire_V2.loc[:,['Produit','Pays','millier de tonne']]

pot_alimentaire_V4=pd.merge(pot_alimentaire_V1,pot_alimentaire_V2,how='outer',on=['Pays','Produit'])
pot_alimentaire_V4=pd.merge(pot_alimentaire_V4,pot_alimentaire_V3,how='outer',on=['Pays','Produit'])

pot_alimentaire_V4=pot_alimentaire_V4.replace(np.nan,0)

pot_alimentaire_V4['total en millier de tonne']=pot_alimentaire_V4['millier de tonne']+pot_alimentaire_V4['Millier de tonne_x']+pot_alimentaire_V4['Millier de tonne_y']
azer2=pot_alimentaire_V4['total en millier de tonne'].sum()
print(f'Le total en millier de tonne du potentiel alimentaire et de :{azer2}')
print(f'Le total en kg du potentiel alimentaire et de :{azer2*1000000}')

dispo_interieur_V4_1=dispo_interieur_V4.loc[:,['Pays','Produit','ratio de proteine']]
pot_alimentaire_V4=pd.merge(pot_alimentaire_V4,dispo_interieur_V4_1,how='outer',on=['Pays','Produit'])

pot_alimentaire_V4['prot en millier de tonne']=pot_alimentaire_V4['total en millier de tonne']/pot_alimentaire_V4['ratio de proteine']
azer3=pot_alimentaire_V4['prot en millier de tonne'].sum()
print(f'Le total en millier de tonne de protéine du potentiel alimentaire et de :{azer3}')
print(f'la moyenne de proteine par habitant est de :{moyenneProteine}')
print(f"Ce qui nous donne en terme de population nourrissable est de {(azer3*1000000)/moyenneProteine} ce qui correspond a {(((azer3*1000000)/moyenneProteine)*100)/population_total}%")

#pot_alimentaire_V4=pd.merge(pot_alimentaire_V4,popu_sans_chine3,how='outer',on=['Pays'])

pot_alimentaire_V4=pd.merge(pot_alimentaire_V4,dispo_result_kg_kcal_pays,how='outer',on=['Pays','Produit'])
pot_alimentaire_V4['kcal']=pot_alimentaire_V4['total en millier de tonne']*(pot_alimentaire_V4['kcal/kg'])*1000000
pot_alimentaire_V4=pot_alimentaire_V4.replace(np.inf,0)



azer4=pot_alimentaire_V4['kcal'].sum()
print(f'Le total en kcal et de :{azer4}')
print(f"Le nombre d'humain que l'on pourrait nourrir est de :{azer4/moyenne_kcal_an} ce qui correspond à {((azer4/moyenne_kcal_an)/(population_total))} fois le nombre d'humain")

#%% question 9
dispo_alimentaire_vege_viande=dispoCVA.loc[:,['Pays','Produit','Valeur']]

dispo_vege_viande=pd.concat([dispoAnimal,dispoVegetal])

dispo_vege_viande1=dispo_vege_viande[dispo_vege_viande.Élément.str.contains('Disponibilité de protéines')]
#dispo_vege_viande2=dispo_vege_viande[dispo_vege_viande.Élément.str.contains('Disponibilité alimentaire en quantité')]
dispo_vege_viande3=dispo_vege_viande[dispo_vege_viande.Élément.str.contains('Kcal')]

dispo_vege_viande1=dispo_vege_viande1.loc[:,['Pays','Produit','Unité','Valeur']]
#dispo_vege_viande2=dispo_vege_viande2.loc[:,['Pays','Produit','Unité','Valeur']]
dispo_vege_viande3=dispo_vege_viande3.loc[:,['Pays','Produit','Unité','Valeur']]

dispo_vege_viande=pd.merge(dispo_vege_viande1,dispo_vege_viande3,how='outer',on=['Pays','Produit'])
#dispo_vege_viande=pd.merge(dispo_vege_viande,dispo_vege_viande2,how='outer',on=['Pays','Produit'])
dispo_vege_viande=pd.merge(dispo_vege_viande,popu_sans_chine3,how='outer',on=['Pays'])

dispo_vege_viande['kcal']=dispo_vege_viande['Valeur_y']*dispo_vege_viande['Valeur']*365*1000
dispo_vege_viande['g de prot']=dispo_vege_viande['Valeur_x']*dispo_vege_viande['Valeur']*365

azerty=dispo_vege_viande['kcal'].sum()
azerty2=dispo_vege_viande['g de prot'].sum()
print(moyenne_kcal_an*population_total)
print(f'La population nourrissable en kcal avec la disponibilité alimentaire mondiale est de {azerty/moyenne_kcal_an}, ce qui correspond a {(azerty*100)/(moyenne_kcal_an*population_total)} %')
print(f'La population nourrissable en prot avec la disponibilité alimentaire mondiale est de {(azerty2*100)/pop_prot} %')

#%% question 10

sousalim=sousalim.rename(columns={'Zone':'Pays'})


sousalim1=sousalim.loc[:,['Pays','Valeur','Symbole']]

sousalim1=sousalim1.set_index('Pays')
sousalim1=sousalim1.drop(labels='Chine')
sousalim1=sousalim1.replace(np.nan,0)
for count,i in enumerate(sousalim1.Symbole):
    if i[0]=='<':
        sousalim1['Valeur'][count]=float(i[1:])
        
    

pop_sousalim=sousalim1['Valeur'].sum()
print(f'La proportion de sous alimentation est de {(pop_sousalim*100*1000000)/population_total}%')

#%% question 11
dispoCereal=dispoCereal.set_index('Pays')
dispoCereal=dispoCereal.drop(labels='Chine')
dispoCereal=dispoCereal.reset_index()

code_Produit_Cereale= list(dispoCereal['Code Produit'].values.tolist())
Produit_Cereale=list(dispoCereal['Produit'].values.tolist())
Dico_Code_Cereale=dict(zip(code_Produit_Cereale,Produit_Cereale))
print(Dico_Code_Cereale)

Cereal_nourriture1=dispoCereal[dispoCereal.Élément.str.contains('Nourriture')]
Cereal_nourriture2=dispoCereal[dispoCereal.Élément.str.contains('Aliments pour')]

Cereal_nourriture1=Cereal_nourriture1.loc[:,['Pays','Produit','Valeur','Unité']]
Cereal_nourriture2=Cereal_nourriture2.loc[:,['Pays','Produit','Valeur','Unité']]

Cereal_nourriture=pd.merge(Cereal_nourriture1, Cereal_nourriture2,how='outer', on =['Pays','Produit'])

Cereal_nourriture=Cereal_nourriture.replace(np.nan,0)
Cereal_nourriture["Quantité pour l'alimentation"]=Cereal_nourriture['Valeur_y']+Cereal_nourriture['Valeur_x']

Nourriture_total_cereal=Cereal_nourriture["Quantité pour l'alimentation"].sum()
Nourriture_animal_cereal=Cereal_nourriture['Valeur_y'].sum()

print(f"Il y a {(Nourriture_animal_cereal*100)/Nourriture_total_cereal}% pour les animaux")

#%%Question 12
list_pays_sousalim=[]
sousalim1=sousalim1.reset_index()
for count1,i in enumerate(sousalim1.Valeur):
    if i!=0:
        list_pays_sousalim.append(sousalim1['Pays'][count1])
print(len(list_pays_sousalim))

dispo_vege_viande_monde=pd.concat([dispoAnimal,dispoVegetal])
dispo_vege_viande_monde=dispo_vege_viande_monde.set_index('Pays')
dispo_vege_viande_monde=dispo_vege_viande_monde.drop(labels='Chine')
dispo_vege_viande_monde=dispo_vege_viande_monde.reset_index()


dispo_vege_viande_sousalim=dispo_vege_viande_monde.set_index('Pays')

dispo_vege_viande_sousalim=dispo_vege_viande_sousalim.loc[[i for i in list_pays_sousalim if i in dispo_vege_viande_sousalim.index ],:]
dispo_vege_viande_sousalim=dispo_vege_viande_sousalim.reset_index()
        
dispo_vege_viande_sousalim_export=dispo_vege_viande_sousalim[dispo_vege_viande_sousalim.Élément.str.contains('Exportation')]
dispo_vege_viande_sousalim_export=dispo_vege_viande_sousalim_export.loc[:,['Pays','Produit','Valeur']]

dispo_vege_viande_sousalim_export=dispo_vege_viande_sousalim_export.set_index('Produit')
dispo_vege_viande_sousalim_export=dispo_vege_viande_sousalim_export.drop(labels=['Pays'],axis=1)

dispo_vege_viande_sousalim_export_produit=dispo_vege_viande_sousalim_export.groupby(level='Produit').mean()

dispo_vege_viande_sousalim_export_produit=dispo_vege_viande_sousalim_export_produit.sort_values(by=['Valeur'],ascending=False)
dispo_vege_viande_sousalim_export_produit_max=dispo_vege_viande_sousalim_export_produit.head(15)

print(dispo_vege_viande_sousalim_export_produit_max)

dispo_vege_viande_sousalim_export_produit_max=dispo_vege_viande_sousalim_export_produit_max.reset_index()

produit_plus_export=list(dispo_vege_viande_sousalim_export_produit_max['Produit'].values.tolist())

dispo_vege_viande_monde_import=dispo_vege_viande_monde[dispo_vege_viande_monde.Élément.str.contains('Importation')]
dispo_vege_viande_monde_import=dispo_vege_viande_monde_import.loc[:,['Pays','Produit','Valeur']]

dispo_vege_viande_monde_import=dispo_vege_viande_monde_import[dispo_vege_viande_monde_import['Produit'].isin(produit_plus_export)]
dispo_vege_viande_monde_import=dispo_vege_viande_monde_import.sort_values(by=['Valeur'],ascending=False)
dispo_vege_viande_monde_import=dispo_vege_viande_monde_import.head(200)

produit_plus_import1=list(dispo_vege_viande_monde_import['Produit'].values.tolist())
produit_plus_import2=list(dispo_vege_viande_monde_import['Pays'].values.tolist())

dispo_vege_viande_monde_import2=dispo_vege_viande_monde[dispo_vege_viande_monde['Produit'].isin(produit_plus_import1) & dispo_vege_viande_monde['Pays'].isin(produit_plus_import2)]
dispo_vege_viande_monde_import2=dispo_vege_viande_monde_import2.loc[:,['Pays','Produit','Élément','Valeur']]

element=list(set(dispo_vege_viande_monde_import2['Élément'].values.tolist()))
pays=list(dispo_vege_viande_monde_import2['Pays'].values.tolist())
produit=list(dispo_vege_viande_monde_import2['Produit'].values.tolist())


dispo_vege_viande_monde_import3 = pd.DataFrame(columns=['Pays','Produit','Valeur'])
mlkj='Valeur'
mlkj1='Valeur'


for count3,i in enumerate(element):
    poiu=dispo_vege_viande_monde_import2[dispo_vege_viande_monde_import2.Élément.str.startswith(f"{i}")]
    poiu=poiu.drop(labels=['Élément'],axis=1)
    dispo_vege_viande_monde_import3=pd.merge(dispo_vege_viande_monde_import3,poiu,how='outer',on=['Pays','Produit'])
      
    if mlkj in dispo_vege_viande_monde_import3.columns.tolist():
        dispo_vege_viande_monde_import3=dispo_vege_viande_monde_import3.rename(columns={'Valeur': f"{element[int(count3)]}"})
    if mlkj1 in dispo_vege_viande_monde_import3.columns.tolist():
        dispo_vege_viande_monde_import3=dispo_vege_viande_monde_import3.rename(columns={'Valeur': f"{element[int(count3)]}"})
        
    if 'Valeur_x' in dispo_vege_viande_monde_import3.columns.tolist():
        dispo_vege_viande_monde_import3=dispo_vege_viande_monde_import3.rename(columns={'Valeur_x': f"{element[int(count3)]}"})
    if 'Valeur_y' in dispo_vege_viande_monde_import3.columns.tolist():
        dispo_vege_viande_monde_import3=dispo_vege_viande_monde_import3.rename(columns={'Valeur_y': f"{element[int(count3)]}"})



dispo_vege_viande_monde_import3 = dispo_vege_viande_monde_import3.dropna(axis=1, how='all')
dispo_vege_viande_monde_import3=dispo_vege_viande_monde_import3.replace(np.nan,0)
dispo_vege_viande_monde_import4=dispo_vege_viande_monde_import3.drop(['Pays'],axis=1)

dispo_vege_viande_monde_import4=dispo_vege_viande_monde_import4.set_index('Produit')
dispo_vege_viande_monde_import4=dispo_vege_viande_monde_import4.groupby(level='Produit').sum()

dispo_vege_viande_monde_import4['ratio (other use)/(dispo inter)']=dispo_vege_viande_monde_import4['Autres Utilisations']/dispo_vege_viande_monde_import4['Disponibilité intérieure']

dispo_vege_viande_monde_import4['ratio (nour A)/(nour H+A)']=dispo_vege_viande_monde_import4['Aliments pour animaux']/(dispo_vege_viande_monde_import4['Aliments pour animaux']+dispo_vege_viande_monde_import4['Nourriture'])

print(f"le ratio (autre utilisation)/(disponibilité intérieur) est en moyenne de : {dispo_vege_viande_monde_import4['ratio (other use)/(dispo inter)'].mean()}")
print(f"le ratio (nourriture A)/(nourriture H+A) est de : {dispo_vege_viande_monde_import4['ratio (nour A)/(nour H+A)'].mean()}")

dispo_vege_viande_monde_import4_ratio_autre_utilisation=dispo_vege_viande_monde_import4.sort_values(by=['ratio (other use)/(dispo inter)'],ascending=False)

dispo_vege_viande_monde_import4_ratio_nourriture_anim=dispo_vege_viande_monde_import4.sort_values(by=['ratio (nour A)/(nour H+A)'],ascending=False)

#%%question 13

dispoCerealUsa=dispoCereal[dispoCereal.Pays.str.contains('Unis')]
dispoCerealUsa=dispoCerealUsa[dispoCerealUsa.Élément.str.contains('Aliments pour ')]
dispoCerealUsa['tonne libéré']=dispoCerealUsa['Valeur']/10
print(f"Le nombre en milier de tonne libéré pour les USA est de : {dispoCerealUsa['tonne libéré'].sum()}")

#%% question 14
dispoManioc=dispoVegetal[dispoVegetal.Pays.str.contains('Thaïlande')]
dispoManioc=dispoManioc[dispoManioc.Produit.str.contains('Manioc')]