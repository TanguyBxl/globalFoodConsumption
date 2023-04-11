# importation of the librairies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

#%%

# raw data necessary here

df_dispo_alim = pd.read_csv(r"C:\Users\tangu\Desktop\Fichier_OC\dispo_alimentaire.csv")
df_sous_nutrition = pd.read_csv(r"C:\Users\tangu\Desktop\Fichier_OC\sous_nutrition.csv")
df_population = pd.read_csv(r"C:\Users\tangu\Desktop\Fichier_OC\population.csv")
df_aide_alimentaire = pd.read_csv(r"C:\Users\tangu\Desktop\Fichier_OC\aide_alimentaire.csv")


#%%

# Please let me know what you observe about the management of the manioc production in Thaïland

df_dispo_alim_thai = df_dispo_alim[df_dispo_alim["Zone"].eq("Thaïlande")]
df_dispo_alim_thai = df_dispo_alim_thai[df_dispo_alim_thai["Produit"].eq("Manioc")]
df_dispo_alim_thai.head()

df_sous_nutrition_thai = df_sous_nutrition[df_sous_nutrition["Zone"].eq("Thaïlande")]
df_sous_nutrition_thai = df_sous_nutrition_thai[df_sous_nutrition_thai["Année"].eq("2016-2018")]
df_sous_nutrition_thai.head()

"""
Observations:
La Thaïlande produit 30 millions de tonnes de manioc en 2017. Alors même que 6,2 millions de Thaïlandais sont en état de sous-nutrition, le pays exporte 83% de sa production. (Accessoirement, il en destine aussi 6% à l'alimentation animale.)
Cette situation de voir un pays exporter les ressources qui permettraient de nourrir sa propre population interroge sur la gestion des ressources ainsi que sur les mécanismes et enjeux régulant les flux de nourriture dans le monde. Cela engendre une grande contradiction: la Thaïlande n'a que peux de disponibilité intérieure (Manioc) comparé à sa production.
car pour rappel:
Disponibilité intérieure = Production + Importation - Exportation + Variation de Stock
"""

#%%

# Request from Melanie1: What are the countries with the highest rate of person suffering of undernutrition?

df_sous_nutrition_2017 = df_sous_nutrition[df_sous_nutrition['Année'].eq('2016-2018')]
df_population_2017 = df_population[df_population['Année'].eq(2017)]
df_final = pd.merge(df_sous_nutrition_2017, df_population_2017, on='Zone', how='inner')
df_final.head()

del df_final['Année_x']
del df_final['Année_y']
df_final.dtypes
df_final = df_final.rename(columns = {'Valeur_x' : "nb_ss_nutrition", 'Valeur_y' : 'pop_millions'})
df_final['pop_millions'] = df_final['pop_millions']*1000

inaccurate_nb = df_final[(df_final['nb_ss_nutrition'] == '<0.1')].index
df_final.drop(inaccurate_nb, inplace = True)

df_final['nb_ss_nutrition'] = df_final['nb_ss_nutrition'].astype(float)
df_final['pop_millions'] = df_final['pop_millions'].astype(float)

df_final.head()
df_final['pourcentage'] = (((df_final['nb_ss_nutrition']*10**6) / df_final['pop_millions'])*100).round(2)

resultat = df_final.sort_values(by = 'pourcentage', ascending = False)
resultat.head(25)

#%%

# Request from Melanie2: What are the countries which have received the most of financial aids? 

df_aide_alimentaire['Année'].unique()


# Remarque: en voyant le .head() nous pouvions supposer que 2013 était l'année de départ de récolte des données. Et on peut voir avec le unique que c'est le cas. Donc nous avons pouvons tout agréger. 

df_aide_alimentaire_grouped = df_aide_alimentaire.groupby(['Pays bénéficiaire']).sum('Valeur')
del df_aide_alimentaire_grouped['Année']
df_aide_alimentaire_grouped.head()

resultat_ordonné = df_aide_alimentaire_grouped.sort_values(by = 'Valeur', ascending = False)
del resultat_ordonné['Année']
resultat_ordonné = resultat_ordonné.rename(columns = {"Valeur" : "aide_reçue_tonnes"})

resultat_ordonné.head(10)


#%%

# Request from Melanie3: What are the countries with the most/less of food availability per capita? 

df_dispo_alimentaire_grouped = df_dispo_alim.groupby(['Zone']).sum('Disponibilité alimentaire (Kcal/personne/jour)')
df_dispo_alimentaire_grouped = df_dispo_alimentaire_grouped.iloc[:,[2,3,4,5]]
df_dispo_alimentaire_grouped.head()

df_dispo_alimentaire_grouped.sort_values('Disponibilité alimentaire (Kcal/personne/jour)')















