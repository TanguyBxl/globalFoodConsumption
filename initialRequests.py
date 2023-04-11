# importation of the librairies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

#%%

# importation of the tables

df_sous_nutrition = pd.read_csv(r"C:\Users\tangu\Desktop\Fichier_OC\sous_nutrition.csv")
df_population = pd.read_csv(r"C:\Users\tangu\Desktop\Fichier_OC\population.csv")
df_dispo_alim = pd.read_csv(r"C:\Users\tangu\Desktop\Fichier_OC\dispo_alimentaire.csv")
df_population = pd.read_csv(r"C:\Users\tangu\Desktop\Fichier_OC\population.csv")

#%%

# requestA: What is the rate of people suffering of undernutrition in the world in 2017? 


df_sous_nutrition_2017 = df_sous_nutrition[df_sous_nutrition["Année"].eq("2016-2018")]
df_population_2017 = df_population[df_population["Année"].eq(2017)]
df_final_requestA = pd.merge(df_sous_nutrition_2017, df_population_2017, on = 'Zone' , how = 'inner')
df_final_requestA.head(5)
del df_final_requestA['Année_x']
del df_final_requestA['Année_y']
df_final_requestA['pop_millions'] = df_final_requestA['Valeur_y']*1000
del df_final_requestA['Valeur_y']

df_final_requestA.rename(columns={"Valeur_x":"nb_ss_nutrition"}, inplace = True)
df_final_requestA.head(3)


df_final_requestA['pop_millions'] = df_final_requestA['pop_millions'].astype('int64')
df_final_requestA.dtypes

df_final_requestA.loc[df_final_requestA['nb_ss_nutrition'] == '<0.1','nb_ss_nutrition' ] = '0.1'
df_final_requestA['nb_ss_nutrition'] = df_final_requestA['nb_ss_nutrition'].astype(float)

df_final_requestA.dtypes

resultat = ((df_final_requestA['nb_ss_nutrition'].sum()*10**6) / (df_final_requestA['pop_millions'].sum()))
resultat_requestA = (resultat*100).round(2)
print("Answer requestA: in 2017, ", resultat_requestA,"% of the global population was undernitrited")

# Answer: in 2017, 7,13% of the global population was undernitrited

#%%

# requestB: in 2017, how many people could have been fed theoratically only with vegatal products?

df_dispo_alim_requestB = df_dispo_alim[df_dispo_alim['Origine'].eq("vegetale")]
df_dispo_alim_requestB = df_dispo_alim_requestB.groupby(by = ['Zone']).sum('Disponibilité alimentaire (Kcal/personne/jour)')

df_final_requestB = pd.merge(df_dispo_alim_requestB, df_population_2017, on= "Zone", how='inner')
df_final_requestB.head()

df_final_requestB = df_final_requestB.iloc[:,[0,3,17]]
df_final_requestB['pop_millions'] = (df_final_requestB['Valeur']*1000).astype('int64')
del df_final_requestB['Valeur']
df_final_requestB.head()

df_final_requestB.dtypes
df_final_requestB["Kcal_pays_an"] = df_final_requestB["Disponibilité alimentaire (Kcal/personne/jour)"]*df_final_requestB["pop_millions"]*365
df_final_requestB.head()

resultat = (df_final_requestB["Kcal_pays_an"].sum()) / (2500*365)
resultat_requestB = (resultat/10**9).round(3)
print ("Answer requestB: in 2017,", resultat_requestB, "billion of people could have been theorically fed just with the vegetal food produced in the word" )

# Answer: in 2017, 6.904 billion of people could have been theorically fed just with the vegetal food produced in the world

#%%

"""
Request 3: Please compute:
    - the domestic availability 
    - the food production dedicated to animal feed
    - the food lost/wasted
    - the real proportion of food consumed by humans      
"""
    

df_dispo_alim_grouped = df_dispo_alim.groupby(by=['Zone']).sum('dispo_interieure')
df_dispo_alim_grouped = df_dispo_alim_grouped.iloc[:,[0,1,6,9,10,11,12]]
len(df_dispo_alim_grouped)
df_dispo_alim_grouped.dtypes
df_dispo_alim_grouped.fillna(0.0)

print("Answers of requestC: (unit = thousands of tons)")
Total_animaux = df_dispo_alim_grouped["Aliments pour animaux"].sum()
print ("Total of aninmal food produced is:",Total_animaux)
Total_autres_utilisations = df_dispo_alim_grouped["Autres Utilisations"].sum()
print ("Total of 'other uses' is:",Total_autres_utilisations)
Total_dispo_interieure = df_dispo_alim_grouped['Disponibilité intérieure'].sum()
print ('Total domestic food availability is:',Total_dispo_interieure)
Total_nourriture = df_dispo_alim_grouped['Nourriture'].sum()
print ("Total human food produced:",Total_nourriture)
Total_pertes = df_dispo_alim_grouped['Pertes'].sum()
print ("Total lost/wasted food:",Total_pertes)
Total_production = df_dispo_alim_grouped['Production'].sum()
print ("Total production",Total_production)
Total_semences = df_dispo_alim_grouped['Semences'].sum()
print ("Total seed:",Total_semences)

globperc_animalFeed = ((Total_animaux / Total_dispo_interieure)*100).round(2)
print("So, the percentage of total food dedicated to animal feed is:", globperc_animalFeed,"%")

globperc_humanCons = ((Total_nourriture / Total_dispo_interieure)*100).round(2)
print("So, the percentage of total food dedicated to human consumption is:", globperc_humanCons,"%")

globperc_wastedFood = ((Total_pertes / Total_dispo_interieure)*100).round(2)
print(globperc_wastedFood, "% of the food in the world is lost/wasted")

globperc_seed = ((Total_semences / Total_dispo_interieure)*100).round(2)
print(globperc_seed, "% of the food produced is re-invested in seed -> we can note here is very good productivity")



# Let's visualize this repartition through a pie chart:

x = np.array([Total_nourriture, Total_animaux, Total_autres_utilisations,Total_pertes, Total_semences])
label = ["Nourriture", "Allocation animaux", "Autres Utilisations","Pertes", "Semences"]
plt.pie(x, labels=label, counterclock=False)
plt.show()






