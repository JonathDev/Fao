import pandas as pd
import numpy as np 
import utility

#v = ProductAnimals.columns
#v = ProductAnimals.loc[0]
#v = ProductAnimals.dtypes
#colums = ["Code Domaine","Domaine","Code Pays","Pays","Code Élément","Élément","Code Produit","Produit","Code Année","Année","Unité","Valeur","Symbole","Description du Symbole"]
#recup_data = ProductAnimals[["Code Pays","Pays","Code Élément","Élément","Code Produit","Produit","Code Année","Année","Unité","Valeur"]]

#productVegetals = 'dataFAO/FAOSTAT_2013_vegetal.csv'
#pop = 'dataFAO/FAOSTAT_2013_population.csv'
#ProductAnimals ='dataFAO/FAOSTAT_2013_animal.csv'
def add_pop() : 
    """ Calcule de la population mondial à partir d'un dataframe
    
    Paramètres: NaN 
    
    Retourne:  le total de la population mondial. 
    """
    # recupération du dataFrame populaition mondial
    df = utility.formatCsv('dataFAO/FAOSTAT_2013_population.csv', ["Pays", "Valeur"])
    # modification du type Valeur par un Float
    numeric_values = df["Valeur"].astype('float64')
    #  Somme des valeurs de tous les pays
    total = numeric_values.sum()
    
    # je modifie l'unité de mesure et retourne le total
    total = int(total * 1000)
    return total


def calcul_disponible_alimentaire(tri, code):

    # recupération des dataFrames et des données utiles
    df_pays = utility.formatCsv('dataFAO/FAOSTAT_2013_population.csv', ["Pays", "Valeur"])
    df_animals =  utility.formatCsv('dataFAO/FAOSTAT_2013_animal.csv', ["Pays","Code Élément", "Élément","Code Produit",'Produit' , "Valeur"])
    df_vegetals = utility.formatCsv('dataFAO/FAOSTAT_2013_vegetal.csv', ["Pays","Code Élément", "Élément","Code Produit",'Produit' , "Valeur"])
    
    # suppression des lignes dont la valeur est égale à 0
    df_animals = df_animals.drop(df_animals[df_animals['Valeur'] == 0].index)
    df_vegetals = df_vegetals.drop(df_vegetals[df_vegetals['Valeur']==0].index)
    
    # creation d'un dataFrame en concaténant les deux dataFrames initiales
    df_concat = pd.concat([df_animals, df_vegetals])
    #print(df_concat)
  
    #df_pays['Valeur'] = df_pays['Valeur'] * 1000
    #print(df_pays)

    # création d'un dataFrame en filtrant les données en fonction du Code Element
    df_filtered = utility.filtred(df_concat, code)
        
    df_sum = utility.calculate_and_sort(df_filtered, tri)
    #print(df_sum['Valeur'])
    # création d'un dataframe final avec les elements choisie 
    df_final = df_sum[[tri, 'Valeur']]
    return df_final
 
 
#dispkcalproduit = calcul_disponible_alimentaire('Produit', 664)
#dispokcalpays = calcul_disponible_alimentaire('Pays', 664)

#dispoproteineproduit = calcul_disponible_alimentaire('Produit', 674)
#dispoproteinepays= calcul_disponible_alimentaire('Pays', 674)
"""
def merge_produit_pays() : 
    
    dispkcalproduit = calcul_disponible_alimentaire('Produit', 664)
    dispokcalpays = calcul_disponible_alimentaire('Pays', 664)
    print(dispkcalproduit)
    print(dispokcalpays)
    #merge = pd.merge('table1' , 'table2', how= 'outer', on = 'Pays' )
    #pivot = pd.pivot_table( 'table1', index = ['index', 'index2'], aggfunc = sum)
merge_produit_pays()
"""

def ratio(choix):
    
    if choix == 1 :
        df_Dp_produit = calcul_disponible_alimentaire('Produit', 645)
        df_Kcal_produit = calcul_disponible_alimentaire('Produit', 664)
        df_Dp_produit = df_Dp_produit.set_index('Produit')
        df_Kcal_produit = df_Kcal_produit.set_index('Produit')
        df_Dp_produit['Valeur'] = df_Dp_produit['Valeur']/365
        
        df_ratio_kcal_kg = df_Kcal_produit.divide(df_Dp_produit).reset_index()
        return df_ratio_kcal_kg
        
    elif choix == 2 : 
        df_Dp_produit = calcul_disponible_alimentaire('Produit', 645)
        df_proteine_produit = calcul_disponible_alimentaire('Produit', 674)
        df_Dp_produit = df_Dp_produit.set_index('Produit')
        df_protine_produit = df_proteine_produit.set_index('Produit')
        df_Dp_produit['Valeur'] = df_Dp_produit['Valeur']/365
        
        df_ratio_proteineg_kg = df_protine_produit.divide(df_Dp_produit).reset_index()
        return df_ratio_proteineg_kg
    elif choix == 3 :
        df_Dp_pays = calcul_disponible_alimentaire(645, 'Pays')
        df_Kcal_pays = calcul_disponible_alimentaire(664, 'Pays')
        df_Dp_pays = df_Dp_pays.set_index('Pays')
        df_Kcal_pays = df_Kcal_pays.set_index('Pays')
        df_Dp_pays['Valeur'] = df_Dp_pays['Valeur']/365
        df_ratio_pays = df_Kcal_pays.divide(df_Dp_pays).reset_index()
        return df_ratio_pays


