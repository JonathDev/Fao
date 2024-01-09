import pandas as pd
import numpy as np 


def formatCsv(file_path, columns):
  """
    Lire un fichier CSV et retourne un sous-ensemble de colonnes d'un DataFrame Pandas.

    Paramètres:
      file_path (str): Chemin vers le fichier CSV à lire.
      columns (list): Liste des noms des colonnes à sélectionner.

    Retourne:
      (DataFrame): Un DataFrame contenant uniquement les colonnes spécifiées 
      et en supprimant le doublon du pays 'Chine'.
 """
  # création du dataFrame initiale a partir d'un csv 
  df = pd.read_csv(file_path)
  
  # Standariser le dataFrame avec les données utile
  if 'Zone' in df.columns:
    df = df.rename(columns={'Zone' : "Pays"})
    
  # supprimmer le doublon de la chine
  indices = df[df["Pays"] == 'Chine'].index
  df = df.drop(indices)
  
  #recuperer les données utiles
  df = df[columns]
  return df


"""    indices = df[df["Zone"] == 'Chine'].index
    df = df.drop(indices)"""

def filtred(df, code) :
  """création d'un dataFrame en filtrant les données en fonction du Code Element

  Args:
      df (_type_): dataFrame valide
      code (_type_): un Code Element Valide

  Returns:
      DataFrame:  le dataFrame trié. 
  """
  df_filtred = df.loc[df['Code Élément'] == code, ['Pays', 'Produit', 'Valeur', 'Code Produit']]
  return df_filtred 

def calculate_and_sort(df, sort):
  
  """création d'un dataFrame en additionnant les valeurs en fonctuion du produit ou du pays 
     important on reset l'index pour avoir les colonnes. 
  Paramètres: un dataFrame valide et un code soit ('produit') ou ('pays')
  Returns: detaFrame dont les valeurs sont caculer

  """
  df_sum = df.groupby(sort)['Valeur'].sum().reset_index()
  return df_sum

def concat (df_1, df_2) :
  df = pd.concat([df_1, df_2])
  return df  