def test_oeuf () : 
    df_oeuf = ratio(1)
    df_oeuf = df_oeuf.loc[df_oeuf['Produit'] == 'Oeufs']
    return df_oeuf
    
#test_oeuf()
    


def top_nourriture(value):
    
    if value == 'kcal' : 
        df_ratio_kcal = ratio(1)
        df_ratio_kcal = df_ratio_kcal.dropna()
        df_ratio_kcal = df_ratio_kcal.sort_values(by='Valeur', ascending=False)
        df_top_kcal_20 = df_ratio_kcal.nlargest(20, 'Valeur')
        df_random_kcal_5 = df_top_kcal_20.sample(n=5)
        return  df_top_kcal_20 
    
    elif value == 'proteine':
           df_ratio_proteine = ratio(2)
           df_ratio_proteine = df_ratio_proteine.dropna()
           df_ratio_proteine = df_ratio_proteine.sort_values(by='Valeur', ascending=False)
           df_top_proteine_20 = df_ratio_proteine.nlargest(20, 'Valeur')
           df_random_proteine_5 = df_top_proteine_20.sample(n=5)
           return df_top_proteine_20

  
  
#totalKcal = top_nourriture('kcal') 
#print(totalKcal)
#print('----')   
#total_proteine = top_nourriture('proteine')
#print(f' top protéine {total_proteine}')


def dispo_vegetal_mondial() :
    df_vegetals = utility.formatCsv('dataFAO/FAOSTAT_2013_vegetal.csv', ["Pays","Code Élément", "Élément","Code Produit",'Produit' , "Valeur"])
    df_vegetals = df_vegetals.drop(df_vegetals[df_vegetals['Valeur']==0].index)
    
    df_vegetals_filtred_dp = utility.filtred(df_vegetals, 5301)
    df_vegetals_filtred_kcal = utility.filtred(df_vegetals, 664)
    df_vegetals_filtred_quantite = utility.filtred(df_vegetals, 645)
    
    
    #print(df_vegetals_filtred_dp)
    #print('-------------------------------------------------')
    #print(df_vegetals_filtred_kcal)
    #print('-------------------------------------------------')
    #print(df_vegetals_filtred_quantite)
    
    
    df_sum_dp = utility.calculate_and_sort(df_vegetals_filtred_dp, "Produit")
    df_sum_quantite = utility.calculate_and_sort(df_vegetals_filtred_quantite, "Produit")
    df_sum_kcal = utility.calculate_and_sort(df_vegetals_filtred_kcal, "Produit")
    df_sum_dp['Valeur'] = df_sum_dp['Valeur']*1000000
    print(f'{df_sum_dp}  kg/an')
    print('-------------------------------------------------')
    
    print(f'{df_sum_quantite} kg/personne/an')
    print('------------------------------------------------')
    df_sum_kcal['Valeur'] =  df_sum_kcal['Valeur']*365
    print(f'{df_sum_kcal} kcal/personne/an' )
   
    df_ratio = pd.merge(df_sum_kcal,df_sum_quantite,how = "outer", on = ['Produit'])
    df_ratio = df_ratio.rename(columns = {'Valeur_x' : 'kcal/personne/jour'})
    df_ratio = df_ratio.rename(columns = {'Valeur_y' : 'kg/personne/jour'})
    df_ratio['Valeur'] = df_ratio['kcal/personne/jour']/df_ratio['kg/personne/jour']
    print(f'{df_ratio} Kcal/kg')
    
    df_ratio['Valeur_dpi_kcal'] = df_ratio['Valeur'] * df_sum_dp['Valeur']
    print(f'{df_ratio} kg')
    
    df_mondial  = df_ratio['Valeur_dpi_kcal'].sum()
    print(f'{df_mondial} kcal/an')

dispo_vegetal_mondial()

def nourriture_mondial_humaine():
    dp_mondial =  dispo_vegetal_mondial()
    pop = add_pop()
    besoinMondial = 2 * pop
    print(besoinMondial)
    resultat = dp_mondial/besoinMondial*100
    print(resultat) 
nourriture_mondial_humaine()